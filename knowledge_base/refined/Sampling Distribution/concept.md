---
concept_name: "Sampling Distribution"
canonical_key: "sampling distribution"
concept_type: "theory"
domain: "Statistics"
topic: "Inference"
importance_score: 5
scope_level: 4
study_priority: 5
version_number: 4
last_updated_timestamp: "2026-08-05T16:27:50.509243+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Sampling Distribution

## Classification
- domain: Statistics
- topic: Inference
- type: theory
- scope: 4/5 (topic or workflow)
- study priority: 5/5
- broader topic(s): Statistical Inference

## Contributing Courses
- ST1131

## Definition
Sampling Distribution is the probability distribution of a statistic across repeated samples from a population or data-generating process. It is used in Confidence Intervals, Hypothesis Testing.

## Why it Matters
It matters because it provides a concrete way to reason about Confidence Intervals, Hypothesis Testing and choose an appropriate next action.

## Core Intuition
Imagine repeating the same sampling process many times. The statistic changes from sample to sample; its distribution describes that variation and therefore the uncertainty of one observed estimate.

## How it Works
1. Define the random quantity and sampling process.
2. State conditions and parameters.
3. Derive or approximate the distribution or result.
4. Use it to quantify uncertainty and check whether conditions fit the data.

## Mathematical Foundation
> #hist(ave, col = 2, xlab = "Sampling Distribution of X-bar") In Topic 06 (Sampling Distributions), we saw that the variance of X¯ is σ2/n When H is true, p = p , the sampling distribution of pˆ is then

## Key Components
- Random quantity or statistic
- Sampling process
- Probability law or approximation
- Parameters and uncertainty interpretation

## Common Mistakes
- Applying the concept without checking its assumptions or data context.
- Reporting a result without explaining what it measures and what it cannot establish.
- Confusing the concept with a related quantity, method, or decision rule.

## Real-world Applications
- Confidence Intervals
- Hypothesis Testing

## Interview Questions
- What problem does Sampling Distribution solve, and what is its output?
- Explain Sampling Distribution using one concrete input-to-decision example.
- What assumptions must hold before using Sampling Distribution?
- Which trade-off decides whether to use Sampling Distribution instead of an alternative?
- How does Sampling Distribution compare with Central Limit Theorem?

## Related Concepts
- Central Limit Theorem
- Confidence Interval
- Standard Error

## Connections
- Depends on: Random Variable and Probability
- Used in: Confidence Intervals and Hypothesis Testing
- Related: Central Limit Theorem, Standard Error, and Confidence Interval
- Broader topic: Statistical Inference

## Prerequisites
- Probability
- Random Variable

## Slide-derived Evidence
- ST1131 | p18 | [Topic0_Introduction.pdf](../data/raw/ST1131/Topic0_Introduction.pdf#page=18) — 6 Sampling Distribution Topics 1 Introduction to R programming 2 Exploratory Data Analysis (EDA) 3 Collecting Data 4 Probability 5 Random Variables (Discrete and Continuous Random Variables) 6 Sampling Distribution 7 Statistical Estimation 8 Hypothesis Testing 9 Linear Regression 10 Some Limitations of Linear Regression (extra topic if time permits)
- ST1131 | p1, p4-p8, p14-p15, p18, p23-p27, p33, p35, p38, p41, p43, p49 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=1) — Sampling Distributions 2 Sampling Distribution of Sample Proportion pˆ 4 Sampling Distribution of Sample Mean
- ST1131 | p2-p3, p13, p22, p28, p30, p37, p46 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=2) — 2 Sampling Distribution of Sample Proportion pˆ 4 Sampling Distribution of Sample Mean Sampling Distributions
- ST1131 | p9-p10 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=9) — The distribution of a statistic, X¯ or pˆ, is called sampling distribution. Sampling Distribution Sampling Distributions
- ST1131 | p11 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=11) — Sampling Distribution The distribution of a statistic, X¯ or pˆ, is called sampling distribution. Sampling Distributions

## Provenance
- ST1131 | p18 | [Topic0_Introduction.pdf](../data/raw/ST1131/Topic0_Introduction.pdf#page=18) — 6 Sampling Distribution Topics 1 Introduction to R programming 2 Exploratory Data Analysis (EDA) 3 Collecting Data 4 Probability 5 Random Variables (Discrete and Continuous Random Variables) 6 Sampling Distribution 7 Statistical Estimation 8 Hypothesis Testing 9 Linear Regression 10 Some Limitations of Linear Regression (extra topic if time permits)
- ST1131 | p1, p4-p8, p14-p15, p18, p23-p27, p33, p35, p38, p41, p43, p49 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=1) — Sampling Distributions 2 Sampling Distribution of Sample Proportion pˆ 4 Sampling Distribution of Sample Mean
- ST1131 | p2-p3, p13, p22, p28, p30, p37, p46 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=2) — 2 Sampling Distribution of Sample Proportion pˆ 4 Sampling Distribution of Sample Mean Sampling Distributions
- ST1131 | p9-p10 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=9) — The distribution of a statistic, X¯ or pˆ, is called sampling distribution. Sampling Distribution Sampling Distributions
- ST1131 | p11 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=11) — Sampling Distribution The distribution of a statistic, X¯ or pˆ, is called sampling distribution. Sampling Distributions
- ST1131 | p12 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=12) — Sampling Distribution A sampling distribution is merely a type of probability distribution. It The sampling distribution helps us determine how close to the population
- ST1131 | p16 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=16) — Sampling Distribution of pˆ Sampling Distributions 2 Sampling Distribution of Sample Proportion pˆ
- ST1131 | p17 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=17) — sampling distribution of pˆ is. Sampling Distributions 2 Sampling Distribution of Sample Proportion pˆ
- ST1131 | p19 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=19) — Sampling Distribution of pˆ in California Election Hence, the sd of the sampling distribution is estimated as Sampling Distributions
- ST1131 | p20 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=20) — Sampling Distribution of pˆ in California Election Sampling Distributions 2 Sampling Distribution of Sample Proportion pˆ
- ST1131 | p21 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=21) — What is the sampling distribution of pˆ then? Sampling Distributions 2 Sampling Distribution of Sample Proportion pˆ
- ST1131 | p29 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=29) — sampling distribution of the sample mean, X¯. Sampling Distributions 2 Sampling Distribution of Sample Proportion pˆ
- ST1131 | p31 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=31) — We can use the sampling distribution of X¯ to answer this question. Sampling Distributions 2 Sampling Distribution of Sample Proportion pˆ
- ST1131 | p32 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=32) — Sampling Distribution of X in Normal Case Sampling Distributions 2 Sampling Distribution of Sample Proportion pˆ
- ST1131 | p34 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=34) — Some Observations on The Sampling Distribution of X The sampling distribution of X¯ depends on µ, σ2 and n. Sampling Distributions
- ST1131 | p36 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=36) — Sample size is larger −→ the sampling distribution is more peaked −→ X¯ is Sampling Distributions 2 Sampling Distribution of Sample Proportion pˆ
- ST1131 | p39 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=39) — We are interested in the sampling distribution of X¯ from this sample. Sampling Distributions 2 Sampling Distribution of Sample Proportion pˆ
- ST1131 | p40 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=40) — Sampling Distribution of X in Non-Normal Case Hence, the sampling distribution of average monthly income, X¯, is normal Sampling Distributions
- ST1131 | p42 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=42) — Some Observations on the Sampling Distribution of X The sampling distribution of X¯ depends on µ, σ2 and n. Sampling Distributions
- ST1131 | p44 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=44) — the sampling distribution of X¯? Hence, by CLT, the sampling distribution of X¯ is approximated by Conclude: sampling distribution of X¯ is approximated by N(24.9,0.669).
- ST1131 | p45 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=45) — Definition 1 (Sampling Distribution of Sample Mean) deviation σ, the sampling distribution of X¯ has its center equal to the population If the population distribution is not normal, then the sampling distribution
- ST1131 | p47 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=47) — How Knowing the Sampling Distribution Helps When the sampling distribution of X¯ is normal, we 95% sure that a random When n is large, the sampling distribution is approximately normal even if
- ST1131 | p48 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=48) — Non-Normal Sampling Distributions Both the sampling distributions we encountered, for pˆ and for X¯, were shall see that their sampling distributions might not be normal though we
- ST1131 | p1-p3, p5-p6, p8-p9, p11, p13-p16, p18, p20, p22 | [Topic6_SamplingDistribution_R.pdf](../data/raw/ST1131/Topic6_SamplingDistribution_R.pdf#page=1) — Sampling Distributions in R Sampling Distribution • Sampling Distribution
- ST1131 | p4 | [Topic6_SamplingDistribution_R.pdf](../data/raw/ST1131/Topic6_SamplingDistribution_R.pdf#page=4) — Sampling Distribution Sampling Distributions in R • Sampling Distribution
- ST1131 | p7 | [Topic6_SamplingDistribution_R.pdf](../data/raw/ST1131/Topic6_SamplingDistribution_R.pdf#page=7) — • Sampling Distribution Sampling Distributions in R Sampling Distribution
- ST1131 | p10 | [Topic6_SamplingDistribution_R.pdf](../data/raw/ST1131/Topic6_SamplingDistribution_R.pdf#page=10) — simulated sampling distribution by using the histogram of the 10000 sample Sampling Distributions in R Sampling Distribution
- ST1131 | p12 | [Topic6_SamplingDistribution_R.pdf](../data/raw/ST1131/Topic6_SamplingDistribution_R.pdf#page=12) — simulated sampling distribution of the sample mean change? Sampling Distributions in R Sampling Distribution
- ST1131 | p17, p19 | [Topic6_SamplingDistribution_R.pdf](../data/raw/ST1131/Topic6_SamplingDistribution_R.pdf#page=17) — > #hist(ave, col = 2, xlab = "Sampling Distribution of X-bar") Sampling Distributions in R Sampling Distribution
- ST1131 | p21 | [Topic6_SamplingDistribution_R.pdf](../data/raw/ST1131/Topic6_SamplingDistribution_R.pdf#page=21) — distribution and sampling distribution will look like: Sampling Distributions in R Sampling Distribution
- ST1131 | p1-p15, p17, p20-p40, p42-p62 | [Topic7_CI.pdf](../data/raw/ST1131/Topic7_CI.pdf#page=1) — Sampling Distributions). (cid:73) It is a multiple of the standard deviation of the sampling distribution of the point For instance, when the sampling distribution is approximately Normal, a
- ST1131 | p16 | [Topic7_CI.pdf](../data/raw/ST1131/Topic7_CI.pdf#page=16) — (cid:73) It is a multiple of the standard deviation of the sampling distribution of the point For instance, when the sampling distribution is approximately Normal, a Sampling Distributions).
- ST1131 | p18 | [Topic7_CI.pdf](../data/raw/ST1131/Topic7_CI.pdf#page=18) — Recall that the sampling distribution for sample proportion pˆ was given by Sampling Distributions). (cid:73) It is a multiple of the standard deviation of the sampling distribution of the point
- ST1131 | p19 | [Topic7_CI.pdf](../data/raw/ST1131/Topic7_CI.pdf#page=19) — The exact value of the standard deviation of the sampling distribution of a Sampling Distributions). (cid:73) It is a multiple of the standard deviation of the sampling distribution of the point
- ST1131 | p41 | [Topic7_CI.pdf](../data/raw/ST1131/Topic7_CI.pdf#page=41) — In Topic 06 (Sampling Distributions), we saw that the variance of X¯ is σ2/n Sampling Distributions). (cid:73) It is a multiple of the standard deviation of the sampling distribution of the point
- ST1131 | p1-p18, p20-p22, p24-p63 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=1) — (cid:73) the value of point estimate from the sample, and its sampling distribution, The sample size n is sufficiently large that the sampling distribution of the When H is true, p = p , the sampling distribution of pˆ is then
- ST1131 | p19 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=19) — The sample size n is sufficiently large that the sampling distribution of the (cid:73) the value of point estimate from the sample, and its sampling distribution, When H is true, p = p , the sampling distribution of pˆ is then
- ST1131 | p23 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=23) — When H is true, p = p , the sampling distribution of pˆ is then (cid:73) the value of point estimate from the sample, and its sampling distribution, The sample size n is sufficiently large that the sampling distribution of the

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.953
- evidence strength: 0.98
- definition quality: 0.9
- interview relevance: 0.98
- version: 4
- last updated: 2026-08-05T16:27:50.509243+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- assumptions not extracted
- trade-offs or limitations not extracted
