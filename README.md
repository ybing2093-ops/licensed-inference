# Licensed Inference — companion repo (v0.1)

This repository provides an **executable instance** (reference skeleton) of the theory developed in the author's Structural Gaps papers:
- endpoint/path gaps & endpoint sufficiency diagnostics
- protocol-level licensing: `LICENSED / NOT_LICENSED / UNDEFINED`
- inference-time gating actions (refine / escalate / abstain)

**Scope:** This repo is **not** presented as a standalone method, benchmark, or empirical claim.
It is an implementation track + evaluation harness intended to make the theory’s predicted failure signatures **testable and reproducible**.

## What you get (v0.1)
- `SPEC.md`: module interface, state machine, tensor-level contracts
- `EVAL.md`: reporting protocol (risk–coverage, calibration, compute, escalation efficiency)
- `THEORY_MAP.md`: theory → observables → how this repo instantiates them
- `community_results/`: template for third-party result submissions (optional)

## References
Project entry: https://ybing2093-ops.github.io/  
ORCID: https://orcid.org/0009-0008-4692-4408  

Papers:
1) Endpoint-Path Gaps QED — DOI: https://doi.org/10.5281/zenodo.18414030  
2) Psi-Delta Structural Gaps — DOI: https://doi.org/10.5281/zenodo.18456597  
3) Why Hierarchical Attention Works — DOI: https://doi.org/10.5281/zenodo.18810251  

## Citation
Please cite the theory papers above in addition to this software metadata (`CITATION.cff`).
