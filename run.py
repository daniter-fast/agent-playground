import os
import sys
import uvicorn
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    load_dotenv(".env.local")  # Load Next.js environment variables

    # Check for required environment variables
    required_vars = ["GITHUB_TOKEN", "ANTHROPIC_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"- {var}")
        sys.exit(1)

    # Start the FastAPI server
    print("Starting the application...")
    print("Visit http://localhost:8000 to access the application")
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main() 