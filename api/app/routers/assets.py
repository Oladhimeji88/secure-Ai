from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.rbac import require_roles
from app.db.session import get_db
from app.models.alert import Alert
from app.models.asset import Asset
from app.models.finding import Finding
from app.models.user import Role
from app.schemas.asset import AssetDetailResponse, AssetOut

router = APIRouter(prefix="/assets", tags=["assets"])


@router.get("")
def list_assets(db: Session = Depends(get_db), _=Depends(require_roles([Role.ADMIN, Role.ANALYST, Role.READ_ONLY]))) -> dict:
    assets = db.query(Asset).order_by(Asset.name.asc()).all()
    return {"items": [AssetOut.model_validate(a).model_dump() for a in assets], "total": len(assets)}


@router.get("/{asset_id}", response_model=AssetDetailResponse)
def get_asset(asset_id: str, db: Session = Depends(get_db), _=Depends(require_roles([Role.ADMIN, Role.ANALYST, Role.READ_ONLY]))) -> AssetDetailResponse:
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    findings = db.query(Finding).filter(Finding.asset_id == asset_id).order_by(Finding.created_at.desc()).all()
    alerts = db.query(Alert).filter(Alert.related_asset_id == asset_id).order_by(Alert.created_at.desc()).limit(20).all()
    return AssetDetailResponse(
        asset=AssetOut.model_validate(asset),
        findings=[
            {"id": str(f.id), "category": f.category.value, "cve": f.cve, "details": f.details, "created_at": f.created_at}
            for f in findings
        ],
        recent_alerts=[
            {"id": str(a.id), "module": a.module, "severity": a.severity.value, "score": a.score, "status": a.status.value}
            for a in alerts
        ],
    )
