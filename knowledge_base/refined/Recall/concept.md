---
concept_name: "Recall"
canonical_key: "recall"
concept_type: "metric"
domain: "Machine Learning"
topic: "Model Evaluation"
importance_score: 4
scope_level: 1
study_priority: 4
version_number: 8
last_updated_timestamp: "2026-08-05T17:20:40.871114+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Recall

## Classification
- domain: Machine Learning
- topic: Model Evaluation
- type: metric
- scope: 1/5 (specific metric or detail)
- study priority: 4/5
- also known as: sensitivity, true positive rate

## Contributing Courses
- BT1101
- BT4240
- CS3244
- ST1131

## Definition
Recall is a classification metric that measures the fraction of actual positive cases that a model correctly identifies. It matters when missing a positive case is more costly than producing a false alarm.

## Why it Matters
Recall matters whenever missing a positive case is costly. It is central in fraud detection, medical screening, and other imbalanced problems where false negatives hurt more than false alarms.

## Core Intuition
Count how many real positives you captured, not just how many predictions were correct overall.

## How it Works
1. Build the confusion matrix for the classifier.
2. Count the true positives and false negatives.
3. Compute recall as the share of actual positives that were correctly identified.

## Mathematical Foundation
$$
\text{Recall} = \frac{TP}{TP + FN}
$$

| Symbol | Meaning |
| --- | --- |
| `TP` | True positives |
| `FN` | False negatives |

## Key Components
- True positives
- False negatives
- Confusion matrix
- Decision threshold
- Recall formula

## Common Mistakes
- Assuming high accuracy means high recall.
- Optimizing recall without checking precision.
- Ignoring the decision threshold that drives the trade-off.

## Common Variants
- Macro Recall
- Micro Recall
- Top-k Recall

## Real-world Applications
- Classification Evaluation

## Interview Questions
- Why does recall matter in imbalanced or high-cost-miss problems?
- How is recall computed from the confusion matrix?
- How does recall trade off against precision?
- Why can accuracy be misleading when recall is low?

## Related Concepts
- Classification Accuracy
- Confusion Matrix
- Precision

## Connections
- Depends on: confusion matrix, true positives, false negatives
- Used in: medical screening, fraud detection, high-cost-miss settings
- Related: precision, F1 score, classification accuracy, threshold selection

## Prerequisites
- Confusion Matrix

## Further Reading
- scikit-learn classification metrics documentation
- Any standard machine learning evaluation reference

## Slide-derived Evidence
- BT1101 | p43 | [Week 9 Model Selection & Data Dimensionality Reduction.pdf](../data/raw/BT1101/Week 9 Model Selection & Data Dimensionality Reduction.pdf#page=43) — Recall : F-test for regression fit in previously … Recall the problem of finding the “best” model, given a set of explanatory variables Recall ) is called the loading of PC1:
- BT4240 | p17 | [L1-ContinuousOptimization.pdf](../data/raw/BT4240/L1-ContinuousOptimization.pdf#page=17) — • Recall Taylor series is a representation of a function f as an infinite sum of terms determined using derivatives
- BT4240 | p58 | [L2-Regression.pdf](../data/raw/BT4240/L2-Regression.pdf#page=58) — • Recall the parameter values are β = -3.0595 and β = 0.1615 ⇐
- BT4240 | p38 | [L3-SVM.pdf](../data/raw/BT4240/L3-SVM.pdf#page=38) — • Recall: In the original space, the optimal weight is w = α d x and the optimal decision boundary is
- BT4240 | p40 | [L3-SVM.pdf](../data/raw/BT4240/L3-SVM.pdf#page=40) — • Recall that the objective function in the original SVM formulation is Q(α) = α - ½ ααddxTx

## Provenance
- BT1101 | p43 | [Week 9 Model Selection & Data Dimensionality Reduction.pdf](../data/raw/BT1101/Week 9 Model Selection & Data Dimensionality Reduction.pdf#page=43) — Recall : F-test for regression fit in previously … Recall the problem of finding the “best” model, given a set of explanatory variables Recall ) is called the loading of PC1:
- BT4240 | p17 | [L1-ContinuousOptimization.pdf](../data/raw/BT4240/L1-ContinuousOptimization.pdf#page=17) — • Recall Taylor series is a representation of a function f as an infinite sum of terms determined using derivatives
- BT4240 | p58 | [L2-Regression.pdf](../data/raw/BT4240/L2-Regression.pdf#page=58) — • Recall the parameter values are β = -3.0595 and β = 0.1615 ⇐
- BT4240 | p38 | [L3-SVM.pdf](../data/raw/BT4240/L3-SVM.pdf#page=38) — • Recall: In the original space, the optimal weight is w = α d x and the optimal decision boundary is
- BT4240 | p40 | [L3-SVM.pdf](../data/raw/BT4240/L3-SVM.pdf#page=40) — • Recall that the objective function in the original SVM formulation is Q(α) = α - ½ ααddxTx
- CS3244 | p6 | [Lecture02_learning_paradigms_knn.pdf](../data/raw/CS3244/Lecture02_learning_paradigms_knn.pdf#page=6) — • You recall your physics lesson 𝑠 = 𝑣𝑡 + The training data is representative of
- ST1131 | p56 | [Topic9_LinearRegression.pdf](../data/raw/ST1131/Topic9_LinearRegression.pdf#page=56) — Recall that the raw residuals are defined to be Residuals Revisited Recall that the raw residuals are defined to be e = Y −Yˆ i i i The raw residuals are like our best estimates of what the ε ’s are. i Residual plots are used to: (cid:73) To check the normality assumption. (cid:73) To check for non-constant variance and the need to transform Y. (cid:73) To check for the need to add higher order terms in X.
- `ST1131/Topic6_SamplingDistribution/lecture.json` | `223670e847c5a3a030d8b5d5518b085da0b32209cfbc4d62a874f38d842bb411`
- `ST1131/Topic7_CI/lecture.json` | `49707f32434ce06d9f7dd569649c766e4623e24bfa406cb00daa0df8c6b5093a`

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.877
- evidence strength: 0.88
- definition quality: 0.8
- interview relevance: 0.98
- version: 8
- last updated: 2026-08-05T17:20:40.871114+00:00

## Assumptions
- Source: Mroz, T. (1987) “The sensitivity of an empirical model of married women's hours of work to economic and statistical assumptions”,Econometrica, 55, 765

## Quality Review
- This page needs human review before treated as authoritative:
- trade-offs or limitations not extracted
