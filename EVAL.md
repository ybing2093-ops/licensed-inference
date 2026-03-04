# EVAL — Reproducible Protocol (v0.1)

This document defines **what to measure** for licensed inference self-check & gating.

## 1. Required reporting items

Any result should report:
- model name + commit/hash (or HF revision)
- domain/task + dataset
- gating configuration (`monitor_layers`, thresholds, refinement options)
- verifier availability (pass/fail/na definition)

## 2. Core metrics

### 2.1 Risk–Coverage
Let the system decide whether to answer.
- Coverage: `C = (# answered) / (# total)`
- Risk: `R = (# wrong among answered) / (# answered)`

Plot `R` vs `C` by sweeping `τ_answer` (and/or using `license_score` bins).

**Acceptance signature (protocol-level):**
- For fixed coverage, gated answers should have lower risk than ungated baseline; or
- For fixed risk, gated system should achieve higher coverage.

### 2.2 Calibration
Let `s` be `license_score`, and `ok ∈ {0,1}` be correctness under the domain verifier.
Report at least one:
- Brier score: `E[(s - ok)^2]`
- ECE (Expected Calibration Error), with bins explicitly defined.

### 2.3 Escalation efficiency
If refinement/tool/budget escalation is implemented:
- Report delta risk after escalation for the subset escalated.
- Report incremental compute/time.

Example:
- `risk_before_refine`, `risk_after_refine`
- `avg_latency_before`, `avg_latency_after`

### 2.4 Compute reporting (minimum viable)
Report one:
- average generated tokens
- average forward passes
- average layers evaluated (if early-exit implemented)
- wall-clock latency (hardware disclosed)

## 3. Verifier definitions

Prefer domains with external correctness checks:
- code + unit tests
- symbolic constraints / solver checks
- fact QA with retrieval-based claim checking (explicitly define the checking policy)

If no verifier exists, report must clearly mark `ok=na` and treat risk–coverage as *not well-defined*.

## 4. Minimal JSONL schema for logs

Each example should log:
- `id`
- `status`
- `action`
- `license_score`
- `answered` (bool)
- `ok` (0/1/na)
- `latency_ms` (optional)
- `extra` (dict)

This repo writes JSONL in `licensed_inference.logging`.

## 5. Reproduction scripts

- `scripts/eval_risk_coverage.py`: build risk–coverage from JSONL
- `scripts/label_builder_stub.py`: scaffolding for offline labeling (multi-sampling / perturbations / verifiers)

Downstream results should attach:
- config file
- raw JSONL logs
- plot artifacts
