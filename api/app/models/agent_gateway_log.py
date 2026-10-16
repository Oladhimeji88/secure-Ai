import uuid
from datetime import datetime

from sqlalchemy import ARRAY, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AgentGatewayLog(Base):
    __tablename__ = "agent_gateway_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    prompt_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    tool_name: Mapped[str] = mapped_column(String(120), nullable=False)
    tool_args: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    decision: Mapped[str] = mapped_column(String(10), nullable=False)
    reasons: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)
