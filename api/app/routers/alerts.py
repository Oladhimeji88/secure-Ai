from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.rbac import require_roles
from app.db.session import get_db
from app.models.alert import Alert, AlertStatus
from app.models.user import Role
from app.schemas.alert import AlertListResponse, AlertOut

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=AlertListResponse)
def list_alerts(
    module: str | None = None,
    severity: str | None = None,
    status: str | None = None,
    min_score: int | None = None,
    max_score: int | None = None,
    db: Session = Depends(get_db),
    _=Depends(require_roles([Role.ADMIN, Role.ANALYST, Role.READ_ONLY])),
) -> AlertListResponse:
    query = db.query(Alert)
    if module:
        query = query.filter(Alert.module == module)
    if severity:
        query = query.filter(Alert.severity == severity)
    if status:
        query = query.filter(Alert.status == status)
    if min_score is not None:
        query = query.filter(Alert.score >= min_score)
    if max_score is not None:
        query = query.filter(Alert.score <= max_score)

    alerts = query.order_by(Alert.created_at.desc()).all()
    return AlertListResponse(items=[AlertOut.model_validate(a) for a in alerts], total=len(alerts))


@router.get("/{alert_id}", response_model=AlertOut)
def get_alert(alert_id: str, db: Session = Depends(get_db), _=Depends(require_roles([Role.ADMIN, Role.ANALYST, Role.READ_ONLY]))) -> AlertOut:
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return AlertOut.model_validate(alert)


@router.post("/{alert_id}/triage")
def triage_alert(alert_id: str, db: Session = Depends(get_db), _=Depends(require_roles([Role.ADMIN, Role.ANALYST]))) -> dict:
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.status = AlertStatus.TRIAGED
    db.commit()
    db.refresh(alert)
    return {"status": alert.status, "id": str(alert.id)}
