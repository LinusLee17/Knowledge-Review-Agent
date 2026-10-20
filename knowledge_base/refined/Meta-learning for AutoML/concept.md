---
concept_name: "Meta-learning for AutoML"
canonical_key: "meta learning for automl"
concept_type: "method"
domain: "Machine Learning"
topic: "AutoML"
importance_score: 5
scope_level: 3
study_priority: 5
version_number: 12
last_updated_timestamp: "2026-08-05T17:21:13.259567+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Meta-learning for AutoML

## Classification
- domain: Machine Learning
- topic: AutoML
- type: method
- scope: 3/5 (core concept or method)
- study priority: 5/5
- also known as: learning to learn, meta learning, meta-learning
- broader topic(s): Model Selection, Transfer Learning

## Contributing Courses
- Auto-ML

## Definition
Meta-learning for AutoML transfers experience across datasets or tasks. Dataset meta-features and prior trials can warm-start algorithm selection, hyperparameter search, or surrogate models on a new task.

## Why it Matters
Meta-learning reduces repeated search across related tasks. It turns prior AutoML runs into useful information for cold-starting a new dataset.

## Core Intuition
A new dataset should not start from zero when similar datasets have already been solved; reuse their metadata and trial history to get a better starting point.

## How it Works
1. Build a meta-dataset containing dataset descriptors, prior trials, and observed performance.
2. Find related historical tasks or learn a cross-task surrogate.
3. Use that information to warm-start algorithm selection, HPO, or NAS.
4. Update the transferred model with observations from the new dataset and monitor negative transfer.

## Key Components
- Meta-dataset
- Dataset descriptors
- Historical trials
- Task similarity
- Warm start
- Transfer update

## Advantages
- Reduces cold-start cost by reusing experience across datasets.
- Can warm-start search with useful configurations, priors, or algorithm choices.

## Limitations
- Transfer fails when prior datasets are unlike the new task.
- Meta-datasets and trial histories can be expensive to collect and standardize.

## Common Mistakes
- Leaking target-task outcomes into meta-features or meta-training data.
- Assuming warm starts always help instead of checking for negative transfer.
- Confusing similarity in dataset metadata with similarity in the best configuration.

## Real-world Applications
- AutoML
- Automated Machine Learning
- Learning Across Datasets
- Warm Starting

## Interview Questions
- How can prior tasks guide search on a new task?
- What is the difference between meta-features, warm starts, and learned priors?
- What causes negative transfer in meta-learning for AutoML?
- How would you prevent metadata or performance leakage?

## Related Concepts
- Bayesian Optimization
- Dynamic Algorithm Configuration

## Connections
- Depends on: Algorithm Selection and Hyperparameter Optimization
- Used in: Warm Starting, Learning Across Datasets, and Automated Machine Learning
- Related: Dynamic Algorithm Configuration and Bayesian Optimization
- Broader topic: AutoML, Transfer Learning, and Model Selection

## Prerequisites
- Algorithm Selection
- Hyperparameter Optimization

## Slide-derived Evidence
- Auto-ML | p40 | [3_Basic-of-HPO_ALL.pdf](../data/raw/Auto-ML/3_Basic-of-HPO_ALL.pdf#page=40) — Meta-Learning can help to decide which hyperparameters should be tuned in which ranges Similar to the scale, e.g., linear or logarithmic, upper and lower bounds for hyperparameters have to be specified as many optimizers require them Setting these correctly usually requires deeper knowledge about the inner workings of the ML method and a lot of practical experience Furthermore, if λλˆλ ˆˆ is close to the border of ΛΛΛ the ranges should be increased (or a different scale should be selected), but many algorithms do not do this automatically Meta-Learning can help to decide which hyperparameters should be tuned in which ranges
- Auto-ML | p135 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=135) — Multi-task, Multi-fidelity and Meta-learning separate lecture Bayesian optimization has been extended to numerous scenarios: Multi-task, Multi-fidelity and Meta-learning separate lecture → Multi-objective Bayesian optimization separate lecture → Bayesian optimization with safety guarantees [Sui et al. 2015] Directly optimizing for ensemble performance [L´evesque et al. 2016] Combination with local search methods [Taddy et al. 2009; Eriksson et al. 2019] Optimization of arbitrary spaces that can be described by a kernel (e.g., neural network architectures [Kandasamy et al. 2018] or molecules [Griffiths and Hern´andez-Lobato. 2017]) Many more (too many to mention)
- Auto-ML | p4 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=4) — Meta-learning across problems / datasets Sum of little black boxes (cid:73) Each little black box is fast but only yields a noisy estimate (cid:80)N (cid:73) SMAC [Hutter et al. 2011] directly solves argmin c(λλλ,i) λλλ∈ΛΛΛ i=1 (cid:73) Auto-WEKA [Thornton et al, 2013] used this to optimize 10-fold cross-validation performance Meta-learning across problems / datasets
- Auto-ML | p5 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=5) — Meta-learning across problems / datasets Sum of little black boxes (cid:73) Each little black box is fast but only yields a noisy estimate (cid:80)N (cid:73) SMAC [Hutter et al. 2011] directly solves argmin c(λλλ,i) λλλ∈ΛΛΛ i=1 (cid:73) Auto-WEKA [Thornton et al, 2013] used this to optimize 10-fold cross-validation performance Meta-learning across problems / datasets Multi-fidelity optimization
- Auto-ML | p6 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=6) — Meta-learning across problems / datasets Sum of little black boxes (cid:73) Each little black box is fast but only yields a noisy estimate (cid:80)N (cid:73) SMAC [Hutter et al. 2011] directly solves argmin c(λλλ,i) λλλ∈ΛΛΛ i=1 (cid:73) Auto-WEKA [Thornton et al, 2013] used this to optimize 10-fold cross-validation performance Meta-learning across problems / datasets Multi-fidelity optimization Graybox optimization / learning curve prediction

## Provenance
- Auto-ML | p40 | [3_Basic-of-HPO_ALL.pdf](../data/raw/Auto-ML/3_Basic-of-HPO_ALL.pdf#page=40) — Meta-Learning can help to decide which hyperparameters should be tuned in which ranges Similar to the scale, e.g., linear or logarithmic, upper and lower bounds for hyperparameters have to be specified as many optimizers require them Setting these correctly usually requires deeper knowledge about the inner workings of the ML method and a lot of practical experience Furthermore, if λλˆλ ˆˆ is close to the border of ΛΛΛ the ranges should be increased (or a different scale should be selected), but many algorithms do not do this automatically Meta-Learning can help to decide which hyperparameters should be tuned in which ranges
- Auto-ML | p135 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=135) — Multi-task, Multi-fidelity and Meta-learning separate lecture Bayesian optimization has been extended to numerous scenarios: Multi-task, Multi-fidelity and Meta-learning separate lecture → Multi-objective Bayesian optimization separate lecture → Bayesian optimization with safety guarantees [Sui et al. 2015] Directly optimizing for ensemble performance [L´evesque et al. 2016] Combination with local search methods [Taddy et al. 2009; Eriksson et al. 2019] Optimization of arbitrary spaces that can be described by a kernel (e.g., neural network architectures [Kandasamy et al. 2018] or molecules [Griffiths and Hern´andez-Lobato. 2017]) Many more (too many to mention)
- Auto-ML | p4 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=4) — Meta-learning across problems / datasets Sum of little black boxes (cid:73) Each little black box is fast but only yields a noisy estimate (cid:80)N (cid:73) SMAC [Hutter et al. 2011] directly solves argmin c(λλλ,i) λλλ∈ΛΛΛ i=1 (cid:73) Auto-WEKA [Thornton et al, 2013] used this to optimize 10-fold cross-validation performance Meta-learning across problems / datasets
- Auto-ML | p5 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=5) — Meta-learning across problems / datasets Sum of little black boxes (cid:73) Each little black box is fast but only yields a noisy estimate (cid:80)N (cid:73) SMAC [Hutter et al. 2011] directly solves argmin c(λλλ,i) λλλ∈ΛΛΛ i=1 (cid:73) Auto-WEKA [Thornton et al, 2013] used this to optimize 10-fold cross-validation performance Meta-learning across problems / datasets Multi-fidelity optimization
- Auto-ML | p6 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=6) — Meta-learning across problems / datasets Sum of little black boxes (cid:73) Each little black box is fast but only yields a noisy estimate (cid:80)N (cid:73) SMAC [Hutter et al. 2011] directly solves argmin c(λλλ,i) λλλ∈ΛΛΛ i=1 (cid:73) Auto-WEKA [Thornton et al, 2013] used this to optimize 10-fold cross-validation performance Meta-learning across problems / datasets Multi-fidelity optimization Graybox optimization / learning curve prediction
- Auto-ML | p7 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=7) — Describe many different ways of using meta-learning to speed up HPO Describe many different ways of using meta-learning to speed up HPO Explain the concept of multi-fidelity optimization to speed up HPO Explain the Successive Halving and Hyperband algorithms Explain how to combine Bayesian optimization and Hyperband in BOHB Describe how to exploit multiple fidelities in Bayesian optimization Discuss several ways of predicting learning curves Discuss success stories of speeding up Bayesian optimization
- Auto-ML | p9 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=9) — For a good introduction to meta-learning in general, see [AutoML Book: Chapter 2] Learning essentially never stops: (cid:73) Many models are periodically re-fit to track changes in the data (cid:73) Many models are re-fit to perform well on new tasks The best hyperparameter configuration tends to remain quite stable across tasks For a good introduction to meta-learning in general, see [AutoML Book: Chapter 2]
- Auto-ML | p10 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=10) — Goal of meta-learning: Given: a set of prior tasks: t , j meta ∈ T ⊂ T a set of new tasks: t , new ∈ T a set of learning algorithms, fully defined by θ Θ i ∈ a set of prior evaluations on t meta j meta D ∈ T a set of evaluations on new task t new new D Goal of meta-learning: use meta-data to choose θ Θ for t better than only based on . meta i new new D ∈ D [adapted from AutoML Book: Chapter 2]
- Auto-ML | p13 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=13) — Meta-Learning for HPO Approach 1: Warmstarting
- Auto-ML | p14 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=14) — Meta-Learning for HPO Approach 2: Model-Warmstarting
- Auto-ML | p15-p16 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=15) — Meta-Learning for HPO Approach 3: Task-independent Recommendations
- Auto-ML | p17-p18 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=17) — This uses meta-learning for Meta-Learning for HPO Approach 4: Meta-Learning for HPO Approach 4: Joint model for Bayesian optimization
- Auto-ML | p19 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=19) — Meta-Learning for HPO Approach 4: This uses meta-learning for Meta-Learning for HPO Approach 4: Joint model for Bayesian optimization
- Auto-ML | p20 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=20) — Meta-Learning for HPO Approach 5: Meta-Learning for HPO Approach 5: Learning a Black-box Optimization Algorithm from Data
- Auto-ML | p21 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=21) — Meta-Learning for HPO Approach 6: Learning Algorithm Parts
- Auto-ML | p22 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=22) — Discussion. In the various meta-learning approaches, what will happen if all prior tasks are Repetition. What are the different kinds of meta-features which can be used to describe machine learning datasets? Repetition. List all the different ways of using the meta data for HPO you recall Discussion. In the various meta-learning approaches, what will happen if all prior tasks are dissimilar to the target task?
- Auto-ML | p75 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=75) — Figure: Bayesian optimization with meta-learning (RGPE) vs. vanilla Bayesian optimization (GP) Large-scale Meta-Learning for HPO in Industry (Facebook) (cid:73) For efficiency: meta-learning Bayesian optimization, as described in [Feurer et al. 2018]
- Auto-ML | p76 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=76) — Uses meta-learning to warmstart Bayesian optimization Extension of Auto-WEKA with focus on speed improvements and robustness: AutoML Bayesianoptimizer system { X train ,Y train , meta- datapre- feature classifier build Yˆ X test ,b, L} learning processor preprocessor ensemble test MLframework Uses meta-learning to warmstart Bayesian optimization Won the 1st AutoML challenge Open source (BSD) and trivial to use Available at https://automl.github.io/auto-sklearn; frequently used in industry
- Auto-ML | p78 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=78) — Uses task-independent meta-learning to warmstart Bayesian optimization Idea: integrate warmstarting and a BOHB-like approach for Auto-sklearn Uses task-independent meta-learning to warmstart Bayesian optimization (cid:73) Therefore, no need for (potentially unreliable) meta-features Uses successive halving to quickly go through proposed configurations (cid:73) Therefore, scales better to larger datasets Followed by BOHB-like approach (uses successive halving instead of Hyperband) Won the 2nd AutoML challenge
- Auto-ML | p17 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=17) — Learning to Learn: L2L Dynamic Adaptation of Hyperparameters The goal is to dynamically adapt hyperparameters based on some feedback from the algorithm. Dynamic Algorithm Configuration: DAC The goal of DAC is to learn a policy from data that adapts the hyperparameter settings of an IOH. Learning to Learn: L2L The goal of L2L is to learn a proposal mechanism from data. (Not covered in this lecture.)
- Auto-ML | p54 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=54) — Meta-learning across datasets Multi-fidelity optimization Learning curve prediction Meta-learning across datasets Network morphisms & weight inheritance Weight sharing & the one-shot model
- Auto-ML | p60 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=60) — Only little work on meta-learning for NAS NAS Speedup Technique 3: Meta-Learning Lots of work on meta-learning for HPO
- Auto-ML | p131 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=131) — - Meta-learning + multi-fidelity NAS is fast, but is still a very young field Hyperparameter optimization is a mature field - Blackbox HPO has been researched for decades; there are many software packages - Multi-fidelity HPO has also become quite mature Neural architecture search is still a very young field - Blackbox is quite mature, but slow - Multi-fidelity NAS is also quite mature and faster - Meta-learning + multi-fidelity NAS is fast, but is still a very young field - Gradient-based NAS is fast, but can have failure modes with terrible performance - Gradient-based NAS hasn’t reached the hands-o↵ AutoML stage yet NAS is mainly used to create new architectures that many others can reuse Given a new dataset, HPO is crucial for good performance; NAS may not be necessary - The biggest gains typically come from tuning key hyperparameters (learning rate, etc) - Reusing a previous achitecture often yields competitive results
- Auto-ML | p133 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=133) — - Meta-learning with Joint Architecture Search and Hyperparameter Optimization - Purely using HPO techniques: very similar methods as in Auto-sklearn 2.0 - Multi-fidelity optimization with BOHB - Meta-learning with task-independent recommendations - Ensembling of neural nets and traditional ML
- Auto-ML | p18 | [w01_t01_04_big_picture.pdf](../data/raw/Auto-ML/w01_t01_04_big_picture.pdf#page=18) — Machine learning, Meta-Learning Professor at Eindhoven University of Technology (Netherlands) Machine learning, Meta-Learning Co-Founder of www.openml.org Co-Editor of book on Automated Machine Learning: Methods, Systems, Challenges

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.675
- evidence strength: 0.82
- definition quality: 0.28
- interview relevance: 0.98
- version: 12
- last updated: 2026-08-05T17:21:13.259567+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- assumptions not extracted
