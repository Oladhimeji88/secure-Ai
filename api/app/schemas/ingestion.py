from pydantic import BaseModel, Field


class EmailIngestRequest(BaseModel):
    sender: str
    display_name: str
    subject: str
    body: str
    spf_pass: bool
    dkim_pass: bool
    dmarc_pass: bool
    urls: list[str] = Field(default_factory=list)


class ChatIngestRequest(BaseModel):
    username: str
    message: str
    channel: str


class GenericIngestResponse(BaseModel):
    alert_id: str
    score: int
    reasons: list[str]
    recommended_actions: list[str]


class SbomIngestRequest(BaseModel):
    asset_id: str
    packages: list[dict] = Field(default_factory=list)


class ScanIngestRequest(BaseModel):
    asset_id: str
    findings: list[dict] = Field(default_factory=list)


class HighRiskRequest(BaseModel):
    user_id: str | None = None
    amount: float
    context: dict = Field(default_factory=dict)


class EventIngestRequest(BaseModel):
    events: list[dict]


class TelemetryIngestRequest(BaseModel):
    host: str
    process_tree: list[str]
    connections: list[dict]
    persistence: list[str]
