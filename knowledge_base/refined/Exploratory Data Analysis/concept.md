---
concept_name: "Exploratory Data Analysis"
canonical_key: "exploratory data analysis"
concept_type: "workflow"
domain: "Statistics"
topic: "Data Exploration"
importance_score: 4
scope_level: 4
study_priority: 4
version_number: 3
last_updated_timestamp: "2026-08-05T16:27:50.402060+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Exploratory Data Analysis

## Classification
- domain: Statistics
- topic: Data Exploration
- type: workflow
- scope: 4/5 (topic or workflow)
- study priority: 4/5
- also known as: eda
- broader topic(s): Statistical Workflow

## Contributing Courses
- ST1131

## Definition
Exploratory Data Analysis (EDA) is an iterative process for inspecting, summarizing, and visualizing data before—or alongside—formal modeling. It uses graphical and numerical summaries to reveal data quality problems, distributions, unusual observations, and relationships between variables. EDA produces questions and evidence; it does not by itself establish causation.

## Why it Matters
Exploratory Data Analysis turns observations into evidence for Data Exploration, Feature Understanding, helping decide what to investigate or model next.

## Core Intuition
Treat EDA as a feedback loop between question and evidence. Start with what data contains, inspect one variable at a time, then compare variables when a relationship matters. Every plot or summary should answer a question and determine the next check.

## How it Works
1. Define analysis question, target, unit of observation, and decision context.
2. Inspect schema, data types, missing values, duplicates, impossible values, and sampling scope.
3. Summarize each variable with suitable tables, plots, and statistics; inspect distribution shape and outliers.
4. Examine relationships using suitable two-variable plots or summaries; stratify when a third variable may explain the pattern.
5. Investigate anomalies and sensitive findings against raw records and collection context.
6. Record findings, limitations, and next action: clean, transform, collect more data, or fit a model.

## Key Components
- Question and decision context
- Data-quality checks: types, missingness, duplicates, invalid values, and sampling scope
- Univariate summaries: counts, proportions, center, spread, shape, and outliers
- Bivariate summaries: plots and association measures matched to variable types
- Finding log: evidence, uncertainty, limitations, and next action

## Mathematical Foundation
For numeric sample values \(x_1,\ldots,x_n\), the sample mean and variance summarize center and spread:

\[
\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i,
\qquad
s^2=\frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})^2.
\]

For paired numeric variables, sample correlation is:

\[
r_{XY}=\frac{\sum_i(x_i-\bar{x})(y_i-\bar{y})}{\sqrt{\sum_i(x_i-\bar{x})^2}\sqrt{\sum_i(y_i-\bar{y})^2}}.
\]

These summaries describe the observed sample. They do not prove causation, and correlation can be distorted by outliers, nonlinearity, confounding, or selection bias.

## Advantages
- Finds data-quality problems and unexpected structure early.
- Guides feature engineering, model choice, and follow-up questions.
- Makes distribution shape, missingness, and subgroup differences visible.

## Limitations
- Visual patterns can be false discoveries when many plots or slices are inspected.
- Sample association does not establish causal effect.
- Results depend on sampling, measurement quality, transformations, and analyst choices.
- Summaries can hide subgroup structure or important rare cases.

## Common Mistakes
- Treating a convenient plot as proof of causation.
- Deleting outliers or imputing missing values before checking whether they carry signal.
- Reporting only averages and hiding skew, spread, subgroup differences, or sample limitations.
- Using a chart whose scale or encoding exaggerates a pattern.

## Real-world Applications
- Data Exploration
- Feature Understanding

## Interview Questions
- Walk through an EDA workflow for a new dataset. What do you inspect first, and why?
- Which plot and summary would you use for one numeric variable, two numeric variables, and a numeric/categorical pair?
- How would you investigate an outlier before removing it?
- Why does a visible association between two variables not establish causation?
- How can missingness, sampling bias, or subgroup structure change your conclusion?
- Give one example where EDA changes a modeling or data-collection decision.
- How does Exploratory Data Analysis compare with Data Cleaning?

## Related Concepts
- Data Cleaning
- Descriptive Statistics
- Sampling Distribution

## Connections
- Depends on: Data Visualization and Summary Statistics
- Used in: Data Exploration and Feature Understanding
- Related: Data Cleaning, Descriptive Statistics, and Sampling Distribution
- Broader topic: Statistical Workflow

## Prerequisites
- Data Visualization
- Summary Statistics

## Background Enrichment
Standard statistical summaries above provide compact ways to describe center, spread, and linear association. Use them as diagnostic evidence; choose robust or stratified summaries when assumptions or outliers make mean/variance misleading.

## Slide-derived Evidence
- ST1131 | p1 | [Topic2_EDA_1.pdf](../data/raw/ST1131/Topic2_EDA_1.pdf#page=1) — Exploratory Data Analysis These are known as Exploratory Data Analysis (EDA) techniques. Exploratory Data Analysis Part 1
- ST1131 | p2-p3, p5-p39 | [Topic2_EDA_1.pdf](../data/raw/ST1131/Topic2_EDA_1.pdf#page=2) — Exploratory Data Analysis These are known as Exploratory Data Analysis (EDA) techniques.
- ST1131 | p4 | [Topic2_EDA_1.pdf](../data/raw/ST1131/Topic2_EDA_1.pdf#page=4) — Exploratory Data Analysis These are known as Exploratory Data Analysis (EDA) techniques. Exploratory Data Analysis Descriptive statistics are used to summarize a sample. This topic covers graphical and numerical summaries that are the key elements of descriptive statistics. We shall learn ways of describing the information in our sample. These are known as Exploratory Data Analysis (EDA) techniques.

## Provenance
- ST1131 | p1 | [Topic2_EDA_1.pdf](../data/raw/ST1131/Topic2_EDA_1.pdf#page=1) — Exploratory Data Analysis These are known as Exploratory Data Analysis (EDA) techniques. Exploratory Data Analysis Part 1
- ST1131 | p2-p3, p5-p39 | [Topic2_EDA_1.pdf](../data/raw/ST1131/Topic2_EDA_1.pdf#page=2) — Exploratory Data Analysis These are known as Exploratory Data Analysis (EDA) techniques.
- ST1131 | p4 | [Topic2_EDA_1.pdf](../data/raw/ST1131/Topic2_EDA_1.pdf#page=4) — Exploratory Data Analysis These are known as Exploratory Data Analysis (EDA) techniques. Exploratory Data Analysis Descriptive statistics are used to summarize a sample. This topic covers graphical and numerical summaries that are the key elements of descriptive statistics. We shall learn ways of describing the information in our sample. These are known as Exploratory Data Analysis (EDA) techniques.
- `ST1131/Topic0_Introduction/lecture.json` | `fa3141684d21e6896b56ef2ab38c0d98a780a3fdfd52c4b5d9ab048f601bd928`
- `ST1131/Topic2_EDA_2/lecture.json` | `260074d04db6afec6dfc5f513315bf26ed52571542f1ffc2bb781374dc5dca0c`
- `ST1131/Topic2_EDA_3/lecture.json` | `eae4da9cec8b33552056027946b62a93a79b4603a620fbfdae7284c9049d556a`
- `ST1131/Topic2_EDA_4/lecture.json` | `a97eba5d2a99ea33ec54dbbb824384abab81c25b8a491b819da5a3768b37e7fe`
- `ST1131/Topic2_EDA_5/lecture.json` | `88f9524669c95f0f24a6240d27119385c8721a522ada4caa0e711e472e0131d8`

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.939
- evidence strength: 0.98
- definition quality: 0.86
- interview relevance: 0.98
- version: 3
- last updated: 2026-08-05T16:27:50.402060+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- definition lacks specific object, purpose, or scope
- assumptions not extracted
- trade-offs or limitations not extracted
