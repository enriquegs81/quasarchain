# Quantum Experiment Visibility Kit

## Purpose

This kit prepares a cautious public release of the Bell-state laboratory and
its Quantum Experiment Passport. It is designed for educational and academic
discussion, not for marketing a security product or claiming a new result in
experimental quantum physics.

## One-sentence description

QuasarChain is an educational prototype that signs a reproducible Bell-state
experiment so that later changes to its circuit, parameters, or observed counts
can be detected.

## Short technical abstract

We present a local Quantum Experiment Passport format for recording the
provenance and integrity of a reproducible Bell-state experiment. The passport
contains a canonical circuit representation, a SHA-256 circuit hash, execution
parameters, observed counts, and an Ed25519 signature. In an ideal state-vector
simulation with 1,024 shots and a fixed seed, the experiment produced only
`00` and `11` outcomes. Modifying a signed count caused verification to return
`invalid_signature`. This prototype addresses record integrity and
reproducibility; it does not establish Bell-inequality violation, nonlocality,
hardware equivalence, or scientific validity of an interpretation.

## Suggested public announcement

> I released an educational prototype of a Quantum Experiment Passport. It
> records a Bell-state circuit, its parameters, observed counts, and a
> cryptographic signature. The demo is intentionally modest: it shows that
> tampering with a signed result is detectable, not that a simulator proves a
> physical claim. The method, tests, observed output, and limitations are
> available in the repository.

## Evidence to publish

- Repository commit or tagged release.
- [Bell-state laboratory note](quantum-experiment-passport.md).
- [CITATION.cff](../CITATION.cff).
- Test output showing `24 passed`.
- The circuit hash and observed counts.
- The explicit limitations and threat model.
- The cross-framework replication report and its comparison criteria.

The current Qiskit comparison produced `00: 517` and `11: 507`, while the
standard-library simulator produced `00: 546` and `11: 478` with the same shot
count and seed. Report the shared support (`00` and `11`) rather than claiming
identical counts across frameworks.

The Qiskit Aer readout-noise run used a symmetric independent error probability
of 5% per qubit and produced `00: 456`, `01: 53`, `10: 50`, and `11: 465`.
Describe this as a noise-model result, not as a measurement from physical
hardware.

The additional contribution is differential replication: the same logical Bell
circuit is executed by two independent simulators, and the passport records
which invariants agree without pretending that framework-specific random
sequences must match exactly.

Do not publish private keys, real user data, production credentials, or an
unverified DOI. A Zenodo DOI should be added only after a release has been
uploaded and Zenodo has minted it.

## Release checklist

1. Run `python -m pytest -q` in a clean supported Python environment.
2. Confirm that the Bell-state note matches the implementation and test output.
3. Create a versioned Git tag or GitHub release.
4. Enable the GitHub-Zenodo integration and archive that exact release.
5. Add the minted DOI to the release description and citation metadata.
6. Ask for technical review from a quantum-computing practitioner and a
   reproducibility or data-provenance researcher.

## Academic discussion prompts

- Which fields are necessary to reproduce a circuit across frameworks?
- How should bit-ordering conventions be represented in a portable passport?
- Which claims require a noise model or hardware execution rather than an ideal
  simulator?
- How should signer identity, key rotation, and revocation be represented?
- Which parts of the receipt are observations, and which are interpretations?

## Scope statement

The project should be described as a small educational study of provenance and
integrity for quantum experiments. It should not be described as a quantum
hardware benchmark, a Bell test, a security certification, or evidence that a
cryptographic signature establishes scientific truth.