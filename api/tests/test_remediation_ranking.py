from app.services.vuln_prioritizer import rank_remediation


def test_remediation_prioritization() -> None:
    ranked = rank_remediation(
        [
            {
                "cve": "CVE-A",
                "cvss": 9.8,
                "criticality": "high",
                "internet_exposed": True,
                "exploit_known": True,
                "patch_available": True,
                "asset_name": "Asset1",
            },
            {
                "cve": "CVE-B",
                "cvss": 6.0,
                "criticality": "low",
                "internet_exposed": False,
                "exploit_known": False,
                "patch_available": True,
                "asset_name": "Asset2",
            },
        ]
    )
    assert ranked[0]["cve"] == "CVE-A"
    assert ranked[0]["priority_score"] > ranked[1]["priority_score"]
