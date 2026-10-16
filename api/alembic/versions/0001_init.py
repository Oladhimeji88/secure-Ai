from sqlalchemy import (
    ARRAY,
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID

from alembic import op
import sqlalchemy as sa

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    role_enum = sa.Enum("admin", "analyst", "read-only", name="role_enum")
    severity_enum = sa.Enum("low", "med", "high", "critical", name="severity_enum")
    status_enum = sa.Enum("open", "triaged", "closed", name="status_enum")
    criticality_enum = sa.Enum("low", "med", "high", name="criticality_enum")
    finding_enum = sa.Enum("vuln", "phishing", "anomaly", "malware", "ai-security", name="finding_enum")

    role_enum.create(op.get_bind(), checkfirst=True)
    severity_enum.create(op.get_bind(), checkfirst=True)
    status_enum.create(op.get_bind(), checkfirst=True)
    criticality_enum.create(op.get_bind(), checkfirst=True)
    finding_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        Column("id", UUID(as_uuid=True), primary_key=True),
        Column("email", String(255), nullable=False, unique=True),
        Column("full_name", String(255), nullable=False),
        Column("hashed_password", String(255), nullable=False),
        Column("role", role_enum, nullable=False),
        Column("is_active", Boolean, nullable=False, server_default=sa.true()),
        Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    )

    op.create_table(
        "assets",
        Column("id", UUID(as_uuid=True), primary_key=True),
        Column("name", String(255), nullable=False),
        Column("type", String(100), nullable=False),
        Column("owner", String(255), nullable=False),
        Column("criticality", criticality_enum, nullable=False),
        Column("internet_exposed", Boolean, nullable=False, server_default=sa.false()),
        Column("tags", ARRAY(String), nullable=False, server_default="{}"),
        Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    )

    op.create_table(
        "alerts",
        Column("id", UUID(as_uuid=True), primary_key=True),
        Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
        Column("module", String(100), nullable=False),
        Column("severity", severity_enum, nullable=False),
        Column("score", Integer, nullable=False),
        Column("status", status_enum, nullable=False, server_default="open"),
        Column("reasons", ARRAY(String), nullable=False, server_default="{}"),
        Column("recommended_actions", ARRAY(String), nullable=False, server_default="{}"),
        Column("evidence", JSON, nullable=False, server_default="{}"),
        Column("related_asset_id", UUID(as_uuid=True), ForeignKey("assets.id"), nullable=True),
    )
    op.create_index("ix_alerts_created_module_sev_status", "alerts", ["created_at", "module", "severity", "status"])

    op.create_table(
        "findings",
        Column("id", UUID(as_uuid=True), primary_key=True),
        Column("asset_id", UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False),
        Column("category", finding_enum, nullable=False),
        Column("cve", String(64), nullable=True),
        Column("details", JSON, nullable=False, server_default="{}"),
        Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    )
    op.create_index("ix_findings_asset_created", "findings", ["asset_id", "created_at"])

    op.create_table(
        "agent_gateway_logs",
        Column("id", UUID(as_uuid=True), primary_key=True),
        Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
        Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), nullable=False),
        Column("prompt_hash", String(128), nullable=False),
        Column("tool_name", String(120), nullable=False),
        Column("tool_args", JSON, nullable=False, server_default="{}"),
        Column("decision", String(10), nullable=False),
        Column("reasons", ARRAY(String), nullable=False, server_default="{}"),
    )
    op.create_index("ix_gateway_created_decision", "agent_gateway_logs", ["created_at", "decision"])

    op.create_table(
        "audit_logs",
        Column("id", UUID(as_uuid=True), primary_key=True),
        Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
        Column("event_type", String(120), nullable=False),
        Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), nullable=True),
        Column("details", JSON, nullable=False, server_default="{}"),
    )

    op.create_table(
        "system_settings",
        Column("id", Integer, primary_key=True),
        Column("phishing_threshold", Integer, nullable=False, server_default="65"),
        Column("step_up_threshold", Integer, nullable=False, server_default="70"),
        Column("anomaly_threshold", Integer, nullable=False, server_default="60"),
        Column("gateway_risk_threshold", Integer, nullable=False, server_default="50"),
        Column("allow_tools", ARRAY(String), nullable=False, server_default="{}"),
    )


def downgrade() -> None:
    op.drop_table("system_settings")
    op.drop_table("audit_logs")
    op.drop_index("ix_gateway_created_decision", table_name="agent_gateway_logs")
    op.drop_table("agent_gateway_logs")
    op.drop_index("ix_findings_asset_created", table_name="findings")
    op.drop_table("findings")
    op.drop_index("ix_alerts_created_module_sev_status", table_name="alerts")
    op.drop_table("alerts")
    op.drop_table("assets")
    op.drop_table("users")
