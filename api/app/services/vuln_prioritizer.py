CRITICALITY_WEIGHT = {"low": 0.8, "med": 1.0, "high": 1.25}


def rank_remediation(items: list[dict]) -> list[dict]:
    ranked: list[dict] = []
    for item in items:
        cvss = float(item.get("cvss", 0.0))
        crit = item.get("criticality", "med")
        exposed_bonus = 1.15 if item.get("internet_exposed") else 1.0
        exploit_bonus = 1.2 if item.get("exploit_known") else 1.0
        patch_bonus = 0.9 if item.get("patch_available") else 1.05
        score = cvss * 10 * CRITICALITY_WEIGHT.get(crit, 1.0) * exposed_bonus * exploit_bonus * patch_bonus
        priority = round(min(100.0, score), 2)
        ranked.append(
            {
                "cve": item.get("cve"),
                "asset": item.get("asset_name", "unknown"),
                "priority_score": priority,
                "sla_suggestion": "24h" if priority >= 85 else "72h" if priority >= 65 else "7d",
                "patch_available": bool(item.get("patch_available")),
            }
        )
    ranked.sort(key=lambda x: x["priority_score"], reverse=True)
    return ranked
