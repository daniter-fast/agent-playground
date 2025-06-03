from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    login: str

class Repository(BaseModel):
    name: str
    full_name: str

class PullRequest(BaseModel):
    id: int
    number: int
    title: str
    html_url: str
    user: User
    repository: Repository
    hasTests: bool = False

class RequestTestsPayload(BaseModel):
    owner: str
    repo: str
    prNumber: int
    comment: str | None = None  # Optional for the initial request, required for posting 