---
concept_name: "Algorithm Selection"
canonical_key: "algorithm selection"
concept_type: "method"
domain: "Machine Learning"
topic: "AutoML"
importance_score: 5
scope_level: 3
study_priority: 5
version_number: 1
last_updated_timestamp: "2026-08-05T17:21:13.097455+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Algorithm Selection

## Classification
- domain: Machine Learning
- topic: AutoML
- type: method
- scope: 3/5 (core concept or method)
- study priority: 5/5
- also known as: automated algorithm selection, model selection
- broader topic(s): Model Selection

## Contributing Courses
- Auto-ML

## Definition
Algorithm Selection maps a problem or dataset to an algorithm from a portfolio. In per-instance selection, meta-features and prior performance are used to choose the algorithm expected to minimize a task-specific cost.

## Why it Matters
Algorithm selection is the first AutoML decision: choose which learner should receive tuning effort. A good selector can outperform a fixed default across heterogeneous datasets.

## Core Intuition
Different datasets favor different algorithms; learn a mapping from dataset evidence to the best member of an algorithm portfolio.

## How it Works
1. Define an algorithm portfolio and a task-specific cost metric.
2. Describe the dataset with meta-features or representative training information.
3. Learn or estimate the performance of portfolio members on similar tasks.
4. Map the new dataset to an algorithm, then evaluate the selected algorithm under the target protocol.

## Mathematical Foundation
$$
s: D \rightarrow A, \qquad s(D) = \arg\min_{a \in A} c(a,D)
$$

`D` is a dataset or problem, `A` an algorithm portfolio, and `c` the task-specific cost.

## Key Components
- Algorithm portfolio
- Dataset meta-features
- Cost metric
- Performance model
- Selection mapping
- Evaluation protocol

## Advantages
- Uses a portfolio instead of assuming one algorithm wins on every dataset.
- Can exploit dataset meta-features and prior benchmark results.

## Limitations
- A portfolio cannot select an algorithm absent from the portfolio.
- Meta-features and historical results may fail to transfer to a distribution-shifted dataset.

## Common Mistakes
- Leaving strong candidate algorithms out of the portfolio before selection begins.
- Using test outcomes or future workload information as meta-features.
- Ignoring distribution shift between benchmark instances used for training and deployment.

## Real-world Applications
- Automated Machine Learning
- Pipeline Design

## Interview Questions
- How does algorithm selection map a dataset instance to a candidate algorithm?
- What makes a useful meta-feature for algorithm selection?
- How is algorithm selection different from hyperparameter optimization?
- How would you avoid leakage across related benchmark instances?

## Related Concepts
- Hyperparameter Optimization
- Meta-learning for AutoML

## Connections
- Depends on: Model Evaluation and Cross Validation
- Used in: Automated Machine Learning and Pipeline Design
- Related: Hyperparameter Optimization and Meta-learning for AutoML
- Broader topic: AutoML and Model Selection

## Prerequisites
- Model Evaluation
- Cross Validation

## Slide-derived Evidence
- Auto-ML | p162 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=162) — First general AutoML system, carrying out Combined Algorithm Selection and First general AutoML system, carrying out Combined Algorithm Selection and Hyperparameter optimization (CASH), jointly optimizing Choice of algorithm (out of 26 classifiers) I The algorithm’s hyperparameters (up to 10) I Choice of preprocessing method and its hyperparameters I Choice of ensemble & meta methods I
- Auto-ML | p163 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=163) — First general AutoML system, carrying out Combined Algorithm Selection and First general AutoML system, carrying out Combined Algorithm Selection and Hyperparameter optimization (CASH), jointly optimizing Choice of algorithm (out of 26 classifiers) I The algorithm’s hyperparameters (up to 10) I Choice of preprocessing method and its hyperparameters I Choice of ensemble & meta methods I Parameterized WEKA [Frank et al, 2016]: 768 hyperparameters, 4 leves of conditionality
- Auto-ML | p164 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=164) — First general AutoML system, carrying out Combined Algorithm Selection and First general AutoML system, carrying out Combined Algorithm Selection and Hyperparameter optimization (CASH), jointly optimizing Choice of algorithm (out of 26 classifiers) I The algorithm’s hyperparameters (up to 10) I Choice of preprocessing method and its hyperparameters I Choice of ensemble & meta methods I Parameterized WEKA [Frank et al, 2016]: 768 hyperparameters, 4 leves of conditionality Optimized 10-fold cross-validation via SMAC [Hutter et al, 2011]
- Auto-ML | p165 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=165) — First general AutoML system, carrying out Combined Algorithm Selection and First general AutoML system, carrying out Combined Algorithm Selection and Hyperparameter optimization (CASH), jointly optimizing Choice of algorithm (out of 26 classifiers) I The algorithm’s hyperparameters (up to 10) I Choice of preprocessing method and its hyperparameters I Choice of ensemble & meta methods I Parameterized WEKA [Frank et al, 2016]: 768 hyperparameters, 4 leves of conditionality Optimized 10-fold cross-validation via SMAC [Hutter et al, 2011] Results: Better than an oracle of the 26 base classifiers with default hyperparameters I 100 faster than grid search over base classifiers, and still better in 14/21 cases I × Better than the only other applicable method TPE in 19/21 cases I Impact for practitioners: Auto-WEKA plugin was downloaded tens of thousands of times
- Auto-ML | p166 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=166) — Discussion. Recall the algorithm selection problem; how does CASH relate to this (after all, it also has “algorithm selection” as part of its name)? (Hint: they are quite different.) Repetition. List several success stories of Bayesian optimization Repetition. List several prominent tools for Bayesian optimization Discussion. Recall the algorithm selection problem; how does CASH relate to this (after all, it also has “algorithm selection” as part of its name)? (Hint: they are quite different.)

## Provenance
- Auto-ML | p162 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=162) — First general AutoML system, carrying out Combined Algorithm Selection and First general AutoML system, carrying out Combined Algorithm Selection and Hyperparameter optimization (CASH), jointly optimizing Choice of algorithm (out of 26 classifiers) I The algorithm’s hyperparameters (up to 10) I Choice of preprocessing method and its hyperparameters I Choice of ensemble & meta methods I
- Auto-ML | p163 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=163) — First general AutoML system, carrying out Combined Algorithm Selection and First general AutoML system, carrying out Combined Algorithm Selection and Hyperparameter optimization (CASH), jointly optimizing Choice of algorithm (out of 26 classifiers) I The algorithm’s hyperparameters (up to 10) I Choice of preprocessing method and its hyperparameters I Choice of ensemble & meta methods I Parameterized WEKA [Frank et al, 2016]: 768 hyperparameters, 4 leves of conditionality
- Auto-ML | p164 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=164) — First general AutoML system, carrying out Combined Algorithm Selection and First general AutoML system, carrying out Combined Algorithm Selection and Hyperparameter optimization (CASH), jointly optimizing Choice of algorithm (out of 26 classifiers) I The algorithm’s hyperparameters (up to 10) I Choice of preprocessing method and its hyperparameters I Choice of ensemble & meta methods I Parameterized WEKA [Frank et al, 2016]: 768 hyperparameters, 4 leves of conditionality Optimized 10-fold cross-validation via SMAC [Hutter et al, 2011]
- Auto-ML | p165 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=165) — First general AutoML system, carrying out Combined Algorithm Selection and First general AutoML system, carrying out Combined Algorithm Selection and Hyperparameter optimization (CASH), jointly optimizing Choice of algorithm (out of 26 classifiers) I The algorithm’s hyperparameters (up to 10) I Choice of preprocessing method and its hyperparameters I Choice of ensemble & meta methods I Parameterized WEKA [Frank et al, 2016]: 768 hyperparameters, 4 leves of conditionality Optimized 10-fold cross-validation via SMAC [Hutter et al, 2011] Results: Better than an oracle of the 26 base classifiers with default hyperparameters I 100 faster than grid search over base classifiers, and still better in 14/21 cases I × Better than the only other applicable method TPE in 19/21 cases I Impact for practitioners: Auto-WEKA plugin was downloaded tens of thousands of times
- Auto-ML | p166 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=166) — Discussion. Recall the algorithm selection problem; how does CASH relate to this (after all, it also has “algorithm selection” as part of its name)? (Hint: they are quite different.) Repetition. List several success stories of Bayesian optimization Repetition. List several prominent tools for Bayesian optimization Discussion. Recall the algorithm selection problem; how does CASH relate to this (after all, it also has “algorithm selection” as part of its name)? (Hint: they are quite different.)
- Auto-ML | p1 | [7_ss23_automl_algo_sel_ALL.pdf](../data/raw/Auto-ML/7_ss23_automl_algo_sel_ALL.pdf#page=1) — AutoML: Algorithm Selection AutoML: Algorithm Selection Overview and Motivation Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p2 | [7_ss23_automl_algo_sel_ALL.pdf](../data/raw/Auto-ML/7_ss23_automl_algo_sel_ALL.pdf#page=2) — Algorithm Selection [Rice, John R. “The Algorithm Selection Problem.” Advances in Computers 15 (1976): 65–118.] Given a problem, choose the best algorithm to solve it. [Rice, John R. “The Algorithm Selection Problem.” Advances in Computers 15 (1976): 65–118.]
- Auto-ML | p3 | [7_ss23_automl_algo_sel_ALL.pdf](../data/raw/Auto-ML/7_ss23_automl_algo_sel_ALL.pdf#page=3) — Algorithm Selection the per-instance algorithm selection problem is to obtain a mapping s : D (cid:55)→ A such that More formally Let p(D) be a probability distribution over datasets D ∈ D, P a portfolio of algorithms A ∈ P, and c : P×D → R be a cost metric the per-instance algorithm selection problem is to obtain a mapping s : D (cid:55)→ A such that (cid:90) argmin c(s(D),D)p(D)dD s D
- Auto-ML | p6 | [7_ss23_automl_algo_sel_ALL.pdf](../data/raw/Auto-ML/7_ss23_automl_algo_sel_ALL.pdf#page=6) — AutoML: Algorithm Selection Algorithm Selection AutoML: Algorithm Selection Algorithm Selection Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p7, p16, p24 | [7_ss23_automl_algo_sel_ALL.pdf](../data/raw/Auto-ML/7_ss23_automl_algo_sel_ALL.pdf#page=7) — Algorithm Selection
- Auto-ML | p12 | [7_ss23_automl_algo_sel_ALL.pdf](../data/raw/Auto-ML/7_ss23_automl_algo_sel_ALL.pdf#page=12) — Building an Algorithm Selection System
- Auto-ML | p14 | [7_ss23_automl_algo_sel_ALL.pdf](../data/raw/Auto-ML/7_ss23_automl_algo_sel_ALL.pdf#page=14) — Key Components of an Algorithm Selection System
- Auto-ML | p15 | [7_ss23_automl_algo_sel_ALL.pdf](../data/raw/Auto-ML/7_ss23_automl_algo_sel_ALL.pdf#page=15) — AutoML: Algorithm Selection AutoML: Algorithm Selection Features Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p23 | [7_ss23_automl_algo_sel_ALL.pdf](../data/raw/Auto-ML/7_ss23_automl_algo_sel_ALL.pdf#page=23) — AutoML: Algorithm Selection AutoML: Algorithm Selection Performance Models Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p32 | [7_ss23_automl_algo_sel_ALL.pdf](../data/raw/Auto-ML/7_ss23_automl_algo_sel_ALL.pdf#page=32) — AutoML: Algorithm Selection AutoML: Algorithm Selection Bonus: Combinatorial Problems Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p33 | [7_ss23_automl_algo_sel_ALL.pdf](../data/raw/Auto-ML/7_ss23_automl_algo_sel_ALL.pdf#page=33) — Algorithm Selection applied in many other domains Algorithm Selection applied in many other domains success and performance improvements for combinatorial and optimization problems in AI dwarfs those in machine learning important application area of AI facilitating cross-disciplinary collaborations and advances
- Auto-ML | p39 | [7_ss23_automl_algo_sel_ALL.pdf](../data/raw/Auto-ML/7_ss23_automl_algo_sel_ALL.pdf#page=39) — Hoos, et al. “ASlib: A Benchmark Library for Algorithm Selection.” Artificial Intelligence Journal (AIJ), no. https://github.com/coseal/aslib_data SAT, CSP, QBF, ASP, MAXSAT, OR, ML... includes data used frequently in the literature that you may want to evaluate your approach on more scenarios in the pipeline http://aslib.net [ Bischl, Bernd, Pascal Kerschke, Lars Kotthoff, Marius Lindauer, Yuri Malitsky, Alexandre Fr´echette, Holger H. Hoos, et al. “ASlib: A Benchmark Library for Algorithm Selection.” Artificial Intelligence Journal (AIJ), no. 237 (2016): 41–58. ]
- Auto-ML | p41 | [7_ss23_automl_algo_sel_ALL.pdf](../data/raw/Auto-ML/7_ss23_automl_algo_sel_ALL.pdf#page=41) — [Kotthoff, Lars. “Algorithm Selection for Combinatorial Search Problems: A Survey.” AI Magazine 35, no. 3 http://larskotthoff.github.io/assurvey/ [Kotthoff, Lars. “Algorithm Selection for Combinatorial Search Problems: A Survey.” AI Magazine 35, no. 3 (2014): 48–60.]
- Auto-ML | p15 | [w01_t01_04_big_picture.pdf](../data/raw/Auto-ML/w01_t01_04_big_picture.pdf#page=15) — Organizer of competitions on algorithm selection Professor at the University of Wyoming (USA) Head of the Meta-Algorithmics, Learning and Large-Scale Empirical Testing lab (MALLET) and director of the Artificially Intelligent Manufacturing Center (AIM) Developer of MLR (Machine Learning in R) Organizer of competitions on algorithm selection Co-Editor of book on Automated Machine Learning: Methods, Systems, Challenges
- Auto-ML | p25 | [w01_t01_04_big_picture.pdf](../data/raw/Auto-ML/w01_t01_04_big_picture.pdf#page=25) — CASH: Combined Algorithm Selection and CASH: Combined Algorithm Selection and Hyperparameter Optimization
- Auto-ML | p28 | [w01_t01_04_big_picture.pdf](../data/raw/Auto-ML/w01_t01_04_big_picture.pdf#page=28) — the per-instance algorithm selection problem is to obtain a mapping s : such that Per-Instance Algorithm Selection For solving the HPO, CASH and NAS problem, we use some kind of optimization approach to search for a solution A different view: Can we learn from data and thus predict an algorithm/ hyperparameter configuration/ neural architecture? Definition Let p( ) be a probability distribution over datasets D, D D ∈ P a portfolio of algorithms P, and A ∈ c : P D R be a cost metric × → the per-instance algorithm selection problem is to obtain a mapping s : such that D 7→ A argmin c(s( ), )p( )d D D D D s ZD

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.857
- evidence strength: 0.8
- definition quality: 0.84
- interview relevance: 0.98
- version: 1
- last updated: 2026-08-05T17:21:13.097455+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- assumptions not extracted
