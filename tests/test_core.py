import pytest

from groundcheck import check_answer


def test_matches_claim_to_best_evidence_and_flags_unsupported_claim():
    report = check_answer(
        "The library opened in 1998. It has a rooftop swimming pool.",
        ["The public library opened in 1998 and serves the whole city."],
        threshold=0.2,
    )

    assert report.supported == 1
    assert report.needs_review == 1
    assert report.claims[0].status == "supported"
    assert report.claims[0].evidence == (
        "The public library opened in 1998 and serves the whole city."
    )
    assert report.claims[1].status == "needs_review"
    assert report.claims[1].evidence is None


def test_empty_context_flags_claim_for_review():
    report = check_answer("A claim without evidence.", [])

    assert report.needs_review == 1
    assert report.claims[0].score == 0


@pytest.mark.parametrize("threshold", [-0.1, 1.1])
def test_rejects_threshold_outside_unit_interval(threshold):
    with pytest.raises(ValueError, match="threshold"):
        check_answer("A claim.", [], threshold=threshold)


def test_empty_answer_produces_empty_report():
    report = check_answer("  ", ["some context"])

    assert report.to_dict() == {"supported": 0, "needs_review": 0, "claims": []}
