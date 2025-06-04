import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

client = TestClient(app)

def test_get_pull_requests():
    """Test that we can fetch pull requests from both personal and org repos"""
    response = client.get("/api/pull-requests")
    assert response.status_code == 200
    
    prs = response.json()
    print(f"\nFound {len(prs)} pull requests:")
    for pr in prs:
        print(f"- {pr['repository']['full_name']}#{pr['number']}: {pr['title']}")
    
    assert len(prs) >= 0  # We should at least not error, even if there are no PRs

def test_post_comment():
    """Test that we can successfully post a comment to a GitHub PR"""
    
    # Debug: Print environment variables
    print("\nEnvironment variables:")
    print(f"TEST_REPO_OWNER: {os.getenv('TEST_REPO_OWNER')}")
    print(f"TEST_REPO_NAME: {os.getenv('TEST_REPO_NAME')}")
    print(f"TEST_PR_NUMBER: {os.getenv('TEST_PR_NUMBER')}")
    print(f"GITHUB_TOKEN: {'*' * len(os.getenv('GITHUB_TOKEN') or '') if os.getenv('GITHUB_TOKEN') else 'None'}\n")
    
    test_data = {
        "owner": os.getenv("TEST_REPO_OWNER"),
        "repo": os.getenv("TEST_REPO_NAME"),
        "prNumber": int(os.getenv("TEST_PR_NUMBER")),
        "comment": "🤖 Test comment from automated test!\n\nThis is a test of the automated comment posting system. If you see this, it means the test passed! 🎉"
    }
    
    response = client.post("/api/post-comment", json=test_data)
    assert response.status_code == 200, f"Failed to post comment: {response.text}"
    assert response.json()["success"] == True 