from pydantic import BaseModel


class AssetOut(BaseModel):
    id: str
    name: str
    type: str
    owner: str
    criticality: str
    internet_exposed: bool
    tags: list[str]

    class Config:
        from_attributes = True


class AssetDetailResponse(BaseModel):
    asset: AssetOut
    findings: list[dict]
    recent_alerts: list[dict]
