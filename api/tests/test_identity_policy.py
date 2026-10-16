from app.services.identity_policy import evaluate_step_up


def test_step_up_required_on_high_amount() -> None:
    decision = evaluate_step_up(amount=10000, threshold=70)
    assert decision["step_up_required"] is True
    assert "webauthn_mock_required" in decision["controls"]
