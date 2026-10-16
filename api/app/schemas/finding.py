from datetime import datetime
from pydantic import BaseModel


class FindingOut(BaseModel):
    id: str
    asset_id: str
    category: str
    cve: str | None
    details: dict
    created_at: datetime

    class Config:
        from_attributes = True
