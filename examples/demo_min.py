import numpy as np

from licensed_inference.config import SelfCheckConfig, Thresholds
from licensed_inference.controller import SelfCheckController
from licensed_inference.features import compute_logits_stats
from licensed_inference.logging import write_jsonl


def main():
    rng = np.random.default_rng(0)

    cfg = SelfCheckConfig(thresholds=Thresholds(tau_answer=0.85))
    ctrl = SelfCheckController(cfg)

    prompts = [
        "Compute 19+23",
        "Write a python add(a,b)",
        "Explain in one sentence",
    ]

    results = []
    ids = []
    for i, p in enumerate(prompts):
        # Fake logits for demo: this repo provides an executable interface, not empirical claims.
        logits = rng.standard_normal(1000).astype(np.float32)  # pretend vocab size
        stats = compute_logits_stats(logits, topk_k=10)
        r = ctrl.infer(stats, tool_available=False)
        print("=" * 80)
        print("PROMPT:", p)
        print("STATUS:", r.status, "ACTION:", r.action, "license_score:", round(r.license_score, 4))
        print("META:", r.meta)
        results.append(r)
        ids.append(f"ex{i}")

    write_jsonl("demo_logs.jsonl", ids, results)
    print("\nWrote demo_logs.jsonl (ok=na). You can now run scripts/eval_risk_coverage.py once ok labels exist.")


if __name__ == "__main__":
    main()
