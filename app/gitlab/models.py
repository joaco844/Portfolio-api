from pydantic import BaseModel


class GitLabRequest(BaseModel):
    token: str
    project_id: str
    branch: str = "main"
    date_from: str  # YYYY-MM-DD
    date_to: str    # YYYY-MM-DD


class CommitItem(BaseModel):
    id: str
    title: str
    author: str
    date: str


class CommitsResponse(BaseModel):
    commits: list[CommitItem]
    total: int


class SummaryResponse(BaseModel):
    summary: str  # markdown


class IssueRequest(GitLabRequest):
    issue_title: str = "Release Summary"


class IssueResponse(BaseModel):
    issue_url: str
    issue_id: int
