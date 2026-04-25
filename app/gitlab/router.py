from fastapi import APIRouter, HTTPException
from gitlab.exceptions import GitlabAuthenticationError, GitlabGetError
from app.gitlab.models import (
    GitLabRequest, IssueRequest,
    CommitsResponse, SummaryResponse, IssueResponse,
)
from app.gitlab.client import get_commits, build_summary, create_issue

router = APIRouter(prefix="/gitlab", tags=["gitlab"])


def _handle(e: Exception):
    if isinstance(e, GitlabAuthenticationError):
        raise HTTPException(status_code=401, detail="Invalid GitLab token")
    if isinstance(e, GitlabGetError):
        raise HTTPException(status_code=404, detail="Project not found")
    raise HTTPException(status_code=500, detail=str(e))


@router.post("/commits", response_model=CommitsResponse)
def commits(req: GitLabRequest):
    try:
        return get_commits(req)
    except Exception as e:
        _handle(e)


@router.post("/summary", response_model=SummaryResponse)
def summary(req: GitLabRequest):
    try:
        return build_summary(req)
    except Exception as e:
        _handle(e)


@router.post("/issue", response_model=IssueResponse)
def issue(req: IssueRequest):
    try:
        return create_issue(req)
    except Exception as e:
        _handle(e)
