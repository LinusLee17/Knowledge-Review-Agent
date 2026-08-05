---
concept_name: "Decision Trees"
canonical_key: "decision tree"
concept_type: "algorithm"
domain: "Machine Learning"
topic: "Supervised Learning"
importance_score: 5
scope_level: 3
study_priority: 5
version_number: 3
last_updated_timestamp: "2026-08-05T16:27:50.385854+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Decision Trees

## Classification
- domain: Machine Learning
- topic: Supervised Learning
- type: algorithm
- scope: 3/5 (core concept or method)
- study priority: 5/5
- also known as: tree model
- broader topic(s): Tree-Based Models

## Contributing Courses
- BT4240
- CS3244

## Definition
Decision Trees are supervised-learning models that recursively split observations by feature rules until terminal leaves support predictions or decisions. They are used in Classification, Decision Analysis, Regression. It is commonly considered alongside Classification, Gradient Boosting, Random Forest.

## Why it Matters
It matters because it provides a concrete way to reason about Classification, Decision Analysis, Regression and choose an appropriate next action.

## Core Intuition
Understand the concept as a link between inputs, assumptions, and an observable output. Change one assumption at a time and check how the result changes.

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

## Common Mistakes
- Applying the concept without checking its assumptions or data context.
- Reporting a result without explaining what it measures and what it cannot establish.
- Confusing the concept with a related quantity, method, or decision rule.

## Real-world Applications
- Classification
- Decision Analysis
- Regression

## Interview Questions
- What problem does Decision Trees solve, and what is its output?
- Explain Decision Trees using one concrete input-to-decision example.
- Walk through Decision Trees step by step and name its stopping or evaluation rule.
- What assumptions must hold before using Decision Trees?
- Which trade-off decides whether to use Decision Trees instead of an alternative?
- How does Decision Trees compare with Classification?

## Related Concepts
- Classification
- Gradient Boosting
- Random Forest

## Connections
- Depends on: Entropy and Gini Impurity
- Used in: Classification, Regression, and Decision Analysis
- Related: Random Forest, Gradient Boosting, and Classification
- Broader topic: Supervised Learning and Tree-Based Models

## Prerequisites
- Entropy
- Gini Impurity

## Slide-derived Evidence
- BT4240 | p6 | [L4-InformationBasedLearning.pdf](../data/raw/BT4240/L4-InformationBasedLearning.pdf#page=6) — 2. Fundamentals of decision trees • Two decision trees that are consistent with the instances in the data set:
- BT4240 | p40 | [L4-InformationBasedLearning.pdf](../data/raw/BT4240/L4-InformationBasedLearning.pdf#page=40) — • Subspace sampling is often used when bagging decision trees. • Random Forest model: the combination of bagging, subspace sampling and decision trees.
- CS3244 | p37 | [Lecture03_decision_trees.pdf](../data/raw/CS3244/Lecture03_decision_trees.pdf#page=37) — Random forest is an ensemble of decision trees.

## Provenance
- BT4240 | p6 | [L4-InformationBasedLearning.pdf](../data/raw/BT4240/L4-InformationBasedLearning.pdf#page=6) — 2. Fundamentals of decision trees • Two decision trees that are consistent with the instances in the data set:
- BT4240 | p40 | [L4-InformationBasedLearning.pdf](../data/raw/BT4240/L4-InformationBasedLearning.pdf#page=40) — • Subspace sampling is often used when bagging decision trees. • Random Forest model: the combination of bagging, subspace sampling and decision trees.
- CS3244 | p37 | [Lecture03_decision_trees.pdf](../data/raw/CS3244/Lecture03_decision_trees.pdf#page=37) — Random forest is an ensemble of decision trees.

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.823
- evidence strength: 0.72
- definition quality: 0.84
- interview relevance: 0.98
- version: 3
- last updated: 2026-08-05T16:27:50.385854+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- assumptions not extracted
- trade-offs or limitations not extracted
