from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.alert import Alert

router = APIRouter(prefix="/overview", tags=["overview"])


@router.get("")
def get_overview(db: Session = Depends(get_db)) -> dict:
    total_alerts = db.query(func.count(Alert.id)).scalar() or 0
    high_sev = db.query(func.count(Alert.id)).filter(Alert.severity.in_(["high", "critical"])).scalar() or 0
    assets_at_risk = db.query(func.count(func.distinct(Alert.related_asset_id))).filter(Alert.related_asset_id.isnot(None)).scalar() or 0
    open_remediations = db.query(func.count(Alert.id)).filter(Alert.status == "open").scalar() or 0

    now = datetime.now(timezone.utc)
    trend = []
    for i in range(6, -1, -1):
        day_start = (now - timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        count = db.query(func.count(Alert.id)).filter(Alert.created_at >= day_start, Alert.created_at < day_end).scalar() or 0
        trend.append({"date": day_start.date().isoformat(), "alerts": count})

    module_rows = db.query(Alert.module, func.count(Alert.id)).group_by(Alert.module).all()
    module_breakdown = [{"module": row[0], "count": row[1]} for row in module_rows]

    return {
        "kpis": {
            "total_alerts": total_alerts,
            "high_severity": high_sev,
            "assets_at_risk": assets_at_risk,
            "open_remediations": open_remediations,
        },
        "trend": trend,
        "module_breakdown": module_breakdown,
    }
