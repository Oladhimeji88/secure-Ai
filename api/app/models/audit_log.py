import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    event_type: Mapped[str] = mapped_column(String(120), nullable=False)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    details: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)


class SystemSettings(Base):
    __tablename__ = "system_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    phishing_threshold: Mapped[int] = mapped_column(Integer, default=65, nullable=False)
    step_up_threshold: Mapped[int] = mapped_column(Integer, default=70, nullable=False)
    anomaly_threshold: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    gateway_risk_threshold: Mapped[int] = mapped_column(Integer, default=50, nullable=False)
    allow_tools: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)
