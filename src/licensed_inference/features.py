from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class LogitsStats:
    entropy: float
    margin: float
    topk_mass: float


def _softmax(x: np.ndarray) -> np.ndarray:
    x = x - np.max(x)
    e = np.exp(x)
    return e / np.sum(e)


def compute_logits_stats(logits: np.ndarray, topk_k: int = 10) -> LogitsStats:
    """
    logits: [V] for a single example.
    """
    p = _softmax(logits.astype(np.float64))
    eps = 1e-12

    entropy = float(-np.sum(p * np.log(p + eps)))

    # margin = top1 - top2
    top2 = np.partition(p, -2)[-2:]
    top1 = float(np.max(top2))
    top2nd = float(np.min(top2))
    margin = top1 - top2nd

    # top-k mass
    k = min(topk_k, p.shape[0])
    topk = np.partition(p, -k)[-k:]
    topk_mass = float(np.sum(topk))

    return LogitsStats(entropy=entropy, margin=margin, topk_mass=topk_mass)
