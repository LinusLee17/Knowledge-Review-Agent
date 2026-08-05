---
concept_name: "Standard Error"
canonical_key: "standard error"
concept_type: "metric"
domain: "Statistics"
topic: "Inference"
importance_score: 5
scope_level: 1
study_priority: 5
version_number: 8
last_updated_timestamp: "2026-08-05T17:17:19.418071+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Standard Error

## Classification
- domain: Statistics
- topic: Inference
- type: metric
- scope: 1/5 (specific metric or detail)
- study priority: 5/5
- also known as: se
- broader topic(s): Statistical Inference

## Contributing Courses
- BT1101
- BT2101
- ST1131

## Definition
Standard Error measures the sampling variability of an estimator; smaller standard error means the estimator varies less across repeated samples. It is used in Uncertainty Quantification. It is commonly considered alongside Confidence Interval, Margin of Error, Sampling Distribution.

## Why it Matters
It matters because it makes Uncertainty Quantification measurable, enabling explicit comparisons and decisions.

## Core Intuition
A metric compresses several observed outcomes into one number. Meaning comes from what it counts, what it divides by, and which error or decision it emphasizes.

## How it Works
1. Define the target quantity and population.
2. Identify the observed outcomes and denominator.
3. Compute the metric.
4. Interpret its scale with uncertainty, class balance, and decision cost.

## Mathematical Foundation
SE of mean = if population standard deviation (𝜎) is known SE of mean = if population standard deviation (𝜎) is unknown, use an

## Key Components
- Quantity being measured
- Numerator and denominator
- Scale and uncertainty
- Decision cost or error trade-off

## Advantages
- Also known as robust standard errors
- Different formula for computing standard errors of coefficient estimates
- Simplifying tip: always use robust standard errors
- Standard Error Regression Coefficients
- coefficients, and identical standard errors

## Common Mistakes
- Applying the concept without checking its assumptions or data context.
- Reporting a result without explaining what it measures and what it cannot establish.
- Confusing the concept with a related quantity, method, or decision rule.

## Real-world Applications
- Uncertainty Quantification

## Interview Questions
- What problem does Standard Error solve, and what is its output?
- Explain Standard Error using one concrete input-to-decision example.
- What does the denominator of Standard Error include or exclude?
- What assumptions must hold before using Standard Error?
- Which trade-off decides whether to use Standard Error instead of an alternative?
- How does Standard Error compare with Confidence Interval?

## Related Concepts
- Confidence Interval
- Margin of Error
- Sampling Distribution

## Connections
- Depends on: Sampling Distribution
- Used in: Uncertainty Quantification
- Related: Margin of Error, Confidence Interval, and Sampling Distribution
- Broader topic: Statistical Inference

## Prerequisites
- Sampling Distribution

## Slide-derived Evidence
- BT1101 | p16 | [Week 7 Linear Regression and Interpretation 2023.pdf](../data/raw/BT1101/Week 7 Linear Regression and Interpretation 2023.pdf#page=16) — • Standard Error Regression Coefficients •Describe Multiple R, R-square, Adjusted R-square, standard error of Fitting of data Standard Error of the estimates
- BT2101 | p60 | [BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=60) — • Standard error of the sample mean n Sample mean Standard Standard Error • Standard error of 𝛽 and 𝛽 can be used for hypothesis testing
- BT2101 | p168 | [BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=168) — • Different formula for computing standard errors of coefficient estimates • But they affect the standard errors of those estimates! • Also known as robust standard errors
- BT2101 | p17 | [VK.wk10.2024.pdf](../data/raw/BT2101/VK.wk10.2024.pdf#page=17) — coefficients, and identical standard errors. heteroscedasticity-robust standard errors)
- ST1131 | p1-p20, p22-p46, p48-p49 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=1) — which is called standard error of pˆ. Will the standard error of pˆ be remained the same? our best estimate for σ. The term (s/ n) is called standard error of X¯.

## Provenance
- BT1101 | p16 | [Week 7 Linear Regression and Interpretation 2023.pdf](../data/raw/BT1101/Week 7 Linear Regression and Interpretation 2023.pdf#page=16) — • Standard Error Regression Coefficients •Describe Multiple R, R-square, Adjusted R-square, standard error of Fitting of data Standard Error of the estimates
- BT2101 | p60 | [BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=60) — • Standard error of the sample mean n Sample mean Standard Standard Error • Standard error of 𝛽 and 𝛽 can be used for hypothesis testing
- BT2101 | p168 | [BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=168) — • Different formula for computing standard errors of coefficient estimates • But they affect the standard errors of those estimates! • Also known as robust standard errors
- BT2101 | p17 | [VK.wk10.2024.pdf](../data/raw/BT2101/VK.wk10.2024.pdf#page=17) — coefficients, and identical standard errors. heteroscedasticity-robust standard errors)
- ST1131 | p1-p20, p22-p46, p48-p49 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=1) — which is called standard error of pˆ. Will the standard error of pˆ be remained the same? our best estimate for σ. The term (s/ n) is called standard error of X¯.
- ST1131 | p21 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=21) — Will the standard error of pˆ be remained the same? which is called standard error of pˆ. our best estimate for σ. The term (s/ n) is called standard error of X¯.
- ST1131 | p47 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=47) — our best estimate for σ. The term (s/ n) is called standard error of X¯. which is called standard error of pˆ. Will the standard error of pˆ be remained the same?
- ST1131 | p1-p19, p21-p22, p24-p62 | [Topic7_CI.pdf](../data/raw/ST1131/Topic7_CI.pdf#page=1) — The standard error of a sample proportion is then pˆ(1−pˆ)/n. Assume n is large enough. Let SE denote the standard error of pˆ then
- ST1131 | p20 | [Topic7_CI.pdf](../data/raw/ST1131/Topic7_CI.pdf#page=20) — The standard error of a sample proportion is then pˆ(1−pˆ)/n. Assume n is large enough. Let SE denote the standard error of pˆ then Back to Formula for Population Proportion (cid:112) The standard error of a sample proportion is then pˆ(1−pˆ)/n. Definition 4 (Confidence Interval for Proportion) A 95% confidence interval for a population proportion p is (cid:114) pˆ(1−pˆ) pˆ±1.96× n where pˆ denotes the sample proportion based on n observations. This formula should be used only when n is sufficiently large that npˆ(1−pˆ) ≥ 5.
- ST1131 | p23 | [Topic7_CI.pdf](../data/raw/ST1131/Topic7_CI.pdf#page=23) — Assume n is large enough. Let SE denote the standard error of pˆ then The standard error of a sample proportion is then pˆ(1−pˆ)/n. Where Did 1.96 Come From? Assume n is large enough. Let SE denote the standard error of pˆ then (cid:0) SE2(cid:1) pˆ−p pˆ ∼ N p, , hence, ∼ N(0,1). SE From N(0,1), we have pˆ−p P(−1.96 ≤ ≤ 1.96) = 0.95, which is equivalent to SE (cid:16) (cid:17) P pˆ−1.96SE ≤ p ≤ pˆ+1.96SE = 0.95
- ST1131 | p1-p43, p45-p48, p50-p63 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=1) — Usually, this distance is measured by the number of standard errors between The observed sample mean X¯ is approximately 31.3 standard errors away both the CI and the test use the same standard error.
- ST1131 | p44 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=44) — The observed sample mean X¯ is approximately 31.3 standard errors away Usually, this distance is measured by the number of standard errors between both the CI and the test use the same standard error.
- ST1131 | p49 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=49) — both the CI and the test use the same standard error. Usually, this distance is measured by the number of standard errors between The observed sample mean X¯ is approximately 31.3 standard errors away
- ST1131 | p58 | [Topic9_LinearRegression.pdf](../data/raw/ST1131/Topic9_LinearRegression.pdf#page=58) — standard error of (Y −Yˆ) Standardized Residuals Different types of residual mentioned in the previous slide typically yield the same information, hence we shall use the standardized residuals (SR) (r ) i from now on. Y −Yˆ standardized residual = standard error of (Y −Yˆ)

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.953
- evidence strength: 0.98
- definition quality: 0.9
- interview relevance: 0.98
- version: 8
- last updated: 2026-08-05T17:17:19.418071+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- assumptions not extracted
- trade-offs or limitations not extracted
