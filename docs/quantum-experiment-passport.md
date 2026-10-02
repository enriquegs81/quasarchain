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

## Blockchain Decision

The Bell experiment does not require an on-chain transaction for its first
validation. The local hash and Ed25519 signature already test whether the
passport was altered and whether it was produced by the expected signing key.
Adding a blockchain at this stage would add an external dependency without
improving the quantum measurement or the simulator model.

Blockchain remains a separate optional extension for anchoring a digest. If
implemented, it should publish only a passport or circuit hash, experiment
identifier, protocol version, and anchoring timestamp. It should not publish
private keys, raw user data, prompts, or sensitive experiment results.

An on-chain anchor could show that a digest was recorded by a network at a
particular time. It could not prove that the circuit was physically executed,
that the simulator was correct, or that the scientific interpretation was true.

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

A separate Qiskit Aer run applies a depolarizing error of `p=0.01` after the
`H` and `CNOT` gates. It produced `00: 524`, `01: 3`, `10: 2`, and `11: 495`.
The count-based estimate of the Bell state's `ZZ` correlation is approximately
`0.990`, compared with the ideal value `1.0`. This is a gate-noise model, not a
calibration of a physical device.

## Readout Calibration

The next control experiment prepares each computational-basis state (`00`,
`01`, `10`, and `11`) and measures it under the same readout-noise model. The
four resulting count vectors estimate a confusion matrix. This calibration is
required before attributing Bell-correlation loss to gate noise, because a
measurement error can create the same `01` and `10` outcomes as an imperfect
state preparation.

Using the calibrated matrix on the 5% readout-noise Bell result changes the
estimated `ZZ` correlation from `0.799` to approximately `0.986`. The corrected
estimate includes a small negative value for one outcome (`-3.44` counts).
This is a statistical quasi-probability caused by finite-sample inversion; it
must not be reported as a literal negative count or silently clipped to zero.

The next analysis uses a two-factor sweep with readout errors `{0, 0.05}`,
depolarizing gate errors `{0, 0.01}`, three seeds, and Wilson 95% intervals for
the mismatch rate. This estimates stability across repeated simulations rather
than treating one seeded run as a complete statistical result.

A thermal-relaxation model is also available with explicit parameters
$T_1=50\,\mu s$, $T_2=70\,\mu s$, `50 ns` for `H`, and `300 ns` for `CNOT`.
It produced `00: 528`, `01: 3`, `10: 2`, and `11: 491`, corresponding to a
`ZZ` correlation of approximately `0.990`. These parameters are illustrative
and must be replaced by calibrated device data before making hardware claims.

A three-seed sweep with the same gate durations produced mean `ZZ` correlations
of `0.990` for `(T1, T2) = (50, 70) us`, `0.878` for `(5, 7) us`, and `0.632`
for `(1, 1.5) us`. The monotonic trend supports the model's qualitative
behavior, but it is not an experimental estimate of a device's coherence times.

The ideal Bell state is also measured in the `X` basis by applying `H` to both
qubits before measurement. Its parity estimates the `XX` correlation. The
thermal-relaxation model can be evaluated in both `Z` and `X` bases, allowing
population correlation and coherence correlation to be compared under the same
noise parameters.

For the illustrative thermal parameters above, the observed estimates were
`ZZ=0.990` and `XX=0.986` with 1,024 shots. These values are close in this
specific model and sample size; a larger study is required before interpreting
their difference.

The model-comparison sweep uses 4,096 shots and three seeds for ideal,
depolarizing, and thermal models in both bases. Its purpose is to test whether
the observables discriminate model behavior, not to select a model for a real
device without calibration data.

In the current illustrative sweep, depolarizing noise produced mean
correlations `ZZ=0.990` and `XX=0.960`, while thermal relaxation produced
`ZZ=0.895` and `XX=0.895`. This suggests that the pair of observables may carry
more model information than either observable alone, but the conclusion still
requires a parameter-matched study and uncertainty analysis.

The parameter-matched study used depolarizing `p=0.12` and thermal
`T1=5 us`, `T2=7 us`. With 4,096 shots and three seeds, depolarizing noise
produced mean `ZZ=0.882`, `XX=0.607`, while thermal relaxation produced
`ZZ=0.895`, `XX=0.895`. This is a candidate discriminator within the two
simulation models, not proof of a physical device or a unique physical cause.

Using the same 30 seeds for both models, the paired thermal-minus-depolarizing
difference was `0.0127` for `ZZ` (95% interval `[0.0099, 0.0156]`) and `0.2943`
for `XX` (95% interval `[0.2913, 0.2973]`). The intervals are model-based
simulation estimates and use a normal approximation; they are not evidence
about a physical backend.

## Real Backend Snapshot

On October 2, 2026, IBM Quantum Runtime reported the following snapshot for
`ibm_fez` (156 qubits). For the connected pair `[7, 17]`, the native `cz` gate
had error `0.002782` and duration `68 ns`. Qubit 7 reported
$T_1=129.0\,\mu s$, $T_2=40.9\,\mu s$, and readout error `0.01343`; qubit 17
reported $T_1=200.1\,\mu s$, $T_2=114.3\,\mu s$, and readout error `0.00415`.

This is a time-stamped calibration snapshot, not a permanent device property.
The values should parameterize a simulator and then be compared with a new
hardware execution under the same backend and qubit mapping.

A cross-backend control was also run on `ibm_kingston` using physical qubits
`[72,73]`. Its readout calibration and Bell job were combined under job
`davei0c92g1c7398oovg`. The raw correlations were `ZZ=0.854` and `XX=0.865`;
using the contemporaneous calibration gave `ZZ=0.978` and `XX=0.986`. This
comparison illustrates why raw hardware counts cannot be compared without
including the backend-specific calibration snapshot.

A third backend, `ibm_marrakesh`, was measured on the same physical mapping
`[72,73]` under job `daveiq04oijs73e7dmhg`. Its raw correlations were
`ZZ=0.932` and `XX=0.904`; calibration-based estimates were `ZZ=0.959` and
`XX=0.933`. These three snapshots demonstrate cross-backend variability, not a
permanent ranking of device quality.

The corresponding calibration snapshots reported mean readout errors of about
`0.0088` for `ibm_fez`, `0.0327` for `ibm_kingston`, and `0.0182` for
`ibm_marrakesh`. The Marrakesh pair also had notably shorter reported $T_2$
values (`16.96 us` and `35.13 us`). These are covariates consistent with the
observed raw differences, not causal proof from only three jobs.

The first hardware readout calibration used `ibm_fez`, physical qubits `[7,17]`,
and 256 shots for each computational-basis state. Job
`daveep5j371s73dmokt0` returned diagonal counts `249`, `246`, `250`, and `246`
out of `1024` total calibration shots. The aggregate observed readout error was
`33/1024 = 0.0322`. These raw counts are the experimental calibration record;
they should be used before interpreting the Bell counts.

The first Bell execution used the same backend and physical mapping. Job
`davef3s92g1c7398olj0` collected 1,024 shots in each basis and returned
`Z={00:537, 01:22, 10:15, 11:450}` and
`X={00:504, 01:19, 10:22, 11:479}`. The raw correlations were `ZZ=0.928` and
`XX=0.920`. Applying the earlier calibration gave `ZZ=0.993` and `XX=0.985`.
The corrected `X` distribution included an estimated `-0.968` counts for one
outcome; this is a quasi-probability from mitigation, not a physical count.

A second hardware job, `daveg8ql7guc73ceoikg`, repeated five circuits in each
measurement basis and recalibrated all four computational-basis states in the
same job. The raw means were `ZZ=0.936` (sample SD `0.0066`) and `XX=0.922`
(sample SD `0.0122`); readout mitigation gave `ZZ=0.991` and `XX=0.977`.
This provides initial same-snapshot repeatability, not long-term device
stability.

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
