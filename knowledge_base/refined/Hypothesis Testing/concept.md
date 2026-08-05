---
concept_name: "Hypothesis Testing"
canonical_key: "hypothesis testing"
concept_type: "method"
domain: "Statistics"
topic: "Inference"
importance_score: 5
scope_level: 3
study_priority: 5
version_number: 4
last_updated_timestamp: "2026-08-05T16:27:50.414852+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Hypothesis Testing

## Classification
- domain: Statistics
- topic: Inference
- type: method
- scope: 3/5 (core concept or method)
- study priority: 5/5
- also known as: significance testing, test of hypothesis
- broader topic(s): Statistical Inference

## Contributing Courses
- ST1131

## Definition
Hypothesis Testing is a procedure that compares sample evidence with a null hypothesis using a test statistic and decision rule. It is used in A/B Testing, Experimentation. It is commonly considered alongside Confidence Interval, Type I Error, Type II Error.

## Why it Matters
It matters because it provides a concrete way to reason about A/B Testing, Experimentation and choose an appropriate next action.

## Core Intuition
Understand the concept as a link between inputs, assumptions, and an observable output. Change one assumption at a time and check how the result changes.

## How it Works
1. State null and alternative claims.
2. Choose a test statistic and its null distribution.
3. Compute the statistic and p-value or critical-region decision.
4. Report the decision, uncertainty, effect size, and possible error.

## Key Components
- Null and alternative hypotheses
- Test statistic and null distribution
- Significance level or decision threshold
- Effect size and Type I/II error consequences

## Common Mistakes
- Applying the concept without checking its assumptions or data context.
- Reporting a result without explaining what it measures and what it cannot establish.
- Confusing the concept with a related quantity, method, or decision rule.

## Real-world Applications
- A/B Testing
- Experimentation

## Interview Questions
- What problem does Hypothesis Testing solve, and what is its output?
- Explain Hypothesis Testing using one concrete input-to-decision example.
- Walk through Hypothesis Testing step by step and name its stopping or evaluation rule.
- What assumptions must hold before using Hypothesis Testing?
- Which trade-off decides whether to use Hypothesis Testing instead of an alternative?
- How does Hypothesis Testing compare with Confidence Interval?

## Related Concepts
- Confidence Interval
- Type I Error
- Type II Error
- p-value

## Connections
- Depends on: Probability and Sampling
- Used in: Experimentation and A/B Testing
- Related: p-value, Confidence Interval, and Type I Error
- Broader topic: Statistical Inference

## Prerequisites
- Probability
- Sampling

## Slide-derived Evidence
- ST1131 | p18 | [Topic0_Introduction.pdf](../data/raw/ST1131/Topic0_Introduction.pdf#page=18) — 8 Hypothesis Testing Topics 1 Introduction to R programming 2 Exploratory Data Analysis (EDA) 3 Collecting Data 4 Probability 5 Random Variables (Discrete and Continuous Random Variables) 6 Sampling Distribution 7 Statistical Estimation 8 Hypothesis Testing 9 Linear Regression 10 Some Limitations of Linear Regression (extra topic if time permits)
- ST1131 | p1, p5-p6, p8-p16, p18-p30, p33-p38, p40-p45, p47-p49, p51-p52, p54-p60, p62-p63 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=1) — Hypothesis Testing 2 5 Steps of Hypothesis Testing in General 3 Hypothesis Testing for Proportions
- ST1131 | p2-p3, p7, p17, p31-p32, p39, p46, p50, p53, p61 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=2) — 2 5 Steps of Hypothesis Testing in General 3 Hypothesis Testing for Proportions 4 Hypothesis Testing for Means
- ST1131 | p4 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=4) — Hypothesis testing, or significance tests, are the major and important Hypothesis Testing 2 5 Steps of Hypothesis Testing in General
- ST1131 | p1 | [Topic8_HypothesisTest_2.pdf](../data/raw/ST1131/Topic8_HypothesisTest_2.pdf#page=1) — Hypothesis Testing Hypothesis Testing Part 2: Two-Sample Data

## Provenance
- ST1131 | p18 | [Topic0_Introduction.pdf](../data/raw/ST1131/Topic0_Introduction.pdf#page=18) — 8 Hypothesis Testing Topics 1 Introduction to R programming 2 Exploratory Data Analysis (EDA) 3 Collecting Data 4 Probability 5 Random Variables (Discrete and Continuous Random Variables) 6 Sampling Distribution 7 Statistical Estimation 8 Hypothesis Testing 9 Linear Regression 10 Some Limitations of Linear Regression (extra topic if time permits)
- ST1131 | p1, p5-p6, p8-p16, p18-p30, p33-p38, p40-p45, p47-p49, p51-p52, p54-p60, p62-p63 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=1) — Hypothesis Testing 2 5 Steps of Hypothesis Testing in General 3 Hypothesis Testing for Proportions
- ST1131 | p2-p3, p7, p17, p31-p32, p39, p46, p50, p53, p61 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=2) — 2 5 Steps of Hypothesis Testing in General 3 Hypothesis Testing for Proportions 4 Hypothesis Testing for Means
- ST1131 | p4 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=4) — Hypothesis testing, or significance tests, are the major and important Hypothesis Testing 2 5 Steps of Hypothesis Testing in General
- ST1131 | p1 | [Topic8_HypothesisTest_2.pdf](../data/raw/ST1131/Topic8_HypothesisTest_2.pdf#page=1) — Hypothesis Testing Hypothesis Testing Part 2: Two-Sample Data
- ST1131 | p2-p45 | [Topic8_HypothesisTest_2.pdf](../data/raw/ST1131/Topic8_HypothesisTest_2.pdf#page=2) — Hypothesis Testing

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.932
- evidence strength: 0.98
- definition quality: 0.84
- interview relevance: 0.98
- version: 4
- last updated: 2026-08-05T16:27:50.414852+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- assumptions not extracted
- trade-offs or limitations not extracted
