from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np

from .config import Action, SelfCheckConfig, Status
from .features import LogitsStats


@dataclass(frozen=True)
class SelfCheckResult:
    status: Status
    action: Action
    license_score: float
    meta: Dict


class SelfCheckController:
    """
    Minimal v0.1 controller.
    This does NOT claim empirical performance; it defines an executable status/action interface.
    """

    def __init__(self, cfg: SelfCheckConfig):
        self.cfg = cfg

    def license_score_from_stats(self, s: LogitsStats) -> float:
        """
        A deterministic placeholder mapping (monotone in margin, inverse in entropy).
        This is intentionally simple: the point is to expose a runnable interface.
        """
        # Normalize roughly: entropy in [0, log V], margin in [0,1]
        # Combine into [0,1] by a squashing function.
        raw = 2.5 * s.margin - 0.7 * s.entropy + 1.0
        score = 1.0 / (1.0 + np.exp(-raw))
        return float(np.clip(score, 0.0, 1.0))

    def infer(self, stats: LogitsStats, tool_available: bool = False) -> SelfCheckResult:
        # Protocol gate
        if self.cfg.verifier_required and not self.cfg.verifier_available:
            status: Status = "UNDEFINED"
            action: Action = "CALL_TOOL" if tool_available else "ABSTAIN"
            return SelfCheckResult(status=status, action=action, license_score=0.0, meta={"reason": "verifier_gate"})

        score = self.license_score_from_stats(stats)

        if score >= self.cfg.thresholds.tau_answer:
            return SelfCheckResult(
                status="LICENSED",
                action="ANSWER_NOW",
                license_score=score,
                meta={"rule": "score>=tau_answer"},
            )

        return SelfCheckResult(
            status="NOT_LICENSED",
            action="INCREASE_BUDGET" if tool_available else "ABSTAIN",
            license_score=score,
            meta={"rule": "score<tau_answer"},
        )
