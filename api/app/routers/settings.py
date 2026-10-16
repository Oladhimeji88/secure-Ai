from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.rbac import require_roles
from app.db.session import get_db
from app.models.audit_log import AuditLog, SystemSettings
from app.models.user import Role, User
from app.schemas.settings import ThresholdSettingsUpdate

router = APIRouter(prefix="/settings", tags=["settings"])


def _get_or_create_settings(db: Session) -> SystemSettings:
    settings = db.query(SystemSettings).filter(SystemSettings.id == 1).first()
    if not settings:
        settings = SystemSettings(id=1, allow_tools=["read_alerts", "search_kb", "open_ticket"])
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


@router.get("/users")
def list_users(db: Session = Depends(get_db), _=Depends(require_roles([Role.ADMIN, Role.ANALYST, Role.READ_ONLY]))) -> dict:
    users = db.query(User).order_by(User.email.asc()).all()
    return {"items": [{"id": str(u.id), "email": u.email, "full_name": u.full_name, "role": u.role.value} for u in users]}


@router.get("/thresholds")
def get_thresholds(db: Session = Depends(get_db), _=Depends(require_roles([Role.ADMIN, Role.ANALYST, Role.READ_ONLY]))) -> dict:
    s = _get_or_create_settings(db)
    return {
        "phishing_threshold": s.phishing_threshold,
        "step_up_threshold": s.step_up_threshold,
        "anomaly_threshold": s.anomaly_threshold,
        "gateway_risk_threshold": s.gateway_risk_threshold,
        "allow_tools": s.allow_tools,
    }


@router.put("/thresholds")
def update_thresholds(payload: ThresholdSettingsUpdate, db: Session = Depends(get_db), _=Depends(require_roles([Role.ADMIN]))) -> dict:
    s = _get_or_create_settings(db)
    s.phishing_threshold = payload.phishing_threshold
    s.step_up_threshold = payload.step_up_threshold
    s.anomaly_threshold = payload.anomaly_threshold
    s.gateway_risk_threshold = payload.gateway_risk_threshold
    s.allow_tools = payload.allow_tools
    db.add(AuditLog(event_type="threshold_update", details=payload.model_dump()))
    db.commit()
    return {"updated": True}
