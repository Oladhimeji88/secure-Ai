from datetime import datetime
from pydantic import BaseModel, Field


class AlertOut(BaseModel):
    id: str
    created_at: datetime
    module: str
    severity: str
    score: int = Field(ge=0, le=100)
    status: str
    reasons: list[str]
    recommended_actions: list[str]
    evidence: dict
    related_asset_id: str | None = None

    class Config:
        from_attributes = True


class AlertListResponse(BaseModel):
    items: list[AlertOut]
    total: int
