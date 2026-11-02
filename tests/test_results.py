"""Tests for the result model: statuses, findings, and roll-up semantics.

The roll-up rule is "worst status wins" with precedence
FAIL > ERROR > PASS > NOT_APPLICABLE. The key safety property: an ERROR can
never be hidden behind a PASS, because that would report an unreadable
resource as compliant.
"""

import dataclasses
import itertools

import pytest

from controlcheck.results import ControlResult, Finding, Status, rollup

PASS, FAIL, ERROR, NA = Status.PASS, Status.FAIL, Status.ERROR, Status.NOT_APPLICABLE


def make_finding(status: Status, resource_id: str = "sg-0abc") -> Finding:
    return Finding(
        resource_id=resource_id,
        resource_type="AWS::EC2::SecurityGroup",
        region="eu-west-1",
        status=status,
        observed="port 22 open to 0.0.0.0/0",
        expected="no ingress to 22 from the internet",
    )


# --- Status -----------------------------------------------------------------


def test_status_values_serialise_as_plain_strings() -> None:
    # Reports are JSON; statuses must serialise without custom encoders.
    assert Status.PASS == "PASS"  # noqa: S105 - status name, not a password
    assert Status.NOT_APPLICABLE == "NOT_APPLICABLE"
    assert {s.value for s in Status} == {"PASS", "FAIL", "ERROR", "NOT_APPLICABLE", "MANUAL"}


# --- rollup -----------------------------------------------------------------


@pytest.mark.parametrize(
    ("statuses", "expected"),
    [
        pytest.param([PASS] * 39 + [FAIL], FAIL, id="one-failure-fails-the-control"),
        pytest.param([PASS] * 39 + [ERROR], ERROR, id="error-is-never-hidden-behind-pass"),
        pytest.param([FAIL, ERROR], FAIL, id="proven-failure-outranks-error"),
        pytest.param([PASS, NA], PASS, id="pass-outranks-not-applicable"),
        pytest.param([NA, NA], NA, id="all-not-applicable"),
        pytest.param([], NA, id="no-findings-is-not-applicable"),
        pytest.param([PASS], PASS, id="single-pass"),
        pytest.param([ERROR], ERROR, id="single-error"),
    ],
)
def test_rollup_worst_status_wins(statuses: list[Status], expected: Status) -> None:
    assert rollup(statuses) is expected


def test_rollup_is_independent_of_order() -> None:
    mixed = [PASS, NA, ERROR, FAIL]
    results = {rollup(p) for p in itertools.permutations(mixed)}
    assert results == {FAIL}


def test_rollup_accepts_a_one_shot_iterator() -> None:
    # Callers pass generators; rollup must not iterate its input twice.
    assert rollup(s for s in [PASS, ERROR]) is ERROR


def test_rollup_rejects_manual() -> None:
    # MANUAL is control-level only: there is nothing to roll up.
    with pytest.raises(ValueError, match="MANUAL"):
        rollup([PASS, Status.MANUAL])


# --- Finding ----------------------------------------------------------------


def test_finding_is_immutable() -> None:
    finding = make_finding(FAIL)
    with pytest.raises(dataclasses.FrozenInstanceError):
        finding.status = PASS  # type: ignore[misc]


def test_finding_cannot_be_manual() -> None:
    with pytest.raises(ValueError, match="MANUAL"):
        make_finding(Status.MANUAL)


# --- ControlResult ----------------------------------------------------------


def test_control_status_is_derived_from_findings() -> None:
    result = ControlResult(
        control_id="NET-03",
        findings=(make_finding(PASS, "sg-1"), make_finding(FAIL, "sg-2")),
    )
    assert result.status is FAIL


def test_control_with_no_findings_is_not_applicable() -> None:
    assert ControlResult(control_id="NET-03", findings=()).status is NA


def test_manual_control_reports_manual() -> None:
    assert ControlResult(control_id="IAM-07", findings=(), manual=True).status is Status.MANUAL


def test_manual_control_cannot_carry_findings() -> None:
    with pytest.raises(ValueError, match="manual"):
        ControlResult(control_id="IAM-07", findings=(make_finding(PASS),), manual=True)


def test_control_result_is_immutable() -> None:
    result = ControlResult(control_id="NET-03", findings=())
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.control_id = "NET-04"  # type: ignore[misc]
