---
concept_name: "Maximum Likelihood Estimation"
canonical_key: "maximum likelihood estimation"
concept_type: "method"
domain: "Statistics"
topic: "Estimation"
importance_score: 5
scope_level: 3
study_priority: 5
version_number: 4
last_updated_timestamp: "2026-08-05T17:13:39.203591+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Maximum Likelihood Estimation

## Classification
- domain: Statistics
- topic: Estimation
- type: method
- scope: 3/5 (core concept or method)
- study priority: 5/5
- also known as: maximum likelihood, mle
- broader topic(s): Statistical Inference

## Contributing Courses
- BT3102
- BT4240

## Definition
Maximum Likelihood Estimation chooses the parameter values that make the observed data most probable under the assumed model. It is a core estimation principle that connects probabilistic modeling, log-likelihood, and many classical statistical estimators.

## Why it Matters
Maximum Likelihood Estimation is the core fitting principle behind many statistical and machine learning models. It turns model fitting into a clear optimization problem.

## Core Intuition
Pick the parameters that best explain the observed sample under the model.

## How it Works
1. Choose a probabilistic model with unknown parameters.
2. Write down the likelihood of the observed data under that model.
3. Find the parameter values that maximize the likelihood, usually by maximizing the log-likelihood instead.

## Mathematical Foundation
$$
\hat{\theta} = \arg\max_{\theta} \prod_i p(x_i \mid \theta)
$$

Often we maximize the log-likelihood instead:

$$
\ell(\theta) = \sum_i \log p(x_i \mid \theta)
$$

## Key Components
- Model
- Parameters
- Likelihood
- Log-likelihood
- Optimizer

## Common Mistakes
- Confusing likelihood with the probability of the parameters.
- Forgetting to take the log before optimizing numerically.
- Ignoring whether the model assumptions are actually reasonable.

## Common Variants
- Penalized Likelihood
- Conditional Likelihood
- Profile Likelihood

## Real-world Applications
- Parameter Estimation

## Interview Questions
- What does it mean to maximize a likelihood?
- Why do we usually work with the log-likelihood?
- How is MLE connected to many standard statistical estimators?
- How does MLE differ from MAP estimation?

## Related Concepts
- Log-Likelihood
- Logistic Regression

## Connections
- Depends on: probabilistic model, likelihood, data
- Used in: parameter estimation, logistic regression, probabilistic modeling
- Related: cross-entropy, Bayesian estimation, probability

## Prerequisites
- Probability

## Further Reading
- Casella and Berger, Statistical Inference
- Murphy, Machine Learning: A Probabilistic Perspective

## Slide-derived Evidence
- BT3102 | p10, p36 | [W5-BN-MLE.pdf](../data/raw/BT3102/W5-BN-MLE.pdf#page=10) — ‣ Maximum likelihood estimation is one such learning method ▸ This is known as maximum likelihood learning! Maximum Likelihood Learning: Key Idea
- BT4240 | p41-p42 | [L2-Regression.pdf](../data/raw/BT4240/L2-Regression.pdf#page=41) — 5. Maximum likelihood estimation • Maximum likelihood estimation (MLE): define a function of the parameters θ that enables us to find a model that fits

## Provenance
- BT3102 | p10, p36 | [W5-BN-MLE.pdf](../data/raw/BT3102/W5-BN-MLE.pdf#page=10) — ‣ Maximum likelihood estimation is one such learning method ▸ This is known as maximum likelihood learning! Maximum Likelihood Learning: Key Idea
- BT4240 | p41-p42 | [L2-Regression.pdf](../data/raw/BT4240/L2-Regression.pdf#page=41) — 5. Maximum likelihood estimation • Maximum likelihood estimation (MLE): define a function of the parameters θ that enables us to find a model that fits

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.908
- evidence strength: 0.88
- definition quality: 0.94
- interview relevance: 0.98
- version: 4
- last updated: 2026-08-05T17:13:39.203591+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- assumptions not extracted
- trade-offs or limitations not extracted
