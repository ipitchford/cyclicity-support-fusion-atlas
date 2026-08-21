#!/usr/bin/env python3
"""Negative controls for the benchmark-to-experiment application programme."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from decomposition_fusion import analyse_decompositions  # noqa: E402
from verify_degree32_receipt import canonical_hash, verify  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def require_raises(action, fragment: str) -> None:
    try:
        action()
    except Exception as error:
        require(fragment in str(error), f"unexpected error: {error}")
        return
    raise RuntimeError(f"expected failure containing: {fragment}")


def run(argv: list[str], expected: int) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True, check=False)
    require(
        completed.returncode == expected,
        f"unexpected exit {completed.returncode} for {argv}: {completed.stdout}\n{completed.stderr}",
    )
    return completed


def epob_submission(answer_key: dict) -> dict:
    return {
        "schema": "epob1-submission-v1",
        "system": {"name": "frozen-answer-key-control", "version": "1", "environment": "test"},
        "cases": [
            {
                key: value
                for key, value in case.items()
                if key in {"id", "order", "support", "operator_coefficients_low_to_high"}
            }
            for case in answer_key["cases"]
        ],
    }


def main() -> None:
    python = sys.executable
    with tempfile.TemporaryDirectory(prefix="application-tests-") as tmp_name:
        tmp = Path(tmp_name)

        answers = json.loads((ROOT / "benchmarks" / "epob1_answer_key.json").read_text())
        correct_submission = tmp / "epob-correct.json"
        correct_submission.write_text(json.dumps(epob_submission(answers)))
        run([python, "tools/verify_epob1_submission.py", str(correct_submission)], 0)

        corrupted = epob_submission(answers)
        corrupted["cases"][0]["operator_coefficients_low_to_high"][0] = "0"
        corrupted_submission = tmp / "epob-corrupted.json"
        corrupted_submission.write_text(json.dumps(corrupted))
        failed = run([python, "tools/verify_epob1_submission.py", str(corrupted_submission)], 1)
        require("incomplete-or-mismatch" in failed.stdout, "EPOB mutation was not diagnosed")

        require_raises(
            lambda: analyse_decompositions(
                "(x**4+x)**3",
                [{"name": "wrong", "factors_outer_to_inner": ["x**3", "x**4+2*x"]}],
            ),
            "does not compose",
        )

        replay_answers = json.loads((ROOT / "challenge" / "answer_key.json").read_text())
        replay_answers["cases"][0]["rank"] = 2
        corrupted_replay_key = tmp / "replay-corrupted.json"
        corrupted_replay_key.write_text(json.dumps(replay_answers))
        failed = run([
            python,
            "challenge/reference_fraction_replay.py",
            "--answer-key",
            str(corrupted_replay_key),
            "--output",
            str(tmp / "should-not-pass.json"),
        ], 1)
        require("challenge mismatch" in failed.stderr, "Fraction mutation was not diagnosed")

        paths = {
            "preregistration_path": ROOT / "experiments" / "degree32_preregistration.json",
            "lock_path": ROOT / "experiments" / "degree32_preregistration_lock.json",
            "runner_path": ROOT / "experiments" / "degree32_quartic_lift.py",
            "result_path": ROOT / "receipts" / "degree32_quartic_lift_result.json",
        }
        verified = verify(**paths)
        require(verified["adjudication"] == "confirmed", "sealed degree-32 receipt did not verify")

        tampered = deepcopy(verified)
        tampered["records"][0]["empty_after_gamma_saturation"] = False
        unhashed = dict(tampered)
        unhashed.pop("result_sha256")
        tampered["result_sha256"] = canonical_hash(unhashed)
        tampered_path = tmp / "degree32-tampered.json"
        tampered_path.write_text(json.dumps(tampered))
        tampered_paths = dict(paths)
        tampered_paths["result_path"] = tampered_path
        require_raises(lambda: verify(**tampered_paths), "nonempty saturated locus")

    print(
        "application-programme tests passed: valid EPOB submission, operator mutation, "
        "invalid decomposition, replay mutation, sealed result and forged-result rejection"
    )


if __name__ == "__main__":
    main()
