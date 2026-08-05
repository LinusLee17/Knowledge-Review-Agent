---
concept_name: "Hidden Markov Models"
canonical_key: "hidden markov model"
concept_type: "model"
domain: "Machine Learning"
topic: "Sequential Modeling"
importance_score: 5
scope_level: 3
study_priority: 5
version_number: 1
last_updated_timestamp: "2026-08-05T17:13:39.145567+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Hidden Markov Models

## Classification
- domain: Machine Learning
- topic: Sequential Modeling
- type: model
- scope: 3/5 (core concept or method)
- study priority: 5/5
- also known as: hmm, hmms
- broader topic(s): Probabilistic Graphical Models

## Contributing Courses
- BT3102

## Definition
Hidden Markov Models represent sequences with unobserved states that emit observed outputs. Inference combines state-transition probabilities with emission probabilities to reason about the hidden sequence.

## Why it Matters
Hidden Markov Models provides a formal way to support Sequence Labeling, Speech Recognition, Time Series under stated assumptions.

## Core Intuition
Infer an invisible state sequence from the noisy observations it generates.

## How it Works
1. Combine the inputs into a score or prediction rule.
2. Fit the parameters with the chosen objective.
3. Interpret the fitted coefficients or predicted values in Sequential Modeling.

## Key Components
- Features or inputs
- Parameters or coefficients
- Prediction rule
- Loss or fit criterion

## Common Mistakes
- Do not memorize Hidden Markov Models without understanding its role in the surrounding topic.

## Real-world Applications
- Sequence Labeling
- Speech Recognition
- Time Series

## Interview Questions
- What problem does Hidden Markov Models solve, and what is its output?
- Explain Hidden Markov Models using one concrete input-to-decision example.
- What assumptions must hold before using Hidden Markov Models?
- Which trade-off decides whether to use Hidden Markov Models instead of an alternative?
- How does Hidden Markov Models compare with Bayesian Networks?

## Related Concepts
- Bayesian Networks
- Markov Models
- Viterbi Algorithm

## Connections
- Depends on: Markov Models and Probability
- Used in: Speech Recognition, Sequence Labeling, and Time Series
- Related: Markov Models, Bayesian Networks, and Viterbi Algorithm
- Broader topic: Probabilistic Graphical Models and Sequential Modeling

## Prerequisites
- Markov Models
- Probability

## Slide-derived Evidence
- BT3102 | p1-p7, p9, p11-p12, p15-p16, p18-p21 | [W0_Logistics.pdf](../data/raw/BT3102/W0_Logistics.pdf#page=1) — ▸ Hidden Markov Models Hidden Markov Models - Introduction & MLE W-7 3-Mar Hidden Markov Models - Inference Discussion of Group Project
- BT3102 | p8 | [W0_Logistics.pdf](../data/raw/BT3102/W0_Logistics.pdf#page=8) — W-7 3-Mar Hidden Markov Models - Inference Discussion of Group Project Hidden Markov Models - Introduction & MLE ▸ Hidden Markov Models
- BT3102 | p1-p21 | [W2-Probability_Basics.pdf](../data/raw/BT3102/W2-Probability_Basics.pdf#page=1) — ‣ e.g., Inference in Bayesian networks, Hidden Markov Models, etc.
- BT3102 | p1-p23, p26, p31-p33 | [W6-BN-MarkovModels.pdf](../data/raw/BT3102/W6-BN-MarkovModels.pdf#page=1) — ▸ AIMA Chapter 15.3: Hidden Markov Models Hidden Markov Models ▸ We can use Hidden Markov models for this purpose:
- BT3102 | p24 | [W6-BN-MarkovModels.pdf](../data/raw/BT3102/W6-BN-MarkovModels.pdf#page=24) — Hidden Markov Models ▸ We can use Hidden Markov models for this purpose: ▸ AIMA Chapter 15.3: Hidden Markov Models

## Provenance
- BT3102 | p1-p7, p9, p11-p12, p15-p16, p18-p21 | [W0_Logistics.pdf](../data/raw/BT3102/W0_Logistics.pdf#page=1) — ▸ Hidden Markov Models Hidden Markov Models - Introduction & MLE W-7 3-Mar Hidden Markov Models - Inference Discussion of Group Project
- BT3102 | p8 | [W0_Logistics.pdf](../data/raw/BT3102/W0_Logistics.pdf#page=8) — W-7 3-Mar Hidden Markov Models - Inference Discussion of Group Project Hidden Markov Models - Introduction & MLE ▸ Hidden Markov Models
- BT3102 | p1-p21 | [W2-Probability_Basics.pdf](../data/raw/BT3102/W2-Probability_Basics.pdf#page=1) — ‣ e.g., Inference in Bayesian networks, Hidden Markov Models, etc.
- BT3102 | p1-p23, p26, p31-p33 | [W6-BN-MarkovModels.pdf](../data/raw/BT3102/W6-BN-MarkovModels.pdf#page=1) — ▸ AIMA Chapter 15.3: Hidden Markov Models Hidden Markov Models ▸ We can use Hidden Markov models for this purpose:
- BT3102 | p24 | [W6-BN-MarkovModels.pdf](../data/raw/BT3102/W6-BN-MarkovModels.pdf#page=24) — Hidden Markov Models ▸ We can use Hidden Markov models for this purpose: ▸ AIMA Chapter 15.3: Hidden Markov Models
- BT3102 | p25, p27-p29 | [W6-BN-MarkovModels.pdf](../data/raw/BT3102/W6-BN-MarkovModels.pdf#page=25) — Hidden Markov Models ▸ AIMA Chapter 15.3: Hidden Markov Models ▸ We can use Hidden Markov models for this purpose:
- BT3102 | p30 | [W6-BN-MarkovModels.pdf](../data/raw/BT3102/W6-BN-MarkovModels.pdf#page=30) — ‣ Hidden Markov Models for Longitudinal Comparisons, Journal of the American Statistical Association, 2005, Scott, S., ▸ AIMA Chapter 15.3: Hidden Markov Models Hidden Markov Models
- BT3102 | p1, p7-p20, p22-p31 | [W7_HMM_Semantics.pdf](../data/raw/BT3102/W7_HMM_Semantics.pdf#page=1) — L7 Hidden Markov Models – Representation & MLE Parameters Recap: Hidden Markov Models ▸ We can use Hidden Markov models for this purpose:
- BT3102 | p2 | [W7_HMM_Semantics.pdf](../data/raw/BT3102/W7_HMM_Semantics.pdf#page=2) — Recap: Hidden Markov Models ▸ We can use Hidden Markov models for this purpose: L7 Hidden Markov Models – Representation & MLE Parameters
- BT3102 | p3-p5 | [W7_HMM_Semantics.pdf](../data/raw/BT3102/W7_HMM_Semantics.pdf#page=3) — Recap: Hidden Markov Models L7 Hidden Markov Models – Representation & MLE Parameters ▸ We can use Hidden Markov models for this purpose:
- BT3102 | p6 | [W7_HMM_Semantics.pdf](../data/raw/BT3102/W7_HMM_Semantics.pdf#page=6) — Hidden Markov Models L7 Hidden Markov Models – Representation & MLE Parameters Recap: Hidden Markov Models
- BT3102 | p21 | [W7_HMM_Semantics.pdf](../data/raw/BT3102/W7_HMM_Semantics.pdf#page=21) — ▸ Hidden Markov Models can be extended in several ways to incorporate L7 Hidden Markov Models – Representation & MLE Parameters Recap: Hidden Markov Models
- BT3102 | p1-p2, p4, p7-p33 | [W8-HMM-Viterbi.pdf](../data/raw/BT3102/W8-HMM-Viterbi.pdf#page=1) — L8 Hidden Markov Models – Viterbi Algorithm ▸ Notes in canvas on Hidden Markov Models Recap: Definition of HMM
- BT3102 | p3 | [W8-HMM-Viterbi.pdf](../data/raw/BT3102/W8-HMM-Viterbi.pdf#page=3) — ▸ Notes in canvas on Hidden Markov Models L8 Hidden Markov Models – Viterbi Algorithm Recap: Definition of HMM
- BT3102 | p5 | [W8-HMM-Viterbi.pdf](../data/raw/BT3102/W8-HMM-Viterbi.pdf#page=5) — L8 Hidden Markov Models – Viterbi Algorithm ▸ Notes in canvas on Hidden Markov Models Recap: Representation of HMM
- BT3102 | p6 | [W8-HMM-Viterbi.pdf](../data/raw/BT3102/W8-HMM-Viterbi.pdf#page=6) — L8 Hidden Markov Models – Viterbi Algorithm ▸ Notes in canvas on Hidden Markov Models Recap: MLE Parameters of HMM

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.742
- evidence strength: 0.98
- definition quality: 0.28
- interview relevance: 0.98
- version: 1
- last updated: 2026-08-05T17:13:39.145567+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- no meaningful equation or formal relationship extracted
- assumptions not extracted
- trade-offs or limitations not extracted
