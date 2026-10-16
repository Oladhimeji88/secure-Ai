from pydantic import BaseModel, Field


class ThresholdSettings(BaseModel):
    phishing_threshold: int = Field(ge=0, le=100)
    step_up_threshold: int = Field(ge=0, le=100)
    anomaly_threshold: int = Field(ge=0, le=100)


class ThresholdSettingsUpdate(ThresholdSettings):
    gateway_risk_threshold: int = Field(ge=0, le=100)
    allow_tools: list[str] = Field(default_factory=list)
