---
concept_name: "Multi-objective Optimization"
canonical_key: "multi objective optimization"
concept_type: "method"
domain: "Machine Learning"
topic: "AutoML"
importance_score: 4
scope_level: 3
study_priority: 4
version_number: 11
last_updated_timestamp: "2026-08-05T17:21:13.267514+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Multi-objective Optimization

## Classification
- domain: Machine Learning
- topic: AutoML
- type: method
- scope: 3/5 (core concept or method)
- study priority: 4/5
- also known as: multi criteria optimisation, multi criteria optimization, multi-criteria optimization, multi-objective optimisation
- broader topic(s): Decision Making, Optimization

## Contributing Courses
- Auto-ML

## Definition
Multi-objective Optimization minimizes several objectives at once, such as validation error, runtime, memory, and model size. Because objectives can conflict, the result is usually a Pareto set of non-dominated trade-offs rather than one universally best configuration.

## Why it Matters
AutoML systems often optimize more than accuracy. Multi-objective optimization makes runtime, memory, model size, and predictive quality explicit so deployment trade-offs remain visible.

## Core Intuition
There may be no single winner: a model can be more accurate but slower, smaller but less accurate, so keep only trade-offs that another candidate does not dominate.

## How it Works
1. Define all objectives and their directions, scales, and resource constraints.
2. Evaluate configurations as objective vectors rather than collapsing them immediately into one score.
3. Remove dominated configurations and preserve the current Pareto front.
4. Present the remaining trade-offs so a deployment decision can select an operating point.

## Mathematical Foundation
$$
\min_{\lambda \in \Lambda} c(\lambda) = (c_1(\lambda), \ldots, c_m(\lambda)), \qquad m \ge 2
$$

A configuration is Pareto-dominated when another is no worse on every objective and strictly better on at least one.

## Key Components
- Objective vector
- Objective scales
- Dominance relation
- Pareto set/front
- Constraint handling
- Decision point

## Advantages
- Makes resource and quality trade-offs visible instead of hiding them in one score.
- Returns alternatives suited to different deployment constraints.

## Limitations
- There may be many non-dominated solutions and no single default choice.
- Scaling and weighting objectives can change the apparent trade-off.

## Common Mistakes
- Collapsing objectives into a weighted score without justifying scales or stakeholder preferences.
- Calling one solution best when several solutions are non-dominated on the Pareto front.
- Reporting accuracy, cost, and latency without stating constraints, units, or measurement conditions.

## Real-world Applications
- Accuracy-Resource Trade-offs
- Pareto Optimization
- Pipeline Optimization

## Interview Questions
- What does Pareto dominance mean?
- Why can there be no single best solution under multiple objectives?
- When should constraints be used instead of a weighted objective?
- How would you report the trade-off between accuracy, latency, and cost?

## Related Concepts
- AutoML Evaluation and Benchmarking
- Bayesian Optimization

## Connections
- Depends on: Hyperparameter Optimization and Model Evaluation
- Used in: Accuracy-Resource Trade-offs, Pareto Optimization, and Pipeline Optimization
- Related: Bayesian Optimization and AutoML Evaluation and Benchmarking
- Broader topic: AutoML, Optimization, and Decision Making

## Prerequisites
- Hyperparameter Optimization
- Model Evaluation

## Slide-derived Evidence
- Auto-ML | p7 | [6_Multicriteria_ALL.pdf](../data/raw/Auto-ML/6_Multicriteria_ALL.pdf#page=7) — Alternative names: multi-criteria optimization, multi-objective optimization, Pareto A multi-criteria optimization problem is defined by minc(λλλ) ⇔ min(c (λλλ),c (λλλ),...,c (λλλ)), 1 2 m λλλ∈ΛΛΛ λλλ∈ΛΛΛ with ΛΛΛ ⊂ Rn and multi-criteria objective function c :ΛΛΛ → Rm, m ≥ 2. Goal: minimize multiple target functions simultaneously. (c (λλλ),...,c (λλλ))(cid:62) maps each candidate λλλ into the objecive space Rm. 1 m Often no clear best solution, as objective are usually conflicting and we cannot totally order in Rm. W.l.o.g. we always minimize. Alternative names: multi-criteria optimization, multi-objective optimization, Pareto optimization. Definition: multi-criteria optimization problem

## Provenance
- Auto-ML | p7 | [6_Multicriteria_ALL.pdf](../data/raw/Auto-ML/6_Multicriteria_ALL.pdf#page=7) — Alternative names: multi-criteria optimization, multi-objective optimization, Pareto A multi-criteria optimization problem is defined by minc(λλλ) ⇔ min(c (λλλ),c (λλλ),...,c (λλλ)), 1 2 m λλλ∈ΛΛΛ λλλ∈ΛΛΛ with ΛΛΛ ⊂ Rn and multi-criteria objective function c :ΛΛΛ → Rm, m ≥ 2. Goal: minimize multiple target functions simultaneously. (c (λλλ),...,c (λλλ))(cid:62) maps each candidate λλλ into the objecive space Rm. 1 m Often no clear best solution, as objective are usually conflicting and we cannot totally order in Rm. W.l.o.g. we always minimize. Alternative names: multi-criteria optimization, multi-objective optimization, Pareto optimization. Definition: multi-criteria optimization problem

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.542
- evidence strength: 0.62
- definition quality: 0.18
- interview relevance: 0.92
- version: 11
- last updated: 2026-08-05T17:21:13.267514+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- assumptions not extracted
