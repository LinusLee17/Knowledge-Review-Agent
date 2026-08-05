---
concept_name: "PCA"
canonical_key: "pca"
concept_type: "method"
domain: "Data Science"
topic: "Dimensionality Reduction"
importance_score: 5
scope_level: 3
study_priority: 5
version_number: 7
last_updated_timestamp: "2026-08-05T17:20:40.853940+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# PCA

## Classification
- domain: Data Science
- topic: Dimensionality Reduction
- type: method
- scope: 3/5 (core concept or method)
- study priority: 5/5
- also known as: principal component analysis, principal components analysis
- broader topic(s): Unsupervised Learning

## Contributing Courses
- BT1101
- CS3244

## Definition
PCA (Principal Component Analysis) projects data onto orthogonal components ordered by explained variance, reducing dimensions while retaining prominent structure. It is used in Compression, Noise Reduction, Visualization. It is commonly considered alongside Dimensionality Reduction, Feature Engineering.

## Why it Matters
It matters because it provides a concrete way to reason about Compression, Noise Reduction, Visualization and choose an appropriate next action.

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
- Compression
- Noise Reduction
- Visualization

## Interview Questions
- What problem does PCA solve, and what is its output?
- Explain PCA using one concrete input-to-decision example.
- Walk through PCA step by step and name its stopping or evaluation rule.
- What assumptions must hold before using PCA?
- Which trade-off decides whether to use PCA instead of an alternative?
- How does PCA compare with Dimensionality Reduction?

## Related Concepts
- Dimensionality Reduction
- Feature Engineering

## Connections
- Depends on: Linear Algebra and Variance
- Used in: Visualization, Compression, and Noise Reduction
- Related: Dimensionality Reduction and Feature Engineering
- Broader topic: Unsupervised Learning

## Prerequisites
- Linear Algebra
- Variance

## Slide-derived Evidence
- BT1101 | p4 | [Week 9 Model Selection & Data Dimensionality Reduction.pdf](../data/raw/BT1101/Week 9 Model Selection & Data Dimensionality Reduction.pdf#page=4) — Main Approach of PCA Application of Principal Component Analysis (PCA) Principal Component Analysis (PCA) - Intuition
- BT1101 | p44 | [Week 9 Model Selection & Data Dimensionality Reduction.pdf](../data/raw/BT1101/Week 9 Model Selection & Data Dimensionality Reduction.pdf#page=44) — Running Principal Component Analysis (PCA) – in R We will select the independent variables for PCA analysis We use PCA to summarize information from all predictors except wage and city. (7 predictors)
- BT1101 | p45 | [Week 9 Model Selection & Data Dimensionality Reduction.pdf](../data/raw/BT1101/Week 9 Model Selection & Data Dimensionality Reduction.pdf#page=45) — Running Principal Component Analysis (PCA) – in R  pca_mroz$rotation contains the loadings for all 7 PC’s Main Approach of PCA
- BT1101 | p46 | [Week 9 Model Selection & Data Dimensionality Reduction.pdf](../data/raw/BT1101/Week 9 Model Selection & Data Dimensionality Reduction.pdf#page=46) — Running Principal Component Analysis (PCA) – in R Main Approach of PCA Application of Principal Component Analysis (PCA)
- BT1101 | p47 | [Week 9 Model Selection & Data Dimensionality Reduction.pdf](../data/raw/BT1101/Week 9 Model Selection & Data Dimensionality Reduction.pdf#page=47) — The PCA biplot shows the compositions of top 2 PC’s wrt to all predictors. Running Principal Component Analysis (PCA) – in R Main Approach of PCA

## Provenance
- BT1101 | p4 | [Week 9 Model Selection & Data Dimensionality Reduction.pdf](../data/raw/BT1101/Week 9 Model Selection & Data Dimensionality Reduction.pdf#page=4) — Main Approach of PCA Application of Principal Component Analysis (PCA) Principal Component Analysis (PCA) - Intuition
- BT1101 | p44 | [Week 9 Model Selection & Data Dimensionality Reduction.pdf](../data/raw/BT1101/Week 9 Model Selection & Data Dimensionality Reduction.pdf#page=44) — Running Principal Component Analysis (PCA) – in R We will select the independent variables for PCA analysis We use PCA to summarize information from all predictors except wage and city. (7 predictors)
- BT1101 | p45 | [Week 9 Model Selection & Data Dimensionality Reduction.pdf](../data/raw/BT1101/Week 9 Model Selection & Data Dimensionality Reduction.pdf#page=45) — Running Principal Component Analysis (PCA) – in R  pca_mroz$rotation contains the loadings for all 7 PC’s Main Approach of PCA
- BT1101 | p46 | [Week 9 Model Selection & Data Dimensionality Reduction.pdf](../data/raw/BT1101/Week 9 Model Selection & Data Dimensionality Reduction.pdf#page=46) — Running Principal Component Analysis (PCA) – in R Main Approach of PCA Application of Principal Component Analysis (PCA)
- BT1101 | p47 | [Week 9 Model Selection & Data Dimensionality Reduction.pdf](../data/raw/BT1101/Week 9 Model Selection & Data Dimensionality Reduction.pdf#page=47) — The PCA biplot shows the compositions of top 2 PC’s wrt to all predictors. Running Principal Component Analysis (PCA) – in R Main Approach of PCA
- CS3244 | p52 | [Lecture08_data-processing.pdf](../data/raw/CS3244/Lecture08_data-processing.pdf#page=52) — 1. Linear Separability 1. What is the issue? 1. Linear SVM, PCA, LDA (PCA, LDA, Deep Auto-Encoders) What did we learn? Data Issues Issue Template Checks 1. Linear Separability 1. What is the issue? 1. Linear SVM, PCA, LDA 2. Curse of Dimensionality 2. Why is it a problem? 2. Visualize Histograms 3. Imbalanced Data 3. When would it happen? Mitigations 4. How to check for it? 1. Dimensionality Reduction 5. How to mitigate it? (PCA, LDA, Deep Auto-Encoders) 2. Feature Selection (Recursive Feature Elimination, Correlation, Mutual Information) 3. Resampling (Under/Oversampling, SMOTE) 55
- CS3244 | p2 | [Lecture09_feature-engineering.pdf](../data/raw/CS3244/Lecture09_feature-engineering.pdf#page=2) — What did we learn this week? PCA and LDA for Dimensionality Reduction Data Issues IssueTemplate Checks PCA LDA 1. Linear Separability 1. Whatis the issue? 1. Linear SVM, PCA, LDA • All axes are orthogonal (independent)

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.973
- evidence strength: 0.98
- definition quality: 0.96
- interview relevance: 0.98
- version: 7
- last updated: 2026-08-05T17:20:40.853940+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- assumptions not extracted
- trade-offs or limitations not extracted
