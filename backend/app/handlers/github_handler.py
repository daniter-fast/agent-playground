from typing import List
import os
import base64
from github import Github
from ..models.github import PullRequest, Repository

class GitHubHandler:
    def __init__(self):
        self.client = Github(os.getenv("GITHUB_TOKEN"))

    async def get_pull_requests(self) -> List[PullRequest]:
        # Get user's organizations
        orgs = self.client.get_user().get_orgs()
        all_prs = []

        for org in orgs:
            # Get repositories for each organization
            repos = org.get_repos()
            for repo in repos:
                # Get open pull requests for each repository
                pulls = repo.get_pulls(state='open')
                for pr in pulls:
                    # Check if PR has test files
                    files = pr.get_files()
                    has_tests = any(
                        'test' in file.filename.lower() or 'spec' in file.filename.lower()
                        for file in files
                    )

                    all_prs.append(
                        PullRequest(
                            id=pr.id,
                            number=pr.number,
                            title=pr.title,
                            html_url=pr.html_url,
                            user={"login": pr.user.login},
                            repository={
                                "name": repo.name,
                                "full_name": repo.full_name
                            },
                            hasTests=has_tests
                        )
                    )

        return all_prs

    async def get_pr_files(self, owner: str, repo: str, pr_number: int):
        repo = self.client.get_repo(f"{owner}/{repo}")
        pr = repo.get_pull(pr_number)
        files = []

        for file in pr.get_files():
            if file.status != 'removed':
                content = repo.get_contents(file.filename, ref=pr.head.sha)
                decoded_content = base64.b64decode(content.content).decode('utf-8')
                files.append({
                    'filename': file.filename,
                    'content': decoded_content
                })

        return {
            'files': files,
            'pr': pr
        } 