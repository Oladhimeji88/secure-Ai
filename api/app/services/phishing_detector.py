import re
from urllib.parse import urlparse

EXEC_NAMES = {"ceo office", "chief executive", "cfo", "finance director"}
URGENCY_MARKERS = {"urgent", "immediately", "wire", "asap", "now", "10 minutes"}


def _severity(score: int) -> str:
    if score >= 85:
        return "critical"
    if score >= 70:
        return "high"
    if score >= 50:
        return "med"
    return "low"


def score_email(payload: dict) -> tuple[int, str, list[str], list[str]]:
    score = 0
    reasons: list[str] = []

    if not payload.get("spf_pass", True):
        score += 15
        reasons.append("SPF validation failed")
    if not payload.get("dkim_pass", True):
        score += 15
        reasons.append("DKIM validation failed")
    if not payload.get("dmarc_pass", True):
        score += 20
        reasons.append("DMARC validation failed")

    sender = payload.get("sender", "")
    if any(ch in sender for ch in ["I", "1", "0"]):
        score += 10
        reasons.append("Potential lookalike sender domain")

    text = f"{payload.get('subject', '')} {payload.get('body', '')}".lower()
    matched = [m for m in URGENCY_MARKERS if m in text]
    if matched:
        score += min(20, len(matched) * 6)
        reasons.append("Urgency language detected")

    display_name = payload.get("display_name", "").strip().lower()
    if display_name in EXEC_NAMES:
        score += 10
        reasons.append("Executive impersonation indicator")

    for url in payload.get("urls", []):
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        if "xn--" in host:
            score += 12
            reasons.append("Punycode URL detected")
        if re.search(r"paypa[i1l]", host):
            score += 10
            reasons.append("Domain mismatch pattern detected")

    score = min(100, score)
    actions = [
        "Show phishing warning banner",
        "Quarantine message pending analyst review",
        "Require out-of-band confirmation for payment requests",
    ]
    return score, _severity(score), reasons, actions


def score_chat(payload: dict) -> tuple[int, str, list[str], list[str]]:
    msg = payload.get("message", "").lower()
    score = 10
    reasons: list[str] = []
    rules = {
        "ignore all previous": 30,
        "send me": 15,
        "secret": 25,
        "credential": 25,
        "password": 20,
    }
    for token, weight in rules.items():
        if token in msg:
            score += weight
            reasons.append(f"Suspicious social engineering phrase: {token}")
    score = min(100, score)
    actions = [
        "Warn user in chat UI",
        "Escalate conversation to security analyst",
        "Block sensitive data sharing until verified",
    ]
    return score, _severity(score), reasons, actions
