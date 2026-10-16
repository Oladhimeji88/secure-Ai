from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.rbac import require_roles
from app.db.session import get_db
from app.models.agent_gateway_log import AgentGatewayLog
from app.models.alert import Alert
from app.models.audit_log import AuditLog, SystemSettings
from app.models.user import Role, User
from app.schemas.gateway import AgentSubmitRequest
from app.schemas.ingestion import (
    ChatIngestRequest,
    EmailIngestRequest,
    EventIngestRequest,
    HighRiskRequest,
    SbomIngestRequest,
    ScanIngestRequest,
    TelemetryIngestRequest,
)
from app.services.agent_gateway import evaluate_agent_request
from app.services.identity_policy import evaluate_step_up
from app.services.malware_detector import detect_malware
from app.services.phishing_detector import score_chat, score_email
from app.services.recon_detector import detect_recon

router = APIRouter(tags=["ingest"])


def _get_or_create_settings(db: Session) -> SystemSettings:
    settings = db.query(SystemSettings).filter(SystemSettings.id == 1).first()
    if not settings:
        settings = SystemSettings(id=1, allow_tools=["read_alerts", "search_kb", "open_ticket"])
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


@router.post("/ingest/email")
def ingest_email(payload: EmailIngestRequest, db: Session = Depends(get_db), _=Depends(require_roles([Role.ADMIN, Role.ANALYST]))) -> dict:
    score, severity, reasons, actions = score_email(payload.model_dump())
    alert = Alert(module="anti-phishing", severity=severity, score=score, reasons=reasons, recommended_actions=actions, evidence=payload.model_dump())
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return {"alert_id": str(alert.id), "score": score, "reasons": reasons, "recommended_actions": actions}


@router.post("/ingest/chat")
def ingest_chat(payload: ChatIngestRequest, db: Session = Depends(get_db), _=Depends(require_roles([Role.ADMIN, Role.ANALYST]))) -> dict:
    score, severity, reasons, actions = score_chat(payload.model_dump())
    alert = Alert(module="anti-phishing", severity=severity, score=score, reasons=reasons, recommended_actions=actions, evidence=payload.model_dump())
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return {"alert_id": str(alert.id), "score": score, "reasons": reasons, "recommended_actions": actions}


@router.post("/ingest/sbom")
def ingest_sbom(payload: SbomIngestRequest, _=Depends(require_roles([Role.ADMIN, Role.ANALYST]))) -> dict:
    return {"accepted": True, "asset_id": payload.asset_id, "packages": len(payload.packages)}


@router.post("/ingest/scan")
def ingest_scan(payload: ScanIngestRequest, _=Depends(require_roles([Role.ADMIN, Role.ANALYST]))) -> dict:
    return {"accepted": True, "asset_id": payload.asset_id, "findings": len(payload.findings)}


@router.post("/requests/high-risk")
def high_risk_request(payload: HighRiskRequest, db: Session = Depends(get_db), _=Depends(require_roles([Role.ADMIN, Role.ANALYST]))) -> dict:
    s = _get_or_create_settings(db)
    decision = evaluate_step_up(payload.amount, s.step_up_threshold)
    db.add(AuditLog(event_type="high_risk_request", user_id=payload.user_id, details={**payload.model_dump(), **decision}))
    db.commit()
    return decision


@router.post("/ingest/events")
def ingest_events(payload: EventIngestRequest, db: Session = Depends(get_db), _=Depends(require_roles([Role.ADMIN, Role.ANALYST]))) -> dict:
    score, severity, reasons, extra = detect_recon(payload.events)
    alert = Alert(
        module="recon-lateral-detection",
        severity=severity,
        score=score,
        reasons=reasons,
        recommended_actions=["Review IAM changes", "Temporarily enforce MFA", "Investigate suspicious hosts"],
        evidence={"events": payload.events, **extra},
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return {"alert_id": str(alert.id), "score": score, "reasons": reasons, "metadata": extra}


@router.post("/ingest/telemetry")
def ingest_telemetry(payload: TelemetryIngestRequest, db: Session = Depends(get_db), _=Depends(require_roles([Role.ADMIN, Role.ANALYST]))) -> dict:
    score, severity, reasons, playbooks, ticket = detect_malware(payload.model_dump())
    alert = Alert(module="adaptive-malware-defense", severity=severity, score=score, reasons=reasons, recommended_actions=playbooks, evidence={**payload.model_dump(), "ticket": ticket})
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return {"alert_id": str(alert.id), "score": score, "playbooks": playbooks, "ticket": ticket}


@router.post("/agent/submit")
def submit_agent(
    payload: AgentSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([Role.ADMIN, Role.ANALYST, Role.READ_ONLY])),
) -> dict:
    s = _get_or_create_settings(db)
    result = evaluate_agent_request(
        prompt=payload.prompt,
        tool_name=payload.tool_name,
        tool_args=payload.tool_args,
        allow_tools=s.allow_tools,
        risk_threshold=s.gateway_risk_threshold,
        role=current_user.role.value,
    )
    log = AgentGatewayLog(
        user_id=current_user.id,
        prompt_hash=result["prompt_hash"],
        tool_name=payload.tool_name,
        tool_args=payload.tool_args,
        decision=result["decision"],
        reasons=result["reasons"],
    )
    db.add(log)
    db.commit()
    return {"decision": result["decision"], "reasons": result["reasons"], "risk_score": result["risk_score"]}
