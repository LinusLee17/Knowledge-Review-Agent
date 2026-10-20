---
concept_name: "Linear Regression"
canonical_key: "linear regression"
concept_type: "model"
domain: "Statistics"
topic: "Regression"
importance_score: 5
scope_level: 3
study_priority: 5
version_number: 26
last_updated_timestamp: "2026-08-05T17:21:13.242941+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Linear Regression

## Classification
- domain: Statistics
- topic: Regression
- type: model
- scope: 3/5 (core concept or method)
- study priority: 5/5
- also known as: least squares regression, ols regression, regression model
- broader topic(s): Statistical Modeling

## Contributing Courses
- BT1101
- BT2101
- BT4240
- CS3244
- ST1131

## Definition
Linear Regression is a statistical modeling method that estimates the relationship between a response variable and one or more predictors by fitting a linear function. It is a baseline method for prediction and inference because coefficients are easy to interpret and the model is simple to diagnose.

## Why it Matters
Linear Regression is a baseline modeling tool in statistics and machine learning. It is valuable because it is simple to interpret, often works well as a first model, and gives a clear view of how features relate to an outcome.

## Core Intuition
Fit the best linear line or plane, then read coefficients as marginal effects under the model assumptions.

## How it Works
1. Represent the outcome as a linear combination of the input features.
2. Fit the coefficients by minimizing squared residuals.
3. Use the fitted line or plane to predict new outcomes and inspect the coefficients for interpretation.

## Mathematical Foundation
$$
\hat{y} = \beta_0 + \beta_1 x_1 + \dots + \beta_p x_p
$$

| Symbol | Meaning |
| --- | --- |
| `\hat{y}` | Predicted value |
| `\beta` | Model coefficients |
| `x` | Input features |
| `\epsilon` | Residual / error term |

## Key Components
- Features
- Target variable
- Coefficients
- Residuals
- Error term
- Least-squares objective

## Advantages
- Simple to fit, explain, and use as a baseline.
- Coefficients provide a direct interpretation of feature effects under the model assumptions.
- Efficient on small and large tabular datasets.

## Limitations
- Sensitive to outliers, influential observations, and multicollinearity.
- Requires checking linearity, independent errors, and constant error variance for reliable inference.
- Can underfit relationships that are substantially nonlinear.

## Common Mistakes
- Treating correlation as causation.
- Ignoring multicollinearity and influential outliers.
- Using the model on clearly nonlinear data without checking fit.

## Common Variants
- Simple Linear Regression
- Multiple Linear Regression
- Polynomial Regression
- Weighted Least Squares

## Real-world Applications
- Business Analytics
- Forecasting
- Prediction

## Interview Questions
- What problem does Linear Regression solve, and what is its output?
- Explain Linear Regression using one concrete input-to-decision example.
- What assumptions must hold before using Linear Regression?
- Which trade-off decides whether to use Linear Regression instead of an alternative?
- How does Linear Regression compare with Lasso Regression?

## Related Concepts
- Lasso Regression
- Logistic Regression
- Regularization
- Ridge Regression

## Connections
- Depends on: features, residuals, least squares, matrix algebra
- Used in: prediction, forecasting, business analytics
- Related: logistic regression, ridge regression, lasso regression, regularization

## Prerequisites
- Matrix Algebra
- Statistics

## Further Reading
- James, Witten, Hastie, Tibshirani, An Introduction to Statistical Learning
- scikit-learn linear regression documentation

## Slide-derived Evidence
- BT1101 | p36-p37 | [Week 7 Linear Regression and Interpretation 2023.pdf](../data/raw/BT1101/Week 7 Linear Regression and Interpretation 2023.pdf#page=36) — Linear Regression Assumptions of Linear Regression Assumptions of Linear Regression Lecture 7 Predictive Analytics: Linear Regression
- BT1101 | p38 | [Week 7 Linear Regression and Interpretation 2023.pdf](../data/raw/BT1101/Week 7 Linear Regression and Interpretation 2023.pdf#page=38) — Linear Regression Assumptions of Linear Regression Lecture 7 Predictive Analytics: Linear Regression Regression Analysis: Simple Linear Regression
- BT2101 | p90, p129, p138, p192 | [BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=90) — Linear Regression • (Quick?) recap of linear regression concepts Interpreting linear regression output
- BT4240 | p44 | [L2-Regression.pdf](../data/raw/BT4240/L2-Regression.pdf#page=44) — • Example: minimizing the negative log-likelihood where p( y |x ,θ) is N(y |x Tθ, σ2) gives us linear regression least
- CS3244 | p47 | [Lecture04_linear_models_svm.pdf](../data/raw/CS3244/Lecture04_linear_models_svm.pdf#page=47) — and differentiable (as gradient is required), e.g. linear regression, logistic regression, deep learning. In comparison, Normal Equations for linear regression

## Provenance
- BT1101 | p36-p37 | [Week 7 Linear Regression and Interpretation 2023.pdf](../data/raw/BT1101/Week 7 Linear Regression and Interpretation 2023.pdf#page=36) — Linear Regression Assumptions of Linear Regression Assumptions of Linear Regression Lecture 7 Predictive Analytics: Linear Regression
- BT1101 | p38 | [Week 7 Linear Regression and Interpretation 2023.pdf](../data/raw/BT1101/Week 7 Linear Regression and Interpretation 2023.pdf#page=38) — Linear Regression Assumptions of Linear Regression Lecture 7 Predictive Analytics: Linear Regression Regression Analysis: Simple Linear Regression
- BT2101 | p90, p129, p138, p192 | [BT2101 Midterms (L1-6).pdf](../data/raw/BT2101/BT2101 Midterms (L1-6).pdf#page=90) — Linear Regression • (Quick?) recap of linear regression concepts Interpreting linear regression output
- BT4240 | p44 | [L2-Regression.pdf](../data/raw/BT4240/L2-Regression.pdf#page=44) — • Example: minimizing the negative log-likelihood where p( y |x ,θ) is N(y |x Tθ, σ2) gives us linear regression least
- CS3244 | p47 | [Lecture04_linear_models_svm.pdf](../data/raw/CS3244/Lecture04_linear_models_svm.pdf#page=47) — and differentiable (as gradient is required), e.g. linear regression, logistic regression, deep learning. In comparison, Normal Equations for linear regression
- ST1131 | p1-p17, p19-p35 | [Topic0_Introduction.pdf](../data/raw/ST1131/Topic0_Introduction.pdf#page=1) — 9 Linear Regression 10 Some Limitations of Linear Regression (extra topic if time permits)
- ST1131 | p18 | [Topic0_Introduction.pdf](../data/raw/ST1131/Topic0_Introduction.pdf#page=18) — 9 Linear Regression 10 Some Limitations of Linear Regression (extra topic if time permits) Topics 1 Introduction to R programming 2 Exploratory Data Analysis (EDA) 3 Collecting Data 4 Probability 5 Random Variables (Discrete and Continuous Random Variables) 6 Sampling Distribution 7 Statistical Estimation 8 Hypothesis Testing 9 Linear Regression 10 Some Limitations of Linear Regression (extra topic if time permits)
- ST1131 | p1, p4-p5, p10-p12, p16, p18-p19, p21-p31, p33-p35, p37, p40-p42, p44, p46-p48, p50-p51, p53-p54, p56-p63, p65-p67, p69-p72, p74, p76-p78, p80, p82-p83, p85-p94 | [Topic9_LinearRegression.pdf](../data/raw/ST1131/Topic9_LinearRegression.pdf#page=1) — Linear Regression and 2 Simple Linear Regression 5 Multiple Linear Regression
- ST1131 | p2-p3, p9, p13-p14, p17, p20, p32, p36, p39, p43, p49, p52, p55, p64, p68, p73, p79, p84 | [Topic9_LinearRegression.pdf](../data/raw/ST1131/Topic9_LinearRegression.pdf#page=2) — 2 Simple Linear Regression 5 Multiple Linear Regression Linear Regression and
- ST1131 | p6 | [Topic9_LinearRegression.pdf](../data/raw/ST1131/Topic9_LinearRegression.pdf#page=6) — Simple Linear Regression Definition 1 (Linear Regression) Linear regression means that this relationship is linear, of the form:
- ST1131 | p7 | [Topic9_LinearRegression.pdf](../data/raw/ST1131/Topic9_LinearRegression.pdf#page=7) — Simple Linear Regression are still linear regression models: The following are not linear regression models:
- ST1131 | p8 | [Topic9_LinearRegression.pdf](../data/raw/ST1131/Topic9_LinearRegression.pdf#page=8) — The Purpose of Simple Linear Regression If we are willing to assume that a simple linear regression of Y on X holds, Linear Regression and
- ST1131 | p15 | [Topic9_LinearRegression.pdf](../data/raw/ST1131/Topic9_LinearRegression.pdf#page=15) — Assumptions for a simple linear regression model Y ∼ X: Linear Regression and 2 Simple Linear Regression
- ST1131 | p38 | [Topic9_LinearRegression.pdf](../data/raw/ST1131/Topic9_LinearRegression.pdf#page=38) — In simple linear regression, there is only one F-test, and it is equivalent to In multiple linear regression (at least two coefficients, except β ), there are Linear Regression and
- ST1131 | p45 | [Topic9_LinearRegression.pdf](../data/raw/ST1131/Topic9_LinearRegression.pdf#page=45) — In a simple linear regression model, the hypotheses of F-test actually are Linear Regression and 2 Simple Linear Regression
- ST1131 | p75 | [Topic9_LinearRegression.pdf](../data/raw/ST1131/Topic9_LinearRegression.pdf#page=75) — The following are differences with simple linear regression: Linear Regression and 2 Simple Linear Regression
- ST1131 | p81 | [Topic9_LinearRegression.pdf](../data/raw/ST1131/Topic9_LinearRegression.pdf#page=81) — Let X denotes transmission type. One possible multiple linear regression Linear Regression and 2 Simple Linear Regression
- ST1131 | p1-p27, p29-p30, p32-p34 | [Topic9_More_Details_R.pdf](../data/raw/ST1131/Topic9_More_Details_R.pdf#page=1) — How does R determine the coe(cid:30)cients for our linear regression model? For a simple linear regression, yˆ= βˆ 0+βˆ 1x, we have e
- ST1131 | p28 | [Topic9_More_Details_R.pdf](../data/raw/ST1131/Topic9_More_Details_R.pdf#page=28) — How does R determine the coe(cid:30)cients for our linear regression model? For a simple linear regression, yˆ= βˆ 0+βˆ 1x, we have e OLS Method How does R determine the coe(cid:30)cients for our linear regression model? It is using the Ordinary Least Squares (OLS) method.
- ST1131 | p31 | [Topic9_More_Details_R.pdf](../data/raw/ST1131/Topic9_More_Details_R.pdf#page=31) — For a simple linear regression, yˆ= βˆ 0+βˆ 1x, we have e How does R determine the coe(cid:30)cients for our linear regression model? Solving Smallest SSR For a simple linear regression, yˆ= βˆ 0+βˆ 1x, we have e = y −(βˆ 0+βˆ 1x ) i i i for each data point. 2 2 2 SSR = e +e +···+e which equates to 1 2 n (cid:16) (cid:17)2 (cid:16) (cid:17)2 (cid:16) (cid:17)2 y1−(βˆ 0+βˆ 1x1) + y2−(βˆ 0+βˆ 1x2) +···+ y −(βˆ 0+βˆ 1x ) . n n βˆ βˆ We will now consider SSR as a function of 0 and 1 and then (cid:28)nd the values for them to minimise SSR. How do we (cid:28)nd those values? βˆ Take derivative of SSR with respect to 0 and set it to 0. βˆ Take derivative of SSR with respect to 1 and set it to 0. βˆ βˆ Solve them to get 0 and 1.

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.953
- evidence strength: 0.98
- definition quality: 0.9
- interview relevance: 0.98
- version: 26
- last updated: 2026-08-05T17:21:13.242941+00:00

## Assumptions
- The expected relationship between predictors and outcome is linear.
- Errors are independent and have constant variance for standard inference.
- Predictors are not perfectly multicollinear.
