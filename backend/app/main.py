import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .models.github import RequestTestsPayload
from .handlers.github_handler import GitHubHandler
from .handlers.llm_handler import LLMHandler

app = FastAPI()

# Get the root directory
root_dir = Path(__file__).parent.parent.parent
static_dir = root_dir / ".next" / "static"
public_dir = root_dir / "public"

# Mount static files
app.mount("/_next/static", StaticFiles(directory=str(static_dir)), name="static")
app.mount("/public", StaticFiles(directory=str(public_dir)), name="public")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize handlers
github_handler = GitHubHandler()
llm_handler = LLMHandler()

@app.get("/")
async def serve_root():
    return FileResponse(str(root_dir / ".next" / "server" / "app" / "index.html"))

@app.get("/api/pull-requests")
async def get_pull_requests():
    try:
        return await github_handler.get_pull_requests()
    except Exception as e:
        print(f"Error fetching pull requests: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/request-tests")
async def request_tests(payload: RequestTestsPayload):
    try:
        # Get PR files and details
        pr_data = await github_handler.get_pr_files(
            payload.owner,
            payload.repo,
            payload.prNumber
        )
        
        if not pr_data['files']:
            raise HTTPException(
                status_code=400,
                detail="No files found in the pull request"
            )
        
        # Get code review message
        try:
            review = llm_handler.get_code_review(pr_data['files'])
        except Exception as e:
            print(f"Error getting code review: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate code review: {str(e)}"
            )
        
        if not review:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate code review: Empty response"
            )
        
        # Format the comment
        try:
            comment = llm_handler.format_comment(
                username=pr_data['pr']['user']['login'],
                review=review
            )
        except Exception as e:
            print(f"Error formatting comment: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to format comment: {str(e)}"
            )
        
        return {
            "success": True,
            "comment": comment
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in request_tests: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@app.post("/api/post-comment")
async def post_comment(payload: RequestTestsPayload):
    if not payload.comment:
        raise HTTPException(
            status_code=400,
            detail="Comment text is required"
        )
        
    try:
        print(f"Attempting to post comment on PR #{payload.prNumber} in {payload.owner}/{payload.repo}")
        
        # Post comment using the new method
        result = await github_handler.post_comment(
            payload.owner,
            payload.repo,
            payload.prNumber,
            payload.comment
        )
        
        print(f"Successfully posted comment: {result.get('html_url', '')}")
        return {
            "success": True,
            "comment_url": result.get('html_url')
        }
    except Exception as e:
        print(f"Error posting comment: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to post comment: {str(e)}"
        )

# Catch-all route for Next.js pages
@app.get("/{path:path}")
async def serve_pages(path: str):
    # Try to serve the HTML file for the route
    html_path = root_dir / ".next" / "server" / "app" / path / "index.html"
    if html_path.exists():
        return FileResponse(str(html_path))
    
    # If not found, serve the 404 page
    return FileResponse(str(root_dir / ".next" / "server" / "app" / "_not-found.html")) 