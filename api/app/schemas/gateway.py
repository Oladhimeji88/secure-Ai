from pydantic import BaseModel, Field


class AgentSubmitRequest(BaseModel):
    prompt: str
    tool_name: str
    tool_args: dict = Field(default_factory=dict)


class AgentSubmitResponse(BaseModel):
    decision: str
    reasons: list[str]
    risk_score: int


class GatewayPolicyResponse(BaseModel):
    gateway_risk_threshold: int
    allow_tools: list[str]
