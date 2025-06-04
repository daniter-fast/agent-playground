# GitHub PR Test Coverage Monitor

A web application that monitors GitHub pull requests and ensures proper test coverage using AI-powered code review.

## Features

- Lists open PRs from GitHub organizations
- Detects missing test coverage
- Uses Claude to analyze code changes
- Posts automated, polite comments requesting tests
- Supports dark mode
- Handles browser extensions gracefully

## Tech Stack

- Frontend: Next.js with TypeScript and Tailwind CSS
- Backend: FastAPI (Python) with LangChain
- APIs: GitHub API, Anthropic Claude API
- Templates: Jinja2 for prompt management

## Setup

1. Clone the repository

2. Install dependencies:
   ```bash
   # Install Python dependencies
   pip install -r backend/requirements.txt

   # Install and build frontend
   npm install
   npm run build
   ```

3. Create a `.env` file in the root directory:
   ```
   GITHUB_TOKEN=your_github_token_here
   ANTHROPIC_API_KEY=your_anthropic_key_here
   ```

## Running the Application

Simply run:
```bash
python run.py
```

This will start the application and serve both the frontend and backend. Visit http://localhost:8000 to access the application.

## Development

The application is structured as follows:

- `app/` - Next.js frontend code
- `backend/` - Python FastAPI backend code
  - `app/handlers/` - GitHub and LLM integration handlers
  - `app/models/` - Pydantic data models
  - `app/prompts/` - Jinja templates for LLM prompts
- `run.py` - Single command to run the entire application

For development:
1. Make changes to the frontend code
2. Run `npm run build` to rebuild the static files
3. The server will automatically reload with the new changes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

# General Musings about using AI Agent

* Very often, the UI is broken. There is a completely manual process of pasting the error back into the chat and asking it to fix it.
* The agent will make decisions that fit your request even if it's not a good idea. For example, I started with a node.js app. Then I wanted to use langchain so i switched to python backend so it created a separate python backend server and used node.js as just a pass through for all requests.
* Generally it doesn't take into account how long things take and I often need to refine approaches like lazy loading, providing loading feedback or parallelization.
* Many tools are being used and it can go down rabbit holes trying to fix bugs. The users may not really understand the tools.
* Complexity quickly baloons and debugging becomes difficult. Example is to speed up the PR calls, it added a loop that re-calls the API every few seconds which is a bug and causes performance issues. Tracking it down is not trivial. Regressions also happened when using code generation to fix it automatically.


TODO:
[ ] Save state to a database
[x] Create a test so I can run the code that posts a comment without the UI.
[x] pull-requests takes too long (5 sec +)
[x] push to GH