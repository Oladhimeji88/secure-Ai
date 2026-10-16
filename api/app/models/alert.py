import enum
import uuid
from datetime import datetime

from sqlalchemy import ARRAY, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Severity(str, enum.Enum):
    LOW = "low"
    MED = "med"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(str, enum.Enum):
    OPEN = "open"
    TRIAGED = "triaged"
    CLOSED = "closed"


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    module: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[Severity] = mapped_column(Enum(Severity, name="severity_enum"), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[AlertStatus] = mapped_column(Enum(AlertStatus, name="status_enum"), nullable=False, default=AlertStatus.OPEN)
    reasons: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)
    recommended_actions: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)
    evidence: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    related_asset_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=True)
