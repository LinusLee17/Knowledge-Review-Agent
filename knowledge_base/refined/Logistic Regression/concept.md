---
concept_name: "Logistic Regression"
canonical_key: "logistic regression"
concept_type: "model"
domain: "Machine Learning"
topic: "Supervised Learning"
importance_score: 5
scope_level: 3
study_priority: 5
version_number: 23
last_updated_timestamp: "2026-08-05T17:21:13.250386+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Logistic Regression

## Classification
- domain: Machine Learning
- topic: Supervised Learning
- type: model
- scope: 3/5 (core concept or method)
- study priority: 5/5
- also known as: binary logistic regression

## Contributing Courses
- BT4240
- CS3244

## Definition
Logistic Regression is a classification model that maps a linear score into a probability using the logistic function. It is widely used when the goal is to predict class membership, estimate odds, and produce a model that remains interpretable enough for business and technical review.

## Why it Matters
Logistic Regression is a standard classification baseline because it produces probabilities, remains interpretable, and transfers cleanly into business and technical settings where you need a decision rule and a score.

## Core Intuition
Model class probability directly, then threshold it for classification when needed.

## How it Works
1. Compute a linear score from the features.
2. Pass that score through the sigmoid function to get a probability.
3. Fit the coefficients by minimizing log-loss or maximizing likelihood, then apply a threshold if you need a class label.

## Mathematical Foundation
$$
p(y = 1 \mid x) = \sigma(\beta_0 + \beta^T x)
$$

$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$

| Symbol | Meaning |
| --- | --- |
| `p(y = 1 | x)` | Probability of class 1 |
| `\sigma` | Sigmoid function |
| `\beta` | Coefficients |
| `x` | Features |

## Key Components
- Linear predictor
- Sigmoid function
- Probability estimate
- Decision threshold
- Coefficients
- Log-loss objective

## Advantages
- Produces interpretable class probabilities.
- Fast to train and effective as a classification baseline.
- Supports regularization and scales well to high-dimensional features.

## Limitations
- Assumes a linear relationship between features and log-odds unless transformed or extended.
- Can be affected by multicollinearity, separation, and severe class imbalance.

## Common Mistakes
- Thinking logistic regression is a regression method instead of a classifier.
- Ignoring class imbalance or the decision threshold.
- Reading raw coefficients without considering the sigmoid link.

## Common Variants
- Binary Logistic Regression
- Multinomial Logistic Regression
- Regularized Logistic Regression

## Real-world Applications
- Classification
- Customer Churn
- Risk Scoring

## Interview Questions
- Why does logistic regression use the sigmoid function?
- How do you turn probabilities into class labels?
- When is logistic regression a strong baseline?
- How does regularization change the model?

## Related Concepts
- Classification
- Regularization

## Connections
- Depends on: probability, linear predictor, maximum likelihood estimation
- Used in: classification, risk scoring, customer churn
- Related: classification accuracy, precision, recall, regularization

## Prerequisites
- Linear Regression
- Probability

## Further Reading
- James, Witten, Hastie, Tibshirani, An Introduction to Statistical Learning
- scikit-learn logistic regression documentation

## Slide-derived Evidence
- BT4240 | p52 | [L2-Regression.pdf](../data/raw/BT4240/L2-Regression.pdf#page=52) — 7. Logistic regression and π, the logistic regression model can be stated as finding parameters β and β such that: It is assumed that there is only one independent variable/descriptive feature: simple logistic regression. The discussion to follow
- CS3244 | p30 | [Lecture04_linear_models_svm.pdf](../data/raw/CS3244/Lecture04_linear_models_svm.pdf#page=30) — Logistic regression Logistic regression predicts “soft” classes, i.e. is interpreted as a probability of class [0,1].
- CS3244 | p47 | [Lecture04_linear_models_svm.pdf](../data/raw/CS3244/Lecture04_linear_models_svm.pdf#page=47) — and differentiable (as gradient is required), e.g. linear regression, logistic regression, deep learning. GD does not work for discrete losses like win/lose (use differentiable loss, e.g. logistic regression)

## Provenance
- BT4240 | p52 | [L2-Regression.pdf](../data/raw/BT4240/L2-Regression.pdf#page=52) — 7. Logistic regression and π, the logistic regression model can be stated as finding parameters β and β such that: It is assumed that there is only one independent variable/descriptive feature: simple logistic regression. The discussion to follow
- CS3244 | p30 | [Lecture04_linear_models_svm.pdf](../data/raw/CS3244/Lecture04_linear_models_svm.pdf#page=30) — Logistic regression Logistic regression predicts “soft” classes, i.e. is interpreted as a probability of class [0,1].
- CS3244 | p47 | [Lecture04_linear_models_svm.pdf](../data/raw/CS3244/Lecture04_linear_models_svm.pdf#page=47) — and differentiable (as gradient is required), e.g. linear regression, logistic regression, deep learning. GD does not work for discrete losses like win/lose (use differentiable loss, e.g. logistic regression)

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.928
- evidence strength: 0.92
- definition quality: 0.98
- interview relevance: 0.98
- version: 23
- last updated: 2026-08-05T17:21:13.250386+00:00

## Assumptions
- The predictors have a linear relationship with the log-odds of the outcome.
- Observations are independent unless the model explicitly accounts for dependence.
- Perfect separation is absent or handled with an appropriate remedy.
