import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

client = TestClient(app)

def test_post_comment():
    """Test that we can successfully post a comment to a GitHub PR"""
    
    test_data = {
        "owner": os.getenv("TEST_REPO_OWNER"),
        "repo": os.getenv("TEST_REPO_NAME"),
        "prNumber": int(os.getenv("TEST_PR_NUMBER")),
        "comment": "🤖 Test comment from automated test!\n\nThis is a test of the automated comment posting system. If you see this, it means the test passed! 🎉"
    }
    
    response = client.post("/api/post-comment", json=test_data)
    assert response.status_code == 200, f"Failed to post comment: {response.text}"
    assert response.json()["success"] == True 