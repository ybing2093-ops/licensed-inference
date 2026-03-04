````markdown
# Licensed Inference — companion repo (v0.1)

This repository provides an **executable instance** (reference skeleton) of the theory developed in the author's *Structural Gaps* papers.  
Its purpose is to make the theory’s predicted **failure signatures** *testable and reproducible* under an explicit protocol.

**Core objects**
- Endpoint/path gaps & endpoint sufficiency diagnostics
- Protocol-level licensing: `LICENSED / NOT_LICENSED / UNDEFINED`
- Inference-time gating actions: `ANSWER_NOW / REFINE_ENDPOINT / INCREASE_BUDGET / CALL_TOOL / ABSTAIN`

**Scope (important)**
- This repo is **not** presented as a standalone method, benchmark, or empirical claim.
- It is an implementation track + evaluation harness intended to anchor discussion at the level of **protocol-defined sufficiency** rather than narrative “confidence” or “self-awareness”.

---

## Quickstart (minimal runnable instance)

This repo includes a minimal runnable demo that exercises the status/action interface and produces logs.

```bash
pip install -e .
python examples/demo_min.py
python scripts/eval_risk_coverage.py --jsonl demo_logs.jsonl
````

Notes:

* The demo writes `demo_logs.jsonl` with `ok=na`.
  Risk–Coverage is **not defined** unless you provide verifier-labeled `ok∈{0,1}` (see `EVAL.md`).
* The demo is intentionally a **reference skeleton** (executable interface), not an empirical report.

---

## What you get (v0.1)

**Documents**

* `SPEC.md` — module interface, state machine, and reporting-level semantics
* `EVAL.md` — evaluation/reporting protocol (risk–coverage, calibration, compute, escalation efficiency)
* `THEORY_MAP.md` — theory → observable signatures → how this repo instantiates them
* `DISCLAIMER.md` — prevents narrative drift (this is not “consciousness” claims)
* `CITATION.cff` — citation metadata (please cite theory papers as well)

**Code (minimal executable interface)**

* `src/licensed_inference/` — config, features, controller, logging
* `examples/` — runnable demo producing JSONL logs
* `scripts/` — evaluation helpers

**Community**

* `community_results/` — template for third-party result submissions

---

## How to interpret statuses and actions

This repo treats licensing as a **protocol-level status** under a declared evaluation gate `V`
(domain, verifier availability, thresholds/resolution).

**Statuses**

* `LICENSED`: endpoint information is treated as sufficient at reporting resolution
* `NOT_LICENSED`: endpoint information is treated as insufficient; escalation is recommended
* `UNDEFINED`: protocol gate conditions are not satisfied (e.g., required verifier unavailable)

**Actions**

* `ANSWER_NOW`: respond normally under the protocol
* `REFINE_ENDPOINT`: increase endpoint resolution/capacity (implementation-dependent)
* `INCREASE_BUDGET`: allocate more compute (implementation-dependent)
* `CALL_TOOL`: invoke verifier/retriever/solver if allowed/available (implementation-dependent)
* `ABSTAIN`: do not answer under current protocol conditions

See `SPEC.md` for the precise state machine and contract.

---

## Providing verifier labels (to make Risk–Coverage meaningful)

Risk–Coverage requires `ok∈{0,1}` defined by an external verifier appropriate to your domain, e.g.:

* unit tests for code-generation tasks
* solver/prover checks for symbolic tasks
* explicitly defined claim-checking policy for fact QA

This repo deliberately refuses to “fake” metrics without a verifier gate.
See `EVAL.md` for the required reporting items and JSONL schema.

---

## Repository philosophy (anti-misread framing)

This repo exists to prevent a common failure mode in reception:
treating a structural theory as a small “confidence trick”.

* The **theory** provides structural claims and predicted signatures (see the papers + `THEORY_MAP.md`).
* The **repo** provides an executable interface + evaluation harness so those signatures can be tested.
* Implementations may vary; what matters is protocol disclosure and reproducible reporting (`EVAL.md`).

---

## References

Project entry:

* [https://ybing2093-ops.github.io/](https://ybing2093-ops.github.io/)

ORCID:

* [https://orcid.org/0009-0008-4692-4408](https://orcid.org/0009-0008-4692-4408)

Papers:

1. *Endpoint-Path Gaps QED* — DOI: [https://doi.org/10.5281/zenodo.18414030](https://doi.org/10.5281/zenodo.18414030)
2. *Psi-Delta Structural Gaps* — DOI: [https://doi.org/10.5281/zenodo.18456597](https://doi.org/10.5281/zenodo.18456597)
3. *Why Hierarchical Attention Works* — DOI: [https://doi.org/10.5281/zenodo.18810251](https://doi.org/10.5281/zenodo.18810251)

---

## Citation

If you use this repository, please cite:

* the theory papers above (preferred), and
* this software metadata (`CITATION.cff`).

---

## Contributing / Community results (optional)

If you run experiments, please submit results using:

* `community_results/TEMPLATE.md`

Include:

* model name + revision/commit
* domain + dataset + verifier definition
* gating configuration + thresholds
* raw JSONL logs + plots/CSV generated under `EVAL.md`

