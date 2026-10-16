def evaluate_step_up(amount: float, threshold: int) -> dict:
    risk_score = min(100, int(amount / 100))
    required = risk_score >= threshold
    controls = []
    if required:
        controls = [
            "portal_approval_required",
            "callback_to_known_number",
            "webauthn_mock_required",
        ]
    return {
        "risk_score": risk_score,
        "step_up_required": required,
        "controls": controls,
    }
