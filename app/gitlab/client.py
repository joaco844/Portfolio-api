import gitlab
from app.gitlab.models import (
    GitLabRequest, IssueRequest,
    CommitItem, CommitsResponse, SummaryResponse, IssueResponse,
)


def _connect(token: str) -> gitlab.Gitlab:
    gl = gitlab.Gitlab("https://gitlab.com", private_token=token)
    gl.auth()
    return gl


def get_commits(req: GitLabRequest) -> CommitsResponse:
    gl = _connect(req.token)
    project = gl.projects.get(req.project_id)
    raw = project.commits.list(
        ref_name=req.branch,
        since=f"{req.date_from}T00:00:00Z",
        until=f"{req.date_to}T23:59:59Z",
        get_all=True,
    )
    items = [
        CommitItem(
            id=c.short_id,
            title=c.title,
            author=c.author_name,
            date=c.created_at[:10],
        )
        for c in raw
    ]
    return CommitsResponse(commits=items, total=len(items))


def build_summary(req: GitLabRequest) -> SummaryResponse:
    result = get_commits(req)
    lines = [
        f"## Release Summary — `{req.branch}`",
        f"**Period:** {req.date_from} → {req.date_to}  ",
        f"**Total commits:** {result.total}",
        "",
        "| Commit | Title | Author | Date |",
        "|--------|-------|--------|------|",
    ]
    for c in result.commits:
        lines.append(f"| `{c.id}` | {c.title} | {c.author} | {c.date} |")
    return SummaryResponse(summary="\n".join(lines))


def create_issue(req: IssueRequest) -> IssueResponse:
    gl = _connect(req.token)
    project = gl.projects.get(req.project_id)
    summary = build_summary(req)
    issue = project.issues.create({
        "title": req.issue_title,
        "description": summary.summary,
        "labels": ["release-summary"],
    })
    return IssueResponse(issue_url=issue.web_url, issue_id=issue.iid)
