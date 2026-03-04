
# SPEC — Licensed Inference Self-Check & Gating (v0.1)

## 1. Purpose

Implement an inference-time, low-overhead self-check module that reads model activations/logits and outputs:

- `STATUS ∈ {LICENSED, NOT_LICENSED, UNDEFINED}`
- `ACTION ∈ {ANSWER_NOW, REFINE_ENDPOINT, INCREASE_BUDGET, CALL_TOOL, ABSTAIN}`
- `license_score ∈ [0,1]` interpreted as calibrated `P(STATUS=LICENSED)` under a declared evaluation protocol.

This module is designed as an **architecture-level control path**, not as output-layer textual introspection.

## 2. Status semantics (reporting-level, thresholded)

Let `V` denote the declared protocol (domain gate, admissible interfaces/verifiers, divergence/metric family, and threshold `ε`).

- `LICENSED`: within protocol `V`, endpoint information is treated as sufficient at reporting resolution; `gap_score ≤ ε` (operationally approximated).
- `NOT_LICENSED`: within `V`, endpoint information is not sufficient at reporting resolution; escalation is recommended.
- `UNDEFINED`: protocol gate conditions are not satisfied (domain out-of-scope, verifier required but unavailable, etc.). The correct behavior is to abstain or request tools/inputs.

**Important:** `UNDEFINED` is not an error state; it is a protocol-correct output when `V` is missing required conditions.

## 3. Actions

- `ANSWER_NOW`: decode as usual.
- `REFINE_ENDPOINT`: increase endpoint resolution/capacity (e.g., more memory tokens, finer hierarchical summary).
- `INCREASE_BUDGET`: allocate more compute (e.g., more decoding steps, higher internal budget mode).
- `CALL_TOOL`: invoke external verifier/retriever/solver (implementation-dependent).
- `ABSTAIN`: return no answer / request more information.

v0.1 provides a hard-rule controller (deterministic mapping) and leaves tool calling to downstream integration.

## 4. Inputs & features

We assume a transformer model with:
- hidden states per layer: `H^ℓ ∈ R^{B×T×d}`
- final logits at last position: `logits ∈ R^{B×V}`

### 4.1 Required features
For each monitored layer `ℓ ∈ S`:
- `p_last^ℓ = H^ℓ[:, T-1, :] ∈ R^{B×d}`
- `p_mean^ℓ = mean_t H^ℓ[:, t, :] ∈ R^{B×d}`
- pooled: `p^ℓ = concat(p_last^ℓ, p_mean^ℓ) ∈ R^{B×2d}`

From final logits:
- `entropy ∈ R^{B×1}`
- `margin = top1 - top2 ∈ R^{B×1}`
- `topk_mass(k) ∈ R^{B×1}`

Optional external verifier signal (domain-dependent):
- `verifier ∈ {pass, fail, na}` one-hot: `R^{B×3}`

Final per-layer feature:
- `f^ℓ = concat(p^ℓ, entropy, margin, topk_mass, verifier_onehot, ...) ∈ R^{B×m}`

## 5. Heads & aggregation

### 5.1 Layerwise License Head (LLH)
For each monitored layer `ℓ`:
- input: `f^ℓ ∈ R^{B×m}`
- output: `z^ℓ ∈ R^{B×3}` corresponding to `[LICENSED, NOT_LICENSED, UNDEFINED]` logits.

LLH is a small MLP:
- `Linear(m→h) + GELU + Linear(h→3)` (h=256 by default)

### 5.2 Aggregator
- input: concatenated `Z = concat_ℓ z^ℓ ∈ R^{B×(3|S|)}` and optionally global stats
- output: `status_logits ∈ R^{B×3}`, `license_score = softmax(status_logits)[:, LICENSED]`

## 6. Controller policy (v0.1 hard rules)

Let:
- `s = license_score`
- thresholds: `τ_answer`, `τ_exit` (optional)

Rules:
1) If `STATUS=UNDEFINED` → `ACTION=ABSTAIN` (or `CALL_TOOL` if domain gate requires and tool is available)
2) Else if `STATUS=LICENSED` and `s ≥ τ_answer` → `ANSWER_NOW`
3) Else (`NOT_LICENSED` or low confidence):
   - If refine is available and refine_steps < max → `REFINE_ENDPOINT`
   - Else if increase-budget available → `INCREASE_BUDGET`
   - Else if tool available → `CALL_TOOL`
   - Else → `ABSTAIN`

## 7. Endpoint refinement interface

This repo defines a generic interface:
- `refine_endpoint(config, step)` → new config

Reference option (v0.1): memory tokens
- low: `M_low`
- high: `M_high`

Downstream implementations may replace this with hierarchical summary refinement.

## 8. Non-claims

This SPEC does not claim empirical gains by itself.
Empirical evaluation must follow `EVAL.md` with explicit model+domain disclosure.
