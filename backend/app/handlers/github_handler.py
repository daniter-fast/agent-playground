from typing import List, Dict, Set
import os
import base64
import time
import asyncio
import aiohttp
from datetime import datetime, timedelta
from functools import partial
from github import Github
from ..models.github import PullRequest, Repository

class GitHubHandler:
    def __init__(self):
        self._cache = {}
        self._cache_timeout = timedelta(minutes=5)
        self._session = None
        self._headers = {
            'Authorization': f'token {os.getenv("GITHUB_TOKEN")}',
            'Accept': 'application/vnd.github.v3+json'
        }

    async def _ensure_session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession(headers=self._headers)
        return self._session

    @property
    def client(self):
        return Github(os.getenv("GITHUB_TOKEN"))

    def _get_from_cache(self, key: str):
        if key in self._cache:
            data, timestamp = self._cache[key]
            if datetime.now() - timestamp < self._cache_timeout:
                return data
            else:
                del self._cache[key]
        return None

    def _set_cache(self, key: str, data):
        self._cache[key] = (data, datetime.now())

    async def _get_user_repos(self) -> List[Dict]:
        """Get user's personal repositories using aiohttp"""
        session = await self._ensure_session()
        async with session.get('https://api.github.com/user/repos?type=all&per_page=100') as response:
            if response.status == 200:
                repos = await response.json()
                return [{
                    'repo': repo,
                    'org': None
                } for repo in repos]
            return []

    async def _get_org_repos(self, org_url: str) -> List[Dict]:
        """Get organization's repositories using aiohttp"""
        session = await self._ensure_session()
        async with session.get(f'{org_url}/repos?per_page=100') as response:
            if response.status == 200:
                repos = await response.json()
                return [{
                    'repo': repo,
                    'org': org_url
                } for repo in repos]
            return []

    async def _get_org_list(self) -> List[str]:
        """Get list of user's organizations using aiohttp"""
        session = await self._ensure_session()
        async with session.get('https://api.github.com/user/orgs') as response:
            if response.status == 200:
                orgs = await response.json()
                return [org['url'] for org in orgs]
            return []

    async def get_repos(self) -> List[Dict]:
        """Get all repositories (personal and from organizations) with caching"""
        cache_key = 'all_repos'
        cached_repos = self._get_from_cache(cache_key)
        if cached_repos:
            return cached_repos

        # Get personal repos
        personal_repos = await self._get_user_repos()

        # Get org repos concurrently
        org_urls = await self._get_org_list()
        org_repo_tasks = [self._get_org_repos(org_url) for org_url in org_urls]
        org_repos_lists = await asyncio.gather(*org_repo_tasks)
        
        # Combine all repos
        all_repos = personal_repos
        for org_repos in org_repos_lists:
            all_repos.extend(org_repos)

        self._set_cache(cache_key, all_repos)
        return all_repos

    async def _get_pull_requests(self, repo_data: Dict) -> List[PullRequest]:
        """Get pull requests for a repository using aiohttp"""
        repo = repo_data['repo']
        repo_full_name = repo['full_name']
        session = await self._ensure_session()
        
        try:
            async with session.get(f'https://api.github.com/repos/{repo_full_name}/pulls?state=open') as response:
                if response.status != 200:
                    print(f"Error getting PRs for {repo_full_name}: {response.status}")
                    return []
                
                pulls = await response.json()
                return [
                    PullRequest(
                        id=pr['id'],
                        number=pr['number'],
                        title=pr['title'],
                        html_url=pr['html_url'],
                        user={"login": pr['user']['login']},
                        repository={
                            "name": repo['name'],
                            "full_name": repo_full_name
                        },
                        hasTests=None  # We'll load this later
                    )
                    for pr in pulls
                ]
        except Exception as e:
            print(f"Error processing repo {repo_full_name}: {str(e)}")
            return []

    async def get_pull_requests(self) -> List[PullRequest]:
        start_time = time.time()
        
        # Get all repositories (cached)
        repos = await self.get_repos()
        print(f"Got {len(repos)} repositories in {time.time() - start_time:.2f}s")

        # Process repositories concurrently
        tasks = [self._get_pull_requests(repo_data) for repo_data in repos]
        results = await asyncio.gather(*tasks)

        # Flatten results
        all_prs = [pr for prs in results for pr in prs]
        
        print(f"Total time to get {len(all_prs)} PRs: {time.time() - start_time:.2f}s")
        return all_prs

    async def get_pr_files(self, owner: str, repo: str, pr_number: int):
        """Get PR files using aiohttp"""
        session = await self._ensure_session()
        files = []

        try:
            # Get PR details
            async with session.get(f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}') as response:
                if response.status != 200:
                    raise Exception(f"Failed to get PR: {response.status}")
                pr_data = await response.json()

            # Get PR files
            async with session.get(f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files') as response:
                if response.status != 200:
                    raise Exception(f"Failed to get PR files: {response.status}")
                pr_files = await response.json()

            for file in pr_files:
                if file['status'] != 'removed':
                    # Get file content
                    async with session.get(file['contents_url']) as response:
                        if response.status == 200:
                            content_data = await response.json()
                            decoded_content = base64.b64decode(content_data['content']).decode('utf-8')
                            files.append({
                                'filename': file['filename'],
                                'content': decoded_content
                            })

            # Transform PR data to match expected structure
            transformed_pr = {
                'user': {
                    'login': pr_data['user']['login']
                },
                'number': pr_number,
                'html_url': pr_data['html_url'],
                'title': pr_data['title'],
                'body': pr_data['body']
            }

            return {
                'files': files,
                'pr': transformed_pr
            }
        except Exception as e:
            print(f"Error getting PR files: {str(e)}")
            raise

    async def post_comment(self, owner: str, repo: str, pr_number: int, comment: str):
        """Post a comment on a PR using aiohttp"""
        session = await self._ensure_session()
        url = f'https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments'
        
        print(f"Posting comment to {url}")
        print(f"Comment content: {comment[:100]}...")  # Print first 100 chars for debugging
        
        async with session.post(url, json={'body': comment}) as response:
            if response.status != 201:  # GitHub API returns 201 for successful creation
                response_data = await response.json()
                error_msg = f"Failed to post comment: {response.status} - {response_data.get('message', '')}"
                print(error_msg)  # Log the error
                raise Exception(error_msg)
            
            result = await response.json()
            print(f"Successfully posted comment. Response: {result.get('html_url', '')}")
            return result

    async def __del__(self):
        if self._session:
            await self._session.close() 