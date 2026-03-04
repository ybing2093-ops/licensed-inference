from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Status = Literal["LICENSED", "NOT_LICENSED", "UNDEFINED"]
Action = Literal["ANSWER_NOW", "REFINE_ENDPOINT", "INCREASE_BUDGET", "CALL_TOOL", "ABSTAIN"]


@dataclass(frozen=True)
class Thresholds:
    tau_answer: float = 0.85


@dataclass(frozen=True)
class SelfCheckConfig:
    thresholds: Thresholds = Thresholds()
    # If a protocol requires a verifier but it is not available, status must be UNDEFINED.
    verifier_required: bool = False
    verifier_available: bool = False
