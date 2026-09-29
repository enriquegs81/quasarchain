# Quantum Experiment Passport: Bell-State Laboratory

## Abstract

This document describes an educational prototype for recording the provenance
and integrity of a local quantum experiment. The experiment prepares an ideal
Bell state, collects 1,024 measurement shots, and signs a receipt using Ed25519.

The proposed contribution is not a new quantum algorithm. It is a small,
verifiable evidence format that separates the circuit, parameters, observed
result, and interpretation.

## Research Question

Can a signed receipt verifiably describe a specific Bell circuit, its execution
parameters, and its observed results?

## Falsifiable Hypothesis

If the receipt signs the serialized circuit, execution parameters, and counts,
then any subsequent modification of those fields must cause verification to
return `invalid_signature`.

## Method

- Initial state: `|00>`.
- Circuit: `H(0)`, followed by `CNOT(0, 1)` and measurement.
- Simulator: a state-vector simulator implemented with the Python standard library.
- Shots: `1024`.
- Random seed: `7`.
- Circuit integrity: SHA-256 of canonical JSON.
- Receipt signature: Ed25519.
- Runtime provenance: package version, Python implementation and version,
  simulator identifier, and source path.
- Implementation: `src/quasar_verifier/quantum_lab.py`.

IBM's documentation uses the same H-on-qubit-0 and CNOT-with-control-0
pattern to prepare a Bell state:

[IBM Quantum: Run your first circuit](https://quantum.cloud.ibm.com/docs/guides/hello-world)

## Observed Result

The reproducible execution with the parameters above produced:

```text
00: 546
01: 0
10: 0
11: 478
```

The observed circuit hash was:

```text
a29f06d219bea1cc615bdf71a457573e047fefb86ca0081cb07163e5aabd9c80
```

Only `00` and `11` occurred in this ideal simulator. This is an observation
about the implemented model, not a claim about real quantum hardware.

## Integrity Test

The test modifies the `00` count after the receipt has been signed:

```python
passport["experiment"]["counts"]["00"] += 1
```

Verification returned:

```text
before: verified
after modifying counts: invalid_signature
```

The automated test is in
[tests/test_quantum_lab.py](../tests/test_quantum_lab.py). Reproduce it with:

```text
python -m pip install -r requirements-dev.txt
python -m pytest tests/test_quantum_lab.py -q
```

## What This Demonstrates

- The circuit and result can be represented in a portable receipt.
- The receipt detects subsequent modifications to signed data.
- The verifier checks that the circuit hash matches the serialized circuit and
  that the outcome counts sum to the declared shot count.
- Another person can repeat the execution under the same parameters.
- A Trust Layer can treat an experiment as a unit with identity, provenance,
  and integrity.

## What This Does Not Demonstrate

- It does not demonstrate a violation of a Bell inequality.
- It does not demonstrate nonlocality or a new physical phenomenon.
- It does not establish that the result will match quantum hardware.
- It does not establish that the interpretation of the result is correct.
- A signature authenticates a record produced by a key; it does not make a
  scientific claim true.

## Reproducibility and Threats to Validity

The current receipt is reproducible for the simulator and sampling algorithm
included in this repository. A Qiskit 2.5.2 comparison is now available through
`src/quasar_verifier/qiskit_lab.py`. With 1,024 shots and seed `7`, Qiskit
produced `00: 517` and `11: 507`, while the standard-library simulator produced
`00: 546` and `11: 478`.

The invariant result is the nonzero support: both simulators produced only
`00` and `11`. The exact counts differ because a seed does not define a
cross-framework random-number sequence. Exact-count comparison would therefore
be an invalid reproducibility criterion unless the sampling algorithm is also
standardized.

The repository also includes a Qiskit Aer experiment with a symmetric 5%
independent readout error. It produced `00: 456`, `01: 53`, `10: 50`, and
`11: 465` for the same 1,024 shots and seed. The newly observed `01` and `10`
outcomes illustrate degraded measurement correlation in this model. This is a
readout-noise simulation, not a complete model of hardware decoherence.

## Differential Replication

The repository also runs the ideal Bell circuit in two independent
implementations: the standard-library simulator and Qiskit's `BasicSimulator`.
The signed passport can include both outputs and a comparison report. The
report expects agreement on shot count and nonzero outcome support, while
allowing framework-specific sample counts. This makes the reproducibility claim
more meaningful than requiring identical pseudo-random sequences.

Important threats to validity include version changes, bit-ordering
conventions, simulator defects, compromised private keys, and conflating the
integrity of a record with the scientific validity of its interpretation.

## Defensible Academic Claim

> We propose and demonstrate a local Quantum Experiment Passport format that
> records the provenance and integrity of a reproducible Bell-state experiment
> and detects subsequent modifications using hashing and Ed25519 signatures.

This claim should be presented as an educational prototype for experimental
infrastructure, not as a result in experimental quantum physics.

## Next Evaluation Steps

1. Compare serialization and bit ordering across additional framework versions.
2. Add gate and thermal-relaxation noise models with documented assumptions.
3. Freeze the repository in a release and archive it with a Zenodo DOI.
4. Request review from one quantum-computing practitioner and one researcher
   experienced in reproducibility or data provenance.

## Agentic Extension

The repository also includes a controlled agent workflow in
`src/quasar_verifier/agentic_quantum.py`. The agent can propose a Bell
experiment, but the workflow requires policy evaluation before execution. A
review decision requires a human approval identifier, and the signed passport
links the proposal to the gateway evidence hash. Proposals that exceed the shot
limit or request an unsupported backend are rejected before execution.
