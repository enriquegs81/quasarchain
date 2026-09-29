# Academic Release Brief

## Title

Quantum Experiment Passports for Reproducible Bell-State Simulations

## Status

Educational prototype and technical study. This brief describes a local
release candidate; it is not a peer-reviewed publication or a hardware result.

## Abstract

This project studies whether a cryptographically signed experiment record can
improve the provenance and reproducibility of small quantum-computing
workflows. The prototype prepares an ideal two-qubit Bell state, records the
circuit, execution parameters, software environment, and observed counts, and
signs the resulting passport with Ed25519. It verifies the circuit hash and
checks that outcome counts sum to the declared number of shots.

The same logical circuit is also executed with Qiskit 2.5.2. The two ideal
simulators agree on the nonzero outcome support (`00` and `11`) while producing
different framework-specific sample counts under the same numeric seed. A
separate Qiskit Aer 0.17.2 run adds a symmetric 5% readout-error model and
produces nonzero `01` and `10` outcomes. These observations illustrate why
reproducibility claims must specify software, backend, randomization, and noise
model rather than relying on a seed alone.

The project also includes a policy-gated agent workflow. An agent may propose a
local Bell experiment, but shot limits, backend restrictions, review decisions,
and human approval are evaluated before execution. The signed passport can link
the proposal to the gateway evidence hash.

## Evidence

- Full test suite: `24 passed`.
- Ideal standard-library simulator: `00: 546`, `11: 478`.
- Ideal Qiskit simulator: `00: 517`, `11: 507`.
- Qiskit Aer readout-noise simulation: `00: 456`, `01: 53`, `10: 50`, `11: 465`.
- Signed tampering test: `verified` becomes `invalid_signature` after a count is changed.
- Cross-framework criterion: same shot count and nonzero support.

## Scope and limitations

This work does not claim a Bell-inequality violation, nonlocality, quantum
advantage, hardware equivalence, or scientific validity of an interpretation.
The noise experiment is a model-based simulation, not a measurement from a
quantum processing unit. The cryptographic signature establishes integrity and
key-based authorship of the record; it does not establish the truth of a
scientific claim.

## Reproduction

```text
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

See [quantum-experiment-passport.md](quantum-experiment-passport.md) for the
method and [CITATION.cff](../CITATION.cff) for citation metadata.

## Suggested citation

QuasarChain contributors. *Quantum Experiment Passport: Bell-State Laboratory*.
Educational software prototype, 2026. See `CITATION.cff` for machine-readable
citation metadata and the DOI once a version is archived.