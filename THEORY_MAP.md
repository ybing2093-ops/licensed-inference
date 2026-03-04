# THEORY_MAP — from structural claims to observable signatures (v0.1)

This repo exists to make the theory's **structural claims** empirically addressable via **observable signatures** under an explicit protocol.

## Structural claims (informal summary)
1) Endpoint information can be insufficient: compressing a process into an endpoint can leave **residual distinguishability**.
2) Such insufficiency is **protocol-relative**: claims of “equality/correctness” are reporting-level under a declared resolution.
3) A correct system behavior is to output **UNDEFINED / NOT_LICENSED** when protocol gates fail or endpoint sufficiency fails, rather than forcing confident answers.

## Observable signatures (what to measure)
- Risk–Coverage improvement under licensing thresholds
- Calibration of `license_score` against verifier-defined correctness
- Escalation efficiency: refinement/tooling reduces risk for NOT_LICENSED cases
- (Optional) monotonicity under endpoint refinement: refined endpoints reduce residual instability

## This repo’s instantiation
- `LICENSED/NOT_LICENSED/UNDEFINED` is treated as protocol-level status.
- Implementations may vary (different probes/features/refinement), but results must be reported per `EVAL.md`.

## Not a standalone method
The code and specs here are an executable instance of the theory, not a claim of a new “confidence trick” detached from the theoretical framework.
