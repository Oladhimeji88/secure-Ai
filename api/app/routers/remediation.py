import json
from pathlib import Path

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.rbac import require_roles
from app.db.session import get_db
from app.models.asset import Asset
from app.models.finding import Finding
from app.models.user import Role
from app.services.vuln_prioritizer import rank_remediation

router = APIRouter(prefix="/remediation-plan", tags=["remediation"])


@router.get("")
def remediation_plan(db: Session = Depends(get_db), _=Depends(require_roles([Role.ADMIN, Role.ANALYST, Role.READ_ONLY]))) -> dict:
    cve_file = Path("/fixtures/cve_sample.json")
    cve_data = json.loads(cve_file.read_text(encoding="utf-8")) if cve_file.exists() else []

    assets = {str(a.id): a for a in db.query(Asset).all()}
    findings = db.query(Finding).filter(Finding.cve.isnot(None)).all()
    rows = []
    cve_map = {c["cve"]: c for c in cve_data}
    for finding in findings:
        cve = cve_map.get(finding.cve)
        if not cve:
            continue
        asset = assets.get(str(finding.asset_id))
        if not asset:
            continue
        rows.append(
            {
                "cve": finding.cve,
                "cvss": cve.get("cvss", 0),
                "exploit_known": cve.get("exploit_known", False),
                "patch_available": cve.get("patch_available", False),
                "criticality": asset.criticality.value,
                "internet_exposed": asset.internet_exposed,
                "asset_name": asset.name,
            }
        )
    return {"items": rank_remediation(rows)}
