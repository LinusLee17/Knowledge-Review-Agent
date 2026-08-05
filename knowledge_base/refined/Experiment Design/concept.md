---
concept_name: "Experiment Design"
canonical_key: "experiment design"
concept_type: "method"
domain: "Statistics"
topic: "Causal Analysis"
importance_score: 5
scope_level: 3
study_priority: 5
version_number: 2
last_updated_timestamp: "2026-08-05T17:17:19.260216+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Experiment Design

## Classification
- domain: Statistics
- topic: Causal Analysis
- type: method
- scope: 3/5 (core concept or method)
- study priority: 5/5
- also known as: design of experiments, experiment, experiment guidelines, experimental design, experiments
- broader topic(s): Statistical Inference

## Contributing Courses
- BT1101
- BT2101

## Definition
Experiment Design is a systematic procedure for transforming inputs into an output or decision in Causal Analysis. It is used in A/B Testing, Policy Evaluation, Treatment Effects. It is commonly considered alongside Causal Inference, Hypothesis Testing, Internal Validity.

## Why it Matters
It matters because it provides a concrete way to reason about A/B Testing, Policy Evaluation, Treatment Effects and choose an appropriate next action.

## Core Intuition
Plan the comparison before collecting outcomes so treatment differences have a credible interpretation.

## How it Works
1. Define the question, inputs, and assumptions.
2. Apply the method or relationship.
3. Produce the estimate, prediction, or decision.
4. Evaluate the result against an explicit criterion and known limitations.

## Key Components
- Inputs and objective
- Core transformation or rule
- Output and evaluation criterion
- Assumptions and failure modes

## Advantages
- Or take advantage of a natural experiment
- Quasi Experiments: Take advantage of “natural” variations in the key
- Take advantage of a “natural experiment”
- You are unable to take advantage of a natural experiment

## Common Mistakes
- Applying the concept without checking its assumptions or data context.
- Reporting a result without explaining what it measures and what it cannot establish.
- Confusing the concept with a related quantity, method, or decision rule.

## Real-world Applications
- A/B Testing
- Policy Evaluation
- Treatment Effects

## Interview Questions
- What problem does Experiment Design solve, and what is its output?
- Explain Experiment Design using one concrete input-to-decision example.
- Walk through Experiment Design step by step and name its stopping or evaluation rule.
- What assumptions must hold before using Experiment Design?
- Which trade-off decides whether to use Experiment Design instead of an alternative?
- How does Experiment Design compare with Causal Inference?

## Related Concepts
- Causal Inference
- Hypothesis Testing
- Internal Validity

## Connections
- Depends on: Sampling and Hypothesis Testing
- Used in: A/B Testing, Treatment Effects, and Policy Evaluation
- Related: Causal Inference, Internal Validity, and Hypothesis Testing
- Broader topic: Causal Analysis and Statistical Inference

## Prerequisites
- Hypothesis Testing
- Sampling

## Slide-derived Evidence
- BT1101 | p1-p31 | [Week 5 Probability distributions and Modeling.pdf](../data/raw/BT1101/Week 5 Probability distributions and Modeling.pdf#page=1) — • Experiment: process that results in an outcome • Outcome of an experiment: result that we observe experiment
- BT1101 | p42 | [Week 6 Hypothesis testing.pdf](../data/raw/BT1101/Week 6 Hypothesis testing.pdf#page=42) — Experiment-wise controlling experiment-wise(or family-wise) error rate Experiment-wise error rate ( 1-(1-alpha)^C )
- BT1101 | p6 | [Week 6 Sampling and Estimation.pdf](../data/raw/BT1101/Week 6 Sampling and Estimation.pdf#page=6) — • Experiment: • Repeat sampling experiment for samples of size 25, 100, and 500
- BT1101 | p8 | [Week 6 Sampling and Estimation.pdf](../data/raw/BT1101/Week 6 Sampling and Estimation.pdf#page=8) — • Repeat sampling experiment for samples of size 25, 100, and 500 • Experiment:
- BT2101 | p1-p2, p4, p7, p9, p11-p72, p74-p84, p86-p102, p104-p108, p110, p112-p129, p131-p141, p143, p145, p147-p153, p155, p161, p164, p166-p198, p200, p202, p205 | [BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=1) — Guidelines for a good experiment • Ideally, run an experiment! • In the ideal case of an experiment with random sampling

## Provenance
- BT1101 | p1-p31 | [Week 5 Probability distributions and Modeling.pdf](../data/raw/BT1101/Week 5 Probability distributions and Modeling.pdf#page=1) — • Experiment: process that results in an outcome • Outcome of an experiment: result that we observe experiment
- BT1101 | p42 | [Week 6 Hypothesis testing.pdf](../data/raw/BT1101/Week 6 Hypothesis testing.pdf#page=42) — Experiment-wise controlling experiment-wise(or family-wise) error rate Experiment-wise error rate ( 1-(1-alpha)^C )
- BT1101 | p6 | [Week 6 Sampling and Estimation.pdf](../data/raw/BT1101/Week 6 Sampling and Estimation.pdf#page=6) — • Experiment: • Repeat sampling experiment for samples of size 25, 100, and 500
- BT1101 | p8 | [Week 6 Sampling and Estimation.pdf](../data/raw/BT1101/Week 6 Sampling and Estimation.pdf#page=8) — • Repeat sampling experiment for samples of size 25, 100, and 500 • Experiment:
- BT2101 | p1-p2, p4, p7, p9, p11-p72, p74-p84, p86-p102, p104-p108, p110, p112-p129, p131-p141, p143, p145, p147-p153, p155, p161, p164, p166-p198, p200, p202, p205 | [BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=1) — Guidelines for a good experiment • Ideally, run an experiment! • In the ideal case of an experiment with random sampling
- BT2101 | p109 | [BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=109) — Guidelines for a good experiment • In the ideal case of an experiment with random sampling • Ideally, run an experiment!
- BT2101 | p142 | [BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=142) — Guidelines for a good experiment • How to design a good experiment? • Ideally, run an experiment!
- BT2101 | p144 | [BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=144) — Guidelines for a good experiment • An experiment entails conscious use of a treatment and control group • An experiment is designed and implemented consciously by human
- BT2101 | p146, p199 | [BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=146) — Guidelines for a good experiment • An ideal randomized controlled experiment randomly assigns subjects • Ideally, run an experiment!
- BT2101 | p154, p201 | [BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=154) — Guidelines for a good experiment • subject behavior might be affected by being in an experiment • Ideally, run an experiment!
- BT2101 | p156, p203 | [BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=156) — Guidelines for a good experiment • A quasi-experiment or natural experiment has a source of • Ideally, run an experiment!
- BT2101 | p157 | [BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=157) — Guidelines for a good experiment • But it is unethical to run an experiment that exposes pregnant women to pollution Take advantage of a “natural experiment”:
- BT2101 | p158 | [BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=158) — Guidelines for a good experiment experiment." Environmental health perspectives 123.9 (2015): 880-887. • Ideally, run an experiment!
- BT2101 | p159 | [BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=159) — Guidelines for a good experiment Is this experiment internally valid? experiment." Environmental health perspectives 123.9 (2015): 880-887.
- BT2101 | p160 | [BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=160) — Guidelines for a good experiment Is this natural experiment internally valid? experiment." Environmental health perspectives 123.9 (2015): 880-887.
- BT2101 | p162 | [BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=162) — Guidelines for a good experiment Is this experiment internally valid? • Ideally, run an experiment!
- BT2101 | p163, p165 | [BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=163) — Guidelines for a good experiment Is this natural experiment internally valid? • Ideally, run an experiment!
- BT2101 | p1-p11, p13-p18, p21-p29 | [VK.wk13.2024.pdf](../data/raw/BT2101/VK.wk13.2024.pdf#page=1) — Guidelines for a good experiment • An experiment is designed and implemented consciously by human • An experiment entails conscious use of a treatment and control group
- BT2101 | p12 | [VK.wk13.2024.pdf](../data/raw/BT2101/VK.wk13.2024.pdf#page=12) — Guidelines for a good experiment • An experiment entails conscious use of a treatment and control group • An experiment is designed and implemented consciously by human
- BT2101 | p19 | [VK.wk13.2024.pdf](../data/raw/BT2101/VK.wk13.2024.pdf#page=19) — Guidelines for a good experiment • A quasi-experiment or natural experiment has a source of randomization • A natural experiment setup in which assignment to treatment/control
- BT2101 | p20 | [VK.wk13.2024.pdf](../data/raw/BT2101/VK.wk13.2024.pdf#page=20) — Guidelines for a good experiment • A natural experiment setup in which assignment to treatment/control • An experiment is designed and implemented consciously by human
- BT2101 | p1-p6, p8-p12, p15-p22, p24-p36 | [VK.wk8.2024.pdf](../data/raw/BT2101/VK.wk8.2024.pdf#page=1) — Guidelines for a good experiment • A quasi-experiment or natural experiment has a source of • A natural experiment setup in which assignment to treatment/control
- BT2101 | p7, p13 | [VK.wk8.2024.pdf](../data/raw/BT2101/VK.wk8.2024.pdf#page=7) — Guidelines for a good experiment • A natural experiment setup in which assignment to treatment/control • A quasi-experiment or natural experiment has a source of
- BT2101 | p14 | [VK.wk8.2024.pdf](../data/raw/BT2101/VK.wk8.2024.pdf#page=14) — Guidelines for a good experiment • Is this a random experiment? Are Jurong East and Clementi • A quasi-experiment or natural experiment has a source of
- BT2101 | p23 | [VK.wk8.2024.pdf](../data/raw/BT2101/VK.wk8.2024.pdf#page=23) — Guidelines for a good experiment • It is unethical/expensive/infeasible to run an experiment • You are unable to take advantage of a natural experiment
- BT2101 | p1-p16, p19-p31 | [VK.wk9.2024.pdf](../data/raw/BT2101/VK.wk9.2024.pdf#page=1) — • Ideally, run an experiment • Or take advantage of a natural experiment • It is unethical/expensive/infeasible to run an experiment
- BT2101 | p17 | [VK.wk9.2024.pdf](../data/raw/BT2101/VK.wk9.2024.pdf#page=17) — • Or take advantage of a natural experiment • Ideally, run an experiment • It is unethical/expensive/infeasible to run an experiment
- BT2101 | p18 | [VK.wk9.2024.pdf](../data/raw/BT2101/VK.wk9.2024.pdf#page=18) — • It is unethical/expensive/infeasible to run an experiment • You are unable to take advantage of a natural experiment • Ideally, run an experiment

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.692
- evidence strength: 0.86
- definition quality: 0.28
- interview relevance: 0.98
- version: 2
- last updated: 2026-08-05T17:17:19.260216+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- assumptions not extracted
- trade-offs or limitations not extracted
