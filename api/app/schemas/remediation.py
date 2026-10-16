from pydantic import BaseModel


class RemediationItem(BaseModel):
    cve: str | None
    asset: str
    priority_score: float
    sla_suggestion: str
    patch_available: bool


class RemediationPlanResponse(BaseModel):
    items: list[RemediationItem]
