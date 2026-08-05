---
concept_name: "Hyperparameter Optimization"
canonical_key: "hyperparameter optimization"
concept_type: "workflow"
domain: "Machine Learning"
topic: "AutoML"
importance_score: 5
scope_level: 4
study_priority: 5
version_number: 13
last_updated_timestamp: "2026-08-05T17:21:13.209312+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Hyperparameter Optimization

## Classification
- domain: Machine Learning
- topic: AutoML
- type: workflow
- scope: 4/5 (topic or workflow)
- study priority: 5/5
- also known as: HPO, hyperparameter optimisation, hyperparameter tuning
- broader topic(s): Model Selection, Optimization

## Contributing Courses
- Auto-ML

## Definition
Hyperparameter Optimization (HPO) searches a defined configuration space for hyperparameters that minimize a validation cost. Unlike learned model parameters, hyperparameters control the training procedure or model structure, so each trial requires training and evaluating a model.

## Why it Matters
HPO is the outer optimization loop around model training. It determines whether an AutoML system finds a strong pipeline within a fixed evaluation budget rather than relying on arbitrary defaults.

## Core Intuition
Treat each configuration as an expensive experiment: choose a setting, train/evaluate it, learn from the result, and spend the next budget where improvement is most plausible.

## How it Works
1. Define the configuration space, including parameter types, bounds, conditional branches, and forbidden combinations.
2. Choose a validation cost, usually from a train/validation split or cross-validation protocol.
3. Select a configuration, train the pipeline, and record cost, runtime, resource use, and status.
4. Use random search, model-based search, or a multi-fidelity scheduler to choose the next trial.
5. Stop at the budget limit and report the best configuration on an untouched test evaluation.

## Mathematical Foundation
$$
\lambda^* = \arg\min_{\lambda \in \Lambda} c(A_\lambda, D_{train}, D_{valid})
$$

`\Lambda` is the search space, `\lambda` a configuration, and `c` the validation cost of the trained model.

## Key Components
- Configuration space
- Hyperparameters
- Validation objective
- Trial evaluator
- Search strategy
- Budget and stopping rule

## Advantages
- Improves a model or pipeline without requiring manual trial-and-error for every configuration.
- Can optimize mixed continuous, discrete, and conditional search spaces.
- Makes the search objective and compute budget explicit.

## Limitations
- Search can be extremely expensive because every trial may require model training and validation.
- Validation overfitting can occur when many configurations are tested against the same validation signal.
- Results depend on the search space, budget, random seed, and evaluation protocol.

## Common Mistakes
- Tuning on the test set or reporting the same validation score used for search.
- Making the search space so broad that most budget goes to implausible configurations.
- Treating hyperparameters like learned weights, rather than choices evaluated by retraining.

## Real-world Applications
- Automated Machine Learning
- Model Tuning
- Pipeline Optimization

## Interview Questions
- Why is hyperparameter optimization an outer loop around model training?
- How do random search, Bayesian optimization, and multi-fidelity search differ?
- Why must the test set remain outside the search loop?
- How would you allocate a fixed compute budget across configurations?

## Related Concepts
- Algorithm Selection
- Bayesian Optimization
- Multi-fidelity Optimization
- Neural Architecture Search

## Connections
- Depends on: Model Evaluation and Cross Validation
- Used in: Model Tuning, Automated Machine Learning, and Pipeline Optimization
- Related: Bayesian Optimization, Multi-fidelity Optimization, and Algorithm Selection
- Broader topic: AutoML, Model Selection, and Optimization

## Prerequisites
- Cross Validation
- Model Evaluation

## Slide-derived Evidence
- Auto-ML | p1 | [3_Basic-of-HPO_ALL.pdf](../data/raw/Auto-ML/3_Basic-of-HPO_ALL.pdf#page=1) — AutoML: Hyperparameter Optimization AutoML: Hyperparameter Optimization Overview and Introduction Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p9 | [3_Basic-of-HPO_ALL.pdf](../data/raw/Auto-ML/3_Basic-of-HPO_ALL.pdf#page=9) — is nested within the outer hyperparameter optimization (also called second-level problem): We face a bi-level optimization problem: The well-known risk minimization problem to find fˆ is nested within the outer hyperparameter optimization (also called second-level problem):
- Auto-ML | p11 | [3_Basic-of-HPO_ALL.pdf](../data/raw/Auto-ML/3_Basic-of-HPO_ALL.pdf#page=11) — We formally state the nested hyperparameter tuning problem as: We formally state the nested hyperparameter tuning problem as: minc(λλλ) = G(cid:100)E (I(D ,λλλ)) Dtest train λλλ∈ΛΛΛ The learner I(D ,λλλ) takes a training dataset as well as hyperparameter settings ΛΛΛ train (e.g. the maximal depth of a classification tree) as an input. I(D ,λλλ) performs empirical risk minimization on the training data and returns the train optimal model fˆfor the given hyperparameters. Note that for the estimation of the generalization error, more sophisticated resampling strategies like cross-validation can be used.
- Auto-ML | p14 | [3_Basic-of-HPO_ALL.pdf](../data/raw/Auto-ML/3_Basic-of-HPO_ALL.pdf#page=14) — AutoML: Hyperparameter Optimization AutoML: Hyperparameter Optimization Grid and Random Search Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p20 | [3_Basic-of-HPO_ALL.pdf](../data/raw/Auto-ML/3_Basic-of-HPO_ALL.pdf#page=20) — AutoML: Hyperparameter Optimization AutoML: Hyperparameter Optimization Evolutionary Algorithms Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren

## Provenance
- Auto-ML | p1 | [3_Basic-of-HPO_ALL.pdf](../data/raw/Auto-ML/3_Basic-of-HPO_ALL.pdf#page=1) — AutoML: Hyperparameter Optimization AutoML: Hyperparameter Optimization Overview and Introduction Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p9 | [3_Basic-of-HPO_ALL.pdf](../data/raw/Auto-ML/3_Basic-of-HPO_ALL.pdf#page=9) — is nested within the outer hyperparameter optimization (also called second-level problem): We face a bi-level optimization problem: The well-known risk minimization problem to find fˆ is nested within the outer hyperparameter optimization (also called second-level problem):
- Auto-ML | p11 | [3_Basic-of-HPO_ALL.pdf](../data/raw/Auto-ML/3_Basic-of-HPO_ALL.pdf#page=11) — We formally state the nested hyperparameter tuning problem as: We formally state the nested hyperparameter tuning problem as: minc(λλλ) = G(cid:100)E (I(D ,λλλ)) Dtest train λλλ∈ΛΛΛ The learner I(D ,λλλ) takes a training dataset as well as hyperparameter settings ΛΛΛ train (e.g. the maximal depth of a classification tree) as an input. I(D ,λλλ) performs empirical risk minimization on the training data and returns the train optimal model fˆfor the given hyperparameters. Note that for the estimation of the generalization error, more sophisticated resampling strategies like cross-validation can be used.
- Auto-ML | p14 | [3_Basic-of-HPO_ALL.pdf](../data/raw/Auto-ML/3_Basic-of-HPO_ALL.pdf#page=14) — AutoML: Hyperparameter Optimization AutoML: Hyperparameter Optimization Grid and Random Search Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p20 | [3_Basic-of-HPO_ALL.pdf](../data/raw/Auto-ML/3_Basic-of-HPO_ALL.pdf#page=20) — AutoML: Hyperparameter Optimization AutoML: Hyperparameter Optimization Evolutionary Algorithms Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p37 | [3_Basic-of-HPO_ALL.pdf](../data/raw/Auto-ML/3_Basic-of-HPO_ALL.pdf#page=37) — Conceptually simple, yet powerful enough to solve complex problems (including HPO) Not perfectly suited for expensive problems like HPO, as quite a higher number of Advantages Conceptually simple, yet powerful enough to solve complex problems (including HPO) All parameter types possible in general Highly parallelizable (depends on µ) Allows customization via specific variation operators Disadvantages Less theory available (for realistic, complex EAs) Can be hard to get balance between exploration and exploitation right Can have quite a few control parameters, hard to set them correctly Customization necessary for complex problems Not perfectly suited for expensive problems like HPO, as quite a higher number of evaluations is usually needed for appropriate convergence / progress
- Auto-ML | p38 | [3_Basic-of-HPO_ALL.pdf](../data/raw/Auto-ML/3_Basic-of-HPO_ALL.pdf#page=38) — AutoML: Hyperparameter Optimization AutoML: Hyperparameter Optimization Example and Practical Hints Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p1 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=1) — AutoML: Bayesian Optimization for HPO AutoML: Bayesian Optimization for HPO Overview of Bayesian Optimization Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p2-p4 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=2) — Blackbox optimization can be used for hyperparameter optimization (HPO) Note: for formulations of HPO that go beyond blackbox optimization, see next lecture
- Auto-ML | p5 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=5) — Blackbox optimization can be used for hyperparameter optimization (HPO) Consider the global optimization problem of finding: λλλ argminf(λλλ) ∗ ∈ λλλ ΛΛΛ ∈ In the most general form, function f is a blackbox function: λλλ f(λλλ) Only mode of interaction with f: querying f’s value at a givenλλλ I Function f may not be available in closed form, not convex, not differentiable, noisy, etc. I Today, we’ll discuss a Bayesian approach for solving such blackbox optimization problems Blackbox optimization can be used for hyperparameter optimization (HPO) Define f(λλλ):= ( , , ) I λλλ train valid L A D D Note: for formulations of HPO that go beyond blackbox optimization, see next lecture I Note: for formulations of HPO that go beyond blackbox optimization, see next lecture
- Auto-ML | p19 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=19) — hyperparameter optimization? Repetition. What is Bayesian about Bayesian optimization? Repetition. Write down the steps of the BO loop. Discussion. Can you think of an expensive blackbox optimization problem other than hyperparameter optimization?
- Auto-ML | p21 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=21) — AutoML: Bayesian Optimization for HPO AutoML: Bayesian Optimization for HPO Computationally Cheap Acquisition Functions Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p54 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=54) — AutoML: Bayesian Optimization for HPO AutoML: Bayesian Optimization for HPO Computationally Expensive Acquisition Functions Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p85 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=85) — AutoML: Bayesian Optimization for HPO AutoML: Bayesian Optimization for HPO Surrogate Models Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p108 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=108) — Hyperparameter Optimization with Factorized Multilayer Perceptrons [Schilling et al. 2015] Scalable Bayesian Optimization Using Deep Neural Networks (DNGO) [Snoek et al. 2015] Bayesian Optimization with Robust Bayesian Neural Networks [Springenberg et al. 2016] Parallel and Distributed Thompson Sampling for Large-scale Accelerated Exploration of Chemical Space [Hern´andez-Lobato et al. 2017] Hyperparameter Optimization with Factorized Multilayer Perceptrons [Schilling et al. 2015] Scalable Hyperparameter Transfer Learning [Perrone et al. 2018]
- Auto-ML | p114 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=114) — AutoML: Bayesian Optimization for HPO AutoML: Bayesian Optimization for HPO Extensions of Bayesian Optimization Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p137 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=137) — AutoML: Bayesian Optimization for HPO AutoML: Bayesian Optimization for HPO The Tree-Parzen Estimator (TPE) Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p154 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=154) — AutoML: Bayesian Optimization for HPO AutoML: Bayesian Optimization for HPO Success Stories Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p162 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=162) — Hyperparameter optimization (CASH), jointly optimizing First general AutoML system, carrying out Combined Algorithm Selection and Hyperparameter optimization (CASH), jointly optimizing Choice of algorithm (out of 26 classifiers) I The algorithm’s hyperparameters (up to 10) I Choice of preprocessing method and its hyperparameters I Choice of ensemble & meta methods I
- Auto-ML | p163 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=163) — Hyperparameter optimization (CASH), jointly optimizing First general AutoML system, carrying out Combined Algorithm Selection and Hyperparameter optimization (CASH), jointly optimizing Choice of algorithm (out of 26 classifiers) I The algorithm’s hyperparameters (up to 10) I Choice of preprocessing method and its hyperparameters I Choice of ensemble & meta methods I Parameterized WEKA [Frank et al, 2016]: 768 hyperparameters, 4 leves of conditionality
- Auto-ML | p164 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=164) — Hyperparameter optimization (CASH), jointly optimizing First general AutoML system, carrying out Combined Algorithm Selection and Hyperparameter optimization (CASH), jointly optimizing Choice of algorithm (out of 26 classifiers) I The algorithm’s hyperparameters (up to 10) I Choice of preprocessing method and its hyperparameters I Choice of ensemble & meta methods I Parameterized WEKA [Frank et al, 2016]: 768 hyperparameters, 4 leves of conditionality Optimized 10-fold cross-validation via SMAC [Hutter et al, 2011]
- Auto-ML | p165 | [4_BO-for-HPO_all.pdf](../data/raw/Auto-ML/4_BO-for-HPO_all.pdf#page=165) — Hyperparameter optimization (CASH), jointly optimizing First general AutoML system, carrying out Combined Algorithm Selection and Hyperparameter optimization (CASH), jointly optimizing Choice of algorithm (out of 26 classifiers) I The algorithm’s hyperparameters (up to 10) I Choice of preprocessing method and its hyperparameters I Choice of ensemble & meta methods I Parameterized WEKA [Frank et al, 2016]: 768 hyperparameters, 4 leves of conditionality Optimized 10-fold cross-validation via SMAC [Hutter et al, 2011] Results: Better than an oracle of the 26 base classifiers with default hyperparameters I 100 faster than grid search over base classifiers, and still better in 14/21 cases I × Better than the only other applicable method TPE in 19/21 cases I Impact for practitioners: Auto-WEKA plugin was downloaded tens of thousands of times
- Auto-ML | p1, p8, p23, p32, p38, p53, p60, p74 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=1) — Speedup Techniques for Hyperparameter Optimization
- Auto-ML | p7 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=7) — Describe many different ways of using meta-learning to speed up HPO Explain the concept of multi-fidelity optimization to speed up HPO Describe many different ways of using meta-learning to speed up HPO Explain the concept of multi-fidelity optimization to speed up HPO Explain the Successive Halving and Hyperband algorithms Explain how to combine Bayesian optimization and Hyperband in BOHB Describe how to exploit multiple fidelities in Bayesian optimization Discuss several ways of predicting learning curves Discuss success stories of speeding up Bayesian optimization
- Auto-ML | p13 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=13) — Experts often start HPO from a strong default (rather than random configurations) Meta-Learning for HPO Approach 1: Warmstarting Can we learn from meta-data how to initialize HPO?
- Auto-ML | p14 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=14) — By running HPO on different datasets, we learn something about the search landscape Meta-Learning for HPO Approach 2: Model-Warmstarting Many HPO methods use a predictive model (e.g., Bayesian optimization)
- Auto-ML | p15-p16 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=15) — Meta-Learning for HPO Approach 3: Task-independent Recommendations
- Auto-ML | p17-p19 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=17) — Meta-Learning for HPO Approach 4: Meta-Learning for HPO Approach 4: Joint model for Bayesian optimization
- Auto-ML | p20 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=20) — Meta-Learning for HPO Approach 5: Meta-Learning for HPO Approach 5: Learning a Black-box Optimization Algorithm from Data
- Auto-ML | p21 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=21) — Meta-Learning for HPO Approach 6: Learning Algorithm Parts
- Auto-ML | p22 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=22) — Repetition. List all the different ways of using the meta data for HPO you recall Repetition. What are the different kinds of meta-features which can be used to describe machine learning datasets? Repetition. List all the different ways of using the meta data for HPO you recall Discussion. In the various meta-learning approaches, what will happen if all prior tasks are dissimilar to the target task?
- Auto-ML | p39 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=39) — Robust and Efficient Hyperparameter Optimization at Scale
- Auto-ML | p48 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=48) — Figure: Hyperparameter optimization of 8 hyperparameters of PPO on the cartpole task.
- Auto-ML | p75 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=75) — Large-scale Meta-Learning for HPO in Industry (Facebook)
- Auto-ML | p82 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=82) — Practical Recommendations Which HPO Method to Use (cid:70) CMA-ES [Hansen et al., since 2001]; evaluated for HPO by [Loshchilov & Hutter, ICLR WS Practical Recommendations Which HPO Method to Use [Feurer & Hutter, 2019]
- Auto-ML | p84 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=84) — Survey on hyperparameter optimization: [Feurer and Hutter 2019]
- Auto-ML | p54 | [6_Multicriteria_ALL.pdf](../data/raw/Auto-ML/6_Multicriteria_ALL.pdf#page=54) — Problem: Feature selection and hyperparameter tuning are usually two separate steps. Goal of feature selection: Identify an informative feature subset with only a small drop in predictive performance compared to all features. Find optimal hyperparameter setting λλλ and minimal feature subset s (cid:32) p (cid:33) 1 (cid:88) min G(cid:100)E(I(D,λλλ,s)), s i λλλ∈ΛΛΛ,s∈{0,1}p p i=1 Problem: Feature selection and hyperparameter tuning are usually two separate steps. Solution: Identify an informative subset of features and a good hyperparameter configuration simultaneously.
- Auto-ML | p55 | [6_Multicriteria_ALL.pdf](../data/raw/Auto-ML/6_Multicriteria_ALL.pdf#page=55) — Idea: Multi-Objective Hyperparameter Tuning and Feature Selection using Filter Idea: Multi-Objective Hyperparameter Tuning and Feature Selection using Filter Ensembles [Moosbauer, Binder, et al. 2020]: Pre-calculate multiple ranked feature filter values . New joint hyperparameter vector: λλλ = (λλλ ˜ ,w ,...,w ,τ) 1 p (cid:73) Hyperparameters of learner: λλλ˜ (cid:73) Weight of each feature filter value vector: (w ,...,w ) 1 p (cid:73) Fraction of features to keep τ
- Auto-ML | p56 | [6_Multicriteria_ALL.pdf](../data/raw/Auto-ML/6_Multicriteria_ALL.pdf#page=56) — Combined feature selection and hyperparameter optimization on Sonar dataset2. Combined feature selection and hyperparameter optimization on Sonar dataset2. Learning algorithm: SVM with RBF kernel. detceles Hyperparameters to optimize: cost [2−10,210] γ [2−10,210] serutaef (w ,...,w ) [0,1]p 1 p τ [0,1]p Objective: minimize misclassification and fraction of fo noitcarF features selected Optimizer: ParEGO with random forest surrogate, LCB acquisition function, 15 batch proposals, budget: 2000 evaluations 2Only the tuning error is shown here
- Auto-ML | p37 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=37) — ⇝ Use HPO to optimize these three continuous hyperparameters Adaptively changing hyperparameters itself is not a new idea Often heuristics are designed manually Example: cosine annealing learning rates [Loshchilov and Hutter. 2016] (cid:18) (cid:18) (cid:19)(cid:19) 1 T cur η = η + (η −η ) 1+cos ·3.141592 (1) t min max min 2 T max Hyperparameters: η initial (maximal) learning rate max η Minimal learning rate min T Maximum number of iterations (i.e. restart of learning rate) max ⇝ Use HPO to optimize these three continuous hyperparameters
- Auto-ML | p27 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=27) — NAS as Hyperparameter Optimization NAS can be formulated as a HPO problem
- Auto-ML | p28 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=28) — NAS as Hyperparameter Optimization NAS can be formulated as a HPO problem NAS can be formulated as a HPO problem E.g., cell search space by [Zoph et al. 2018] has 5 categorical choices per block 2 categorical choices of hidden states I F For block N, the domain of these categorical variables is h ,h ,output of block 1,...,output of block N 1 i i 1 { } 2 categorical variables choosing between operations I 1 categorical variable choosing the combination method I Total number of hyperparameters for the cell: I 5B (with B=5 by default)
- Auto-ML | p29 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=29) — NAS as Hyperparameter Optimization NAS can be formulated as a HPO problem NAS can be formulated as a HPO problem E.g., cell search space by [Zoph et al. 2018] has 5 categorical choices per block 2 categorical choices of hidden states I F For block N, the domain of these categorical variables is h ,h ,output of block 1,...,output of block N 1 i i 1 { } 2 categorical variables choosing between operations I 1 categorical variable choosing the combination method I Total number of hyperparameters for the cell: I 5B (with B=5 by default) In general: one may require conditional hyperparameters E.g., chain-structured search space I F Top-level hyperparameter: number of layers L F Hyperparameters of layer k conditional on L k
- Auto-ML | p42 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=42) — Evolution simply tackles this as a HPO problem with 2 5 B variables: 2 types of cells: normal and reduction cells For each type of cell: B blocks, each with 5 choices - Choose two previous feature maps (from this cell) - For each of these, choose an operation (3 3 conv, max-pool, etc.) ⇥ - Choose a merge operation to combine the two results (concat or add) Evolution simply tackles this as a HPO problem with 2 5 B variables: ⇥ ⇥
- Auto-ML | p44 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=44) — Same fixed-length (HPO) search space as used for RL [Zoph et al. 2018] Quite standard evolutionary algorithm But oldest solutions are dropped from population, instead of the worst I Standard SGD for training weights (optimizing the same blackbox as RL) Same fixed-length (HPO) search space as used for RL [Zoph et al. 2018] Di↵erent types of mutations in cell search space
- Auto-ML | p45 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=45) — Same fixed-length (HPO) search space as used for RL [Zoph et al. 2018] Quite standard evolutionary algorithm But oldest solutions are dropped from population, instead of the worst I Standard SGD for training weights (optimizing the same blackbox as RL) Same fixed-length (HPO) search space as used for RL [Zoph et al. 2018] State-of-the-art performance in Di↵erent types of mutations in cell apples-to-apples comparison search space AmoebaNet
- Auto-ML | p52 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=52) — How can NAS be modelled as a HPO problem? How would you write NAS with the hierarchical search space as a HPO problem? Repetition: What are some pros and cons of using black-box optimizers for NAS? Repetition: How can NAS be modelled as a HPO problem? Discussion: Given enough resources, will blackbox NAS approaches always improve performance? Discussion: Why does discarding the oldest individual (rather than the worst) help in regularized/aging evolution? Transfer: How would you write NAS with the hierarchical search space as a HPO problem?
- Auto-ML | p55 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=55) — Analogous to multi-fidelity optimization in HPO Analogous to multi-fidelity optimization in HPO - Many evaluations for cheaper fidelities (less epochs, smaller datasets, down-sampled images, shallower networks, etc) - Fewer evaluations necessary for more expensive fidelities
- Auto-ML | p56 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=56) — Analogous to multi-fidelity optimization in HPO Analogous to multi-fidelity optimization in HPO - Many evaluations for cheaper fidelities (less epochs, smaller datasets, down-sampled images, shallower networks, etc) - Fewer evaluations necessary for more expensive fidelities Compatible with any blackbox optimization method - Using random search: ASHA [Li and Talwalkar. 2019] - Using Bayesian optimization: BOHB [Zela et al. 2018] - Using di↵erential evolution: DEHB [Awad et al. under review] - Using regularized evolution: progressive dynamic hurdles [So et al. 2019]
- Auto-ML | p57 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=57) — Analogous to multi-fidelity optimization in HPO Analogous to multi-fidelity optimization in HPO - Many evaluations for cheaper fidelities (less epochs, smaller datasets, down-sampled images, shallower networks, etc) - Fewer evaluations necessary for more expensive fidelities Compatible with any blackbox optimization method - Using random search: ASHA [Li and Talwalkar. 2019] - Using Bayesian optimization: BOHB [Zela et al. 2018] - Using di↵erential evolution: DEHB [Awad et al. under review] - Using regularized evolution: progressive dynamic hurdles [So et al. 2019] Often used for joint optimization of architecture & hyperparameters - Auto-Pytorch [Mendoza et al. 2019; Zimmer et al. 2020] - “Auto-RL” [Runge et al. 2019]
- Auto-ML | p58 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=58) — Analogous to learning curve prediction in HPO Analogous to learning curve prediction in HPO - Observe initial learning curve and predict performance at the end - Can use features of the architecture as input (just like hyperparameters as inputs)
- Auto-ML | p59 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=59) — Analogous to learning curve prediction in HPO Analogous to learning curve prediction in HPO - Observe initial learning curve and predict performance at the end - Can use features of the architecture as input (just like hyperparameters as inputs) Often used for joint optimization of architecture & hyperparameters Compatible with any blackbox optimization method - Using random search and Bayesian optimization: [Domhan et al. 2015] - Using reinforcement learning: [Baker et al. 2018]
- Auto-ML | p60 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=60) — Lots of work on meta-learning for HPO Lots of work on meta-learning for HPO Only little work on meta-learning for NAS - Find a set of good architectures to initialize BOHB in Auto-Pytorch [Zimmer et al. 2020] - Learn RL agent’s policy network on previous datasets [Wong et al. 2018] - Learn neural architecture that can be quickly adapted [Lian et al. 2019; Elsken et al. 2019]
- Auto-ML | p73 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=73) — Which speedup techniques directly carry over from HPO to NAS? Why do network morphisms and the one-shot model only apply to NAS, and not to HPO? Repetition: List five methods to speed up NAS over blackbox approaches Repetition: Which speedup techniques directly carry over from HPO to NAS? Discussion: Why do network morphisms and the one-shot model only apply to NAS, and not to HPO?
- Auto-ML | p130 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=130) — Practical Recommendations for NAS and HPO
- Auto-ML | p131 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=131) — Hyperparameter optimization is a mature field Hyperparameter optimization is a mature field - Blackbox HPO has been researched for decades; there are many software packages - Multi-fidelity HPO has also become quite mature Neural architecture search is still a very young field - Blackbox is quite mature, but slow - Multi-fidelity NAS is also quite mature and faster - Meta-learning + multi-fidelity NAS is fast, but is still a very young field - Gradient-based NAS is fast, but can have failure modes with terrible performance - Gradient-based NAS hasn’t reached the hands-o↵ AutoML stage yet NAS is mainly used to create new architectures that many others can reuse Given a new dataset, HPO is crucial for good performance; NAS may not be necessary - The biggest gains typically come from tuning key hyperparameters (learning rate, etc) - Reusing a previous achitecture often yields competitive results Maturity of the Fields of NAS and HPO
- Auto-ML | p132 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=132) — + If you don’t have decent hyperparameters: first run HPO to get competitive Practical Recommendations for NAS and HPO Always run HPO
- Auto-ML | p133 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=133) — Joint Architecture Search and Hyperparameter Optimization - Purely using HPO techniques: very similar methods as in Auto-sklearn 2.0 - Multi-fidelity optimization with BOHB - Meta-learning with task-independent recommendations - Ensembling of neural nets and traditional ML Case Study: NAS & HPO in Auto-PyTorch Tabular - Purely using HPO
- Auto-ML | p134 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=134) — Case Study: NAS & HPO in Auto-DispNet Both NAS and HPO improved the state of the art Subsequent HPO: 2.14 1.94 (by BOHB)
- Auto-ML | p135 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=135) — If you want to use both HPO and NAS for your problem, how could you proceed? you use to combine HPO and NAS, and why? Repetition: If you want to use both HPO and NAS for your problem, how could you proceed? Discussion: Think of a problem of your particular interest. For that problem, which approach would you use to combine HPO and NAS, and why?
- Auto-ML | p23 | [w01_t01_04_big_picture.pdf](../data/raw/Auto-ML/w01_t01_04_big_picture.pdf#page=23) — Hyperparameter Optimization The hyper-parameter optimization (HPO) problem is to find a hyper-parameter configuration Definition Let λλλ be the hyperparameters of an ML algorithm with domain ΛΛΛ, A be a dataset which is split into and opt train val D D D c( , , ) denote the cost of trained on and evaluated on . λλλ train valid λλλ train val A D D A D D The hyper-parameter optimization (HPO) problem is to find a hyper-parameter configuration that minimizes this cost: λλλ argminc( , , ) ∗ λλλ train valid ∈ A D D λλλ ΛΛΛ ∈ Remarks: argmin returns a set of optimal points of a given function. It suffices to find one element of this set and thus we use instead of =. ∈ Sometimes, we want to optimize for different metrics, instead of one multi-objective optimization and Pareto fronts
- Auto-ML | p25 | [w01_t01_04_big_picture.pdf](../data/raw/Auto-ML/w01_t01_04_big_picture.pdf#page=25) — Hyperparameter Optimization CASH: Combined Algorithm Selection and Hyperparameter Optimization
- Auto-ML | p27 | [w01_t01_04_big_picture.pdf](../data/raw/Auto-ML/w01_t01_04_big_picture.pdf#page=27) — very similar to the HPO definition In practice, you want jointly optimize HPO and NAS [Zela et al. 2018] Definition Let λλλ be an architecture for a deep neural network N with domain ΛΛΛ, be a dataset which is split into and opt train valid D D D c(N , , ) denote the cost of N trained on and evaluated on . λλλ train valid λλλ train valid D D D D The neural architecture search (NAS) problem is to find an architecture that minimizes this cost: λλλ argminc(N , , ) ∗ λλλ train valid ∈ D D λλλ ΛΛΛ ∈ Remark: very similar to the HPO definition In practice, you want jointly optimize HPO and NAS [Zela et al. 2018]
- Auto-ML | p28 | [w01_t01_04_big_picture.pdf](../data/raw/Auto-ML/w01_t01_04_big_picture.pdf#page=28) — For solving the HPO, CASH and NAS problem, we use some kind of optimization For solving the HPO, CASH and NAS problem, we use some kind of optimization approach to search for a solution A different view: Can we learn from data and thus predict an algorithm/ hyperparameter configuration/ neural architecture? Definition Let p( ) be a probability distribution over datasets D, D D ∈ P a portfolio of algorithms P, and A ∈ c : P D R be a cost metric × → the per-instance algorithm selection problem is to obtain a mapping s : such that D 7→ A argmin c(s( ), )p( )d D D D D s ZD
- Auto-ML | p30 | [w01_t01_04_big_picture.pdf](../data/raw/Auto-ML/w01_t01_04_big_picture.pdf#page=30) — HPO Search for the best hyperparameter configuration of a ML algorithm HPO Search for the best hyperparameter configuration of a ML algorithm CASH Search for the best combination of algorithm and hyperparameter configuration NAS Search for the architecture of neural network Selection Predict the best algorithm (and its hyperparameter configuration) DAC Predict the best hyperparameter configuration for an algorithm state at a given time point

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.843
- evidence strength: 0.94
- definition quality: 0.7
- interview relevance: 0.98
- version: 13
- last updated: 2026-08-05T17:21:13.209312+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- assumptions not extracted
