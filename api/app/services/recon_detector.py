from datetime import datetime


def detect_recon(events: list[dict]) -> tuple[int, str, list[str], dict]:
    score = 0
    reasons: list[str] = []
    mitre: list[str] = []

    login_events = [e for e in events if e.get("event_type") == "login"]
    if len(login_events) >= 2:
        first, second = login_events[0], login_events[1]
        try:
            t1 = datetime.fromisoformat(first["timestamp"].replace("Z", "+00:00"))
            t2 = datetime.fromisoformat(second["timestamp"].replace("Z", "+00:00"))
            if first.get("country") != second.get("country") and (t2 - t1).total_seconds() < 7200:
                score += 35
                reasons.append("Impossible travel detected")
                mitre.append("T1078")
        except Exception:
            pass

    if any(e.get("event_type") == "admin_grant" for e in events):
        score += 25
        reasons.append("New admin privilege grant")
        mitre.append("T1098")

    enum_events = [e for e in events if e.get("event_type") == "directory_query"]
    if len(enum_events) > 20:
        score += 20
        reasons.append("Directory enumeration spike")
        mitre.append("T1087")

    if any(e.get("event_type") in {"rdp_attempt", "smb_attempt"} for e in events):
        score += 20
        reasons.append("Unusual RDP/SMB lateral attempt")
        mitre.append("T1021")

    severity = "critical" if score >= 85 else "high" if score >= 65 else "med" if score >= 45 else "low"
    return min(100, score), severity, reasons, {"mitre_techniques": sorted(set(mitre))}
