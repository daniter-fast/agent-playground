import os
import sys
import pytest
from pathlib import Path
from dotenv import load_dotenv

@pytest.fixture(autouse=True)
def load_env():
    """Load environment variables before each test"""
    # Get the root directory (two levels up from tests/)
    root_dir = Path(__file__).parent.parent.parent
    env_file = root_dir / ".env.local"
    
    # Load the .env.local file
    load_dotenv(env_file)
    
    # Verify that we have the required environment variables
    required_vars = [
        "GITHUB_TOKEN",
        "TEST_REPO_OWNER",  # GitHub username or organization
        "TEST_REPO_NAME",   # Repository name
        "TEST_PR_NUMBER"    # PR number to test with
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise AssertionError(f"Missing required environment variables: {', '.join(missing_vars)}\n"
                           f"Please add them to your .env.local file") 