from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.rbac import require_roles
from app.db.session import get_db
from app.models.agent_gateway_log import AgentGatewayLog
from app.models.audit_log import AuditLog, SystemSettings
from app.models.user import Role
from app.schemas.settings import ThresholdSettingsUpdate

router = APIRouter(prefix="/agent-gateway", tags=["agent-gateway"])


def _get_or_create_settings(db: Session) -> SystemSettings:
    settings = db.query(SystemSettings).filter(SystemSettings.id == 1).first()
    if not settings:
        settings = SystemSettings(id=1, allow_tools=["read_alerts", "search_kb", "open_ticket"])
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


@router.get("/logs")
def list_gateway_logs(db: Session = Depends(get_db), _=Depends(require_roles([Role.ADMIN, Role.ANALYST, Role.READ_ONLY]))) -> dict:
    rows = db.query(AgentGatewayLog).order_by(AgentGatewayLog.created_at.desc()).limit(200).all()
    return {
        "items": [
            {
                "id": str(r.id),
                "created_at": r.created_at,
                "tool_name": r.tool_name,
                "decision": r.decision,
                "reasons": r.reasons,
            }
            for r in rows
        ]
    }


@router.get("/policy")
def get_gateway_policy(db: Session = Depends(get_db), _=Depends(require_roles([Role.ADMIN, Role.ANALYST, Role.READ_ONLY]))) -> dict:
    s = _get_or_create_settings(db)
    return {"gateway_risk_threshold": s.gateway_risk_threshold, "allow_tools": s.allow_tools}


@router.put("/policy")
def update_gateway_policy(
    payload: ThresholdSettingsUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_roles([Role.ADMIN])),
) -> dict:
    s = _get_or_create_settings(db)
    s.gateway_risk_threshold = payload.gateway_risk_threshold
    s.allow_tools = payload.allow_tools
    db.add(AuditLog(event_type="policy_update", details=payload.model_dump()))
    db.commit()
    return {"updated": True}
