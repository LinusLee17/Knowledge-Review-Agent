---
concept_name: "p-value"
canonical_key: "p value"
concept_type: "metric"
domain: "Statistics"
topic: "Hypothesis Testing"
importance_score: 5
scope_level: 1
study_priority: 5
version_number: 4
last_updated_timestamp: "2026-08-05T16:27:50.475565+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# p-value

## Classification
- domain: Statistics
- topic: Hypothesis Testing
- type: metric
- scope: 1/5 (specific metric or detail)
- study priority: 5/5
- broader topic(s): Statistical Inference

## Contributing Courses
- ST1131

## Definition
p-value is the probability, assuming the null hypothesis is true, of observing a test statistic at least as extreme as the observed value. It is used in Testing. It is commonly considered alongside Hypothesis Testing, Statistical Significance, Type I Error.

## Why it Matters
It matters because it makes Testing measurable, enabling explicit comparisons and decisions.

## Core Intuition
Think of a hypothesis test as a controlled comparison: state a baseline, measure how far observed data move from it, then account for uncertainty before deciding.

## How it Works
1. Define the target quantity and population.
2. Identify the observed outcomes and denominator.
3. Compute the metric.
4. Interpret its scale with uncertainty, class balance, and decision cost.

## Mathematical Foundation
t = 31.326, df = 122, p-value < 2.2e-16 F = 1.0116, num df = 462, denom df = 267, p-value = 0.9234 t = 7.0568, df = 729, p-value = 3.971e-12 F = 0.67575, num df = 41181, denom df = 24977, p-value < 2.2e-16

## Key Components
- Quantity being measured
- Numerator and denominator
- Scale and uncertainty
- Decision cost or error trade-off

## Common Mistakes
- Applying the concept without checking its assumptions or data context.
- Reporting a result without explaining what it measures and what it cannot establish.
- Confusing the concept with a related quantity, method, or decision rule.

## Real-world Applications
- Testing

## Interview Questions
- What problem does p-value solve, and what is its output?
- Explain p-value using one concrete input-to-decision example.
- What does the denominator of p-value include or exclude?
- What assumptions must hold before using p-value?
- Which trade-off decides whether to use p-value instead of an alternative?
- How does p-value compare with Hypothesis Testing?

## Related Concepts
- Hypothesis Testing
- Statistical Significance
- Type I Error

## Connections
- Depends on: Null Hypothesis and Test Statistic
- Used in: Testing
- Related: Statistical Significance, Hypothesis Testing, and Type I Error
- Broader topic: Statistical Inference

## Prerequisites
- Null Hypothesis
- Test Statistic

## Slide-derived Evidence
- ST1131 | p1-p13, p17-p24, p31-p36, p39-p44, p46, p48-p50, p53-p63 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=1) — Step 4: p-Value is p-value. Step 4: Interpret a p-value
- ST1131 | p14 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=14) — Step 4: Interpret a p-value as p-value. When p-value is very small, either the assumption“H is true”is not correct,
- ST1131 | p15 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=15) — Reports the p-value and summarize how strong the evidence against H . (cid:73) Compare p-value to α. (cid:73) If p-value ≤α, then we reject H . Otherwise we retain (don’t reject) H .
- ST1131 | p16 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=16) — For example, we may decide that we will reject H if the p-value is less than (cid:73) The significance level is a number such that we reject H if the p-value is less Step 4: p-Value
- ST1131 | p25 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=25) — Step 4: p-Value The p-value summaries the evidence against H , and in support of H . Calculate p-value:

## Provenance
- ST1131 | p1-p13, p17-p24, p31-p36, p39-p44, p46, p48-p50, p53-p63 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=1) — Step 4: p-Value is p-value. Step 4: Interpret a p-value
- ST1131 | p14 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=14) — Step 4: Interpret a p-value as p-value. When p-value is very small, either the assumption“H is true”is not correct,
- ST1131 | p15 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=15) — Reports the p-value and summarize how strong the evidence against H . (cid:73) Compare p-value to α. (cid:73) If p-value ≤α, then we reject H . Otherwise we retain (don’t reject) H .
- ST1131 | p16 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=16) — For example, we may decide that we will reject H if the p-value is less than (cid:73) The significance level is a number such that we reject H if the p-value is less Step 4: p-Value
- ST1131 | p25 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=25) — Step 4: p-Value The p-value summaries the evidence against H , and in support of H . Calculate p-value:
- ST1131 | p26 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=26) — p-Value Alternative hypothesis p-Value Step 4: p-Value
- ST1131 | p27 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=27) — Step 4: p-Value for California Election Example Using the N(0,1) curve, we can see that the p-value (for H : p > 0.5 ) is the Step 4: p-Value
- ST1131 | p28 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=28) — Step 4: p-Value for California Election Example What would the p-value for this two-sided test be? > # p-value
- ST1131 | p29 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=29) — We summarize the test by reporting and interpreting the p-value in the If a significance level α is given, we compare p-value with α to conclude on Step 4: p-Value
- ST1131 | p30 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=30) — Consider the right-sided test (H : p > 0.5 ) the p-value of 0.0000552 is Step 4: p-Value is p-value.
- ST1131 | p37 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=37) — Step 4: p-Value The p-value depends on whether the alternative hypothesis is one- or Alternative hypothesis p-Value
- ST1131 | p38 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=38) — We summarize the test by reporting and interpreting the p-value in the reject H by comparing p-value with α. Step 4: p-Value
- ST1131 | p45 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=45) — Step 4, p-value: two-sided test (from Step 2) hence, p-value is the two tails Step 4: p-Value is p-value.
- ST1131 | p47 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=47) — Since the p-value is much smaller than 0.05, we reject H and conclude that Step 4: p-Value is p-value.
- ST1131 | p51-p52 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=51) — t = 31.326, df = 122, p-value < 2.2e-16 Step 4: p-Value is p-value.
- ST1131 | p1-p14, p17, p19, p21, p23, p26-p28, p33-p38, p43-p45 | [Topic8_HypothesisTest_2.pdf](../data/raw/ST1131/Topic8_HypothesisTest_2.pdf#page=1) — test in R. If the test is significant (has p-value smaller than 0.05), then this Steps 4 and 5: Derive p-Value p-value depends on whether the alternative hypothesis is one- or two-sided.
- ST1131 | p15 | [Topic8_HypothesisTest_2.pdf](../data/raw/ST1131/Topic8_HypothesisTest_2.pdf#page=15) — Steps 4 and 5: Derive p-Value p-value depends on whether the alternative hypothesis is one- or two-sided. Alternative hypothesis p-Value
- ST1131 | p16 | [Topic8_HypothesisTest_2.pdf](../data/raw/ST1131/Topic8_HypothesisTest_2.pdf#page=16) — Interpret the p-value in the context of study. test in R. If the test is significant (has p-value smaller than 0.05), then this Steps 4 and 5: Derive p-Value
- ST1131 | p18 | [Topic8_HypothesisTest_2.pdf](../data/raw/ST1131/Topic8_HypothesisTest_2.pdf#page=18) — F = 1.0116, num df = 462, denom df = 267, p-value = 0.9234 test in R. If the test is significant (has p-value smaller than 0.05), then this Steps 4 and 5: Derive p-Value
- ST1131 | p20 | [Topic8_HypothesisTest_2.pdf](../data/raw/ST1131/Topic8_HypothesisTest_2.pdf#page=20) — t = 7.0568, df = 729, p-value = 3.971e-12 test in R. If the test is significant (has p-value smaller than 0.05), then this Steps 4 and 5: Derive p-Value
- ST1131 | p22 | [Topic8_HypothesisTest_2.pdf](../data/raw/ST1131/Topic8_HypothesisTest_2.pdf#page=22) — Step 4-5: p-value is close to 0 (< 0.0001). Hence, data provide very strong test in R. If the test is significant (has p-value smaller than 0.05), then this Steps 4 and 5: Derive p-Value
- ST1131 | p24 | [Topic8_HypothesisTest_2.pdf](../data/raw/ST1131/Topic8_HypothesisTest_2.pdf#page=24) — significant (having small p-value). test in R. If the test is significant (has p-value smaller than 0.05), then this Steps 4 and 5: Derive p-Value
- ST1131 | p25 | [Topic8_HypothesisTest_2.pdf](../data/raw/ST1131/Topic8_HypothesisTest_2.pdf#page=25) — p-value. test in R. If the test is significant (has p-value smaller than 0.05), then this Steps 4 and 5: Derive p-Value
- ST1131 | p29 | [Topic8_HypothesisTest_2.pdf](../data/raw/ST1131/Topic8_HypothesisTest_2.pdf#page=29) — F = 0.67575, num df = 41181, denom df = 24977, p-value < 2.2e-16 The test has very small p-value, suggests the two samples come from two test in R. If the test is significant (has p-value smaller than 0.05), then this
- ST1131 | p30 | [Topic8_HypothesisTest_2.pdf](../data/raw/ST1131/Topic8_HypothesisTest_2.pdf#page=30) — We rely on R to get the test statistic and p-value of the test. test in R. If the test is significant (has p-value smaller than 0.05), then this Steps 4 and 5: Derive p-Value
- ST1131 | p31 | [Topic8_HypothesisTest_2.pdf](../data/raw/ST1131/Topic8_HypothesisTest_2.pdf#page=31) — t = 85.921, df = 45056, p-value < 2.2e-16 test in R. If the test is significant (has p-value smaller than 0.05), then this Steps 4 and 5: Derive p-Value
- ST1131 | p32, p42 | [Topic8_HypothesisTest_2.pdf](../data/raw/ST1131/Topic8_HypothesisTest_2.pdf#page=32) — p-value of the test is close to 0 (< 0.0001). test in R. If the test is significant (has p-value smaller than 0.05), then this Steps 4 and 5: Derive p-Value
- ST1131 | p39-p40 | [Topic8_HypothesisTest_2.pdf](../data/raw/ST1131/Topic8_HypothesisTest_2.pdf#page=39) — t = 5.4563, df = 31, p-value = 2.902e-06 test in R. If the test is significant (has p-value smaller than 0.05), then this Steps 4 and 5: Derive p-Value
- ST1131 | p41 | [Topic8_HypothesisTest_2.pdf](../data/raw/ST1131/Topic8_HypothesisTest_2.pdf#page=41) — t = 5.4563, df = 31, p-value = 5.803e-06 test in R. If the test is significant (has p-value smaller than 0.05), then this Steps 4 and 5: Derive p-Value
- ST1131 | p1-p18, p20 | [Topic8_QQplots_R.pdf](../data/raw/ST1131/Topic8_QQplots_R.pdf#page=1) — A small p-value would reject H0. We hope for a large p-value for the Normality assumption to hold. With a p-value of 0.01349 < 0.05, the sample does not follow a Normal
- ST1131 | p19 | [Topic8_QQplots_R.pdf](../data/raw/ST1131/Topic8_QQplots_R.pdf#page=19) — With a p-value of 0.01349 < 0.05, the sample does not follow a Normal W = 0.97272, p-value = 0.01349 A small p-value would reject H0.
- ST1131 | p1-p41, p43-p44, p47-p71, p73-p87, p90-p94 | [Topic9_LinearRegression.pdf](../data/raw/ST1131/Topic9_LinearRegression.pdf#page=1) — 4 Step 4: Derive p-value which also can be found from the R output. Test statistic: t = 31.874. The p-value is less than 0.001. and the F-test to test the significance of model have the same p-value.
- ST1131 | p42 | [Topic9_LinearRegression.pdf](../data/raw/ST1131/Topic9_LinearRegression.pdf#page=42) — Test statistic: t = 31.874. The p-value is less than 0.001. 4 Step 4: Derive p-value which also can be found from the R output. and the F-test to test the significance of model have the same p-value.
- ST1131 | p45 | [Topic9_LinearRegression.pdf](../data/raw/ST1131/Topic9_LinearRegression.pdf#page=45) — and the F-test to test the significance of model have the same p-value. 4 Step 4: Derive p-value which also can be found from the R output. Test statistic: t = 31.874. The p-value is less than 0.001.
- ST1131 | p46 | [Topic9_LinearRegression.pdf](../data/raw/ST1131/Topic9_LinearRegression.pdf#page=46) — Test statistic: F = 1016. p-value is less than 0.001. 4 Step 4: Derive p-value which also can be found from the R output. Test statistic: t = 31.874. The p-value is less than 0.001.
- ST1131 | p72 | [Topic9_LinearRegression.pdf](../data/raw/ST1131/Topic9_LinearRegression.pdf#page=72) — (F-test has very small p-value). 4 Step 4: Derive p-value which also can be found from the R output. Test statistic: t = 31.874. The p-value is less than 0.001.
- ST1131 | p88 | [Topic9_LinearRegression.pdf](../data/raw/ST1131/Topic9_LinearRegression.pdf#page=88) — This F-test has test statistic F = 372.5 ∼ F . p-value < 0.00001. 4 Step 4: Derive p-value which also can be found from the R output. Test statistic: t = 31.874. The p-value is less than 0.001.
- ST1131 | p89 | [Topic9_LinearRegression.pdf](../data/raw/ST1131/Topic9_LinearRegression.pdf#page=89) — significant with p-value = 0.125. Normally, we can drop the insignificant 4 Step 4: Derive p-value which also can be found from the R output. Test statistic: t = 31.874. The p-value is less than 0.001.

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.953
- evidence strength: 0.98
- definition quality: 0.9
- interview relevance: 0.98
- version: 4
- last updated: 2026-08-05T16:27:50.475565+00:00

## Assumptions
- We hope for a large p-value for the Normality assumption to hold
- When p-value is very small, either the assumption“H is true”is not correct

## Quality Review
- This page needs human review before treated as authoritative:
- trade-offs or limitations not extracted
