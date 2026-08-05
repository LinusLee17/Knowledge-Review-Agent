---
concept_name: "Overfitting"
canonical_key: "overfitting"
concept_type: "phenomenon"
domain: "Machine Learning"
topic: "Model Evaluation"
importance_score: 4
scope_level: 2
study_priority: 4
version_number: 2
last_updated_timestamp: "2026-08-05T16:27:50.474765+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Overfitting

## Classification
- domain: Machine Learning
- topic: Model Evaluation
- type: phenomenon
- scope: 2/5 (supporting concept or practice)
- study priority: 4/5

## Contributing Courses
- CS3244

## Definition
Overfitting occurs when a model fits noise or idiosyncrasies in observed training data, giving low training error but poor performance on unseen data. It is used in Model Diagnostics. It is commonly considered alongside Cross Validation, Regularization.

## Why it Matters
It matters because a model can look successful on training data while failing on unseen cases. Detecting and controlling this gap protects generalization and makes validation results trustworthy.

## Core Intuition
A model has learned details of its training sample instead of the stable pattern. Training error keeps falling while validation or test error stops improving or rises.

## How it Works
1. Split data into training and validation/test sets without leakage.
2. Fit models of increasing flexibility or complexity.
3. Compare training error with validation/test error.
4. If the gap grows, reduce complexity, regularize, collect more data, or improve validation.

## Key Components
- Inputs and objective
- Core transformation or rule
- Output and evaluation criterion
- Assumptions and failure modes

## Common Mistakes
- Applying the concept without checking its assumptions or data context.
- Reporting a result without explaining what it measures and what it cannot establish.
- Confusing the concept with a related quantity, method, or decision rule.

## Real-world Applications
- Model Diagnostics

## Interview Questions
- What problem does Overfitting solve, and what is its output?
- Explain Overfitting using one concrete input-to-decision example.
- What assumptions must hold before using Overfitting?
- Which trade-off decides whether to use Overfitting instead of an alternative?
- How does Overfitting compare with Cross Validation?

## Related Concepts
- Cross Validation
- Regularization

## Connections
- Depends on: Bias-Variance Tradeoff
- Used in: Model Diagnostics
- Related: Regularization and Cross Validation
- Broader topic: Model Evaluation

## Prerequisites
- Bias-Variance Tradeoff

## Slide-derived Evidence
- CS3244 | p26 | [Lecture12a.deep-learning-rnn_26.pdf](../data/raw/CS3244/Lecture12a.deep-learning-rnn_26.pdf#page=26) — Overfitting in deep neural networks • Recall: what is overfitting?

## Provenance
- CS3244 | p26 | [Lecture12a.deep-learning-rnn_26.pdf](../data/raw/CS3244/Lecture12a.deep-learning-rnn_26.pdf#page=26) — Overfitting in deep neural networks • Recall: what is overfitting?

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.756
- evidence strength: 0.68
- definition quality: 0.72
- interview relevance: 0.94
- version: 2
- last updated: 2026-08-05T16:27:50.474765+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- definition lacks specific object, purpose, or scope
- assumptions not extracted
- trade-offs or limitations not extracted
