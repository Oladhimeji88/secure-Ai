from app.services.phishing_detector import score_email


def test_phishing_score_increases_on_failed_auth() -> None:
    score, _, reasons, _ = score_email(
        {
            "sender": "ceo@paypaI-secure.com",
            "display_name": "CEO Office",
            "subject": "Urgent action now",
            "body": "wire now",
            "spf_pass": False,
            "dkim_pass": False,
            "dmarc_pass": False,
            "urls": ["http://xn--evil.example/login"],
        }
    )
    assert score > 60
    assert any("DMARC" in r for r in reasons)
