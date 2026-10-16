import hashlib
import re


def evaluate_agent_request(prompt: str, tool_name: str, tool_args: dict, allow_tools: list[str], risk_threshold: int, role: str) -> dict:
    reasons: list[str] = []
    risk = 0
    lower = prompt.lower()

    indicators = {
        r"ignore (all )?previous": 25,
        r"reveal .*secret": 30,
        r"exfiltrat": 35,
        r"override policy": 20,
        r"credential": 25,
        r"password": 20,
    }
    for pattern, weight in indicators.items():
        if re.search(pattern, lower):
            risk += weight
            reasons.append(f"Prompt injection indicator: {pattern}")

    if tool_name not in allow_tools:
        risk += 30
        reasons.append("Tool is not in allowlist")

    if role == "read-only" and tool_name in {"write_db", "update_policy", "delete_record"}:
        risk += 40
        reasons.append("Role not permitted for mutating tools")

    if len(str(tool_args)) > 2000:
        risk += 10
        reasons.append("Tool arguments exceed safe size threshold")

    decision = "block" if risk >= risk_threshold else "allow"
    prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    return {
        "risk_score": min(100, risk),
        "decision": decision,
        "reasons": reasons or ["No high-risk indicators"],
        "prompt_hash": prompt_hash,
    }
