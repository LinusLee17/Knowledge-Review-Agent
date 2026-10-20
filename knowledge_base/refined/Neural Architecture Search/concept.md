---
concept_name: "Neural Architecture Search"
canonical_key: "neural architecture search"
concept_type: "workflow"
domain: "Machine Learning"
topic: "AutoML"
importance_score: 5
scope_level: 4
study_priority: 5
version_number: 7
last_updated_timestamp: "2026-08-05T15:34:07.945816+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Neural Architecture Search

## Classification
- domain: Machine Learning
- topic: AutoML
- type: workflow
- scope: 4/5 (topic or workflow)
- study priority: 5/5
- also known as: NAS, neural architecture optimisation, neural architecture optimization
- broader topic(s): Architecture Design, Deep Learning

## Contributing Courses
- Auto-ML

## Definition
Neural Architecture Search (NAS) searches an architecture space for a neural network that performs well on validation data, optionally subject to resource constraints such as training time, memory, or parameter count.

## Why it Matters
NAS automates architecture design, one of the most consequential and expensive choices in deep learning. It also exposes the trade-off between accuracy and deployment resources.

## Core Intuition
Turn architecture design into a search problem: define what structures are legal, generate candidates, estimate their performance, and keep the best under the resource budget.

## How it Works
1. Encode a legal architecture search space: operations, connections, depth, width, or cell structure.
2. Choose a search strategy such as Bayesian optimization, evolutionary search, reinforcement learning, or gradients.
3. Train or estimate each candidate's validation performance, often with a proxy or shared weights.
4. Select a high-performing architecture and verify it with an independent full training run and resource check.

## Mathematical Foundation
$$
\lambda^* = \arg\min_{\lambda \in \Lambda} c(N_\lambda, D_{train}, D_{valid})
$$

`\lambda` encodes an architecture and `N_\lambda` is the resulting neural network; constraints can add runtime, memory, or size objectives.

## Key Components
- Architecture search space
- Architecture encoding
- Search strategy
- Performance estimator
- Resource constraint
- Final retraining

## Advantages
- Automates architecture decisions that otherwise require extensive expert experimentation.
- Can optimize accuracy together with resource constraints.

## Limitations
- The architecture space and training cost can be enormous.
- Weight sharing, proxies, or partial training can bias architecture rankings.

## Common Mistakes
- Treating the search-space design as neutral when it strongly limits possible architectures.
- Trusting weight-sharing or proxy results without retraining selected architectures fairly.
- Comparing architectures without matching parameter count, latency, hardware, and training budget.

## Real-world Applications
- Automated Architecture Design
- Neural Network Design

## Interview Questions
- What are the search space, search strategy, and evaluation strategy in NAS?
- Why can weight sharing make architecture ranking unreliable?
- How would you compare NAS results under a fixed latency or compute budget?
- Why must the selected architecture be retrained before final evaluation?

## Related Concepts
- Meta-learning for AutoML
- Multi-fidelity Optimization

## Connections
- Depends on: Hyperparameter Optimization and Gradient Descent
- Used in: Automated Architecture Design and Neural Network Design
- Related: Meta-learning for AutoML and Multi-fidelity Optimization
- Broader topic: AutoML, Deep Learning, and Architecture Design

## Prerequisites
- Gradient Descent
- Hyperparameter Optimization

## Slide-derived Evidence
- Auto-ML | p81 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=81) — 1 Which mutation operators could make sense if applied to NAS? 1 Which mutation operators could make sense if applied to NAS? 2 Why is it important to model cost improvement instead of cost directly? 3 How would you decide how many of the poorly-performing models (or which) you can drop?
- Auto-ML | p1 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=1) — AutoML: Neural Architecture Search (NAS) AutoML: Neural Architecture Search (NAS) Overview Bernd Bischl Frank Hutter Lars Kottho↵ Marius Lindauer Joaquin Vanschoren
- Auto-ML | p2-p4 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=2) — Neural Architecture Search (NAS)
- Auto-ML | p5-p7 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=5) — Motivation for NAS
- Auto-ML | p8 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=8) — NAS components NAS components [Elsken et al. 2019]

## Provenance
- Auto-ML | p81 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=81) — 1 Which mutation operators could make sense if applied to NAS? 1 Which mutation operators could make sense if applied to NAS? 2 Why is it important to model cost improvement instead of cost directly? 3 How would you decide how many of the poorly-performing models (or which) you can drop?
- Auto-ML | p1 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=1) — AutoML: Neural Architecture Search (NAS) AutoML: Neural Architecture Search (NAS) Overview Bernd Bischl Frank Hutter Lars Kottho↵ Marius Lindauer Joaquin Vanschoren
- Auto-ML | p2-p4 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=2) — Neural Architecture Search (NAS)
- Auto-ML | p5-p7 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=5) — Motivation for NAS
- Auto-ML | p8 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=8) — NAS components NAS components [Elsken et al. 2019]
- Auto-ML | p9 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=9) — Is there a problem for which you would like to apply NAS yourself? List three major components of NAS methods. Repetition: List three major components of NAS methods. Discussion: Is there a problem for which you would like to apply NAS yourself?
- Auto-ML | p10 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=10) — AutoML: Neural Architecture Search (NAS) AutoML: Neural Architecture Search (NAS) Search Spaces Bernd Bischl Frank Hutter Lars Kottho↵ Marius Lindauer Joaquin Vanschoren
- Auto-ML | p11 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=11) — Basic Neural Architecture Search Spaces
- Auto-ML | p26 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=26) — AutoML: Neural Architecture Search (NAS) AutoML: Neural Architecture Search (NAS) Blackbox Optimization Methods Bernd Bischl Frank Hutter Lars Kottho↵ Marius Lindauer Joaquin Vanschoren
- Auto-ML | p27 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=27) — NAS as Hyperparameter Optimization NAS can be formulated as a HPO problem
- Auto-ML | p28 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=28) — NAS as Hyperparameter Optimization NAS can be formulated as a HPO problem NAS can be formulated as a HPO problem E.g., cell search space by [Zoph et al. 2018] has 5 categorical choices per block 2 categorical choices of hidden states I F For block N, the domain of these categorical variables is h ,h ,output of block 1,...,output of block N 1 i i 1 { } 2 categorical variables choosing between operations I 1 categorical variable choosing the combination method I Total number of hyperparameters for the cell: I 5B (with B=5 by default)
- Auto-ML | p29 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=29) — NAS as Hyperparameter Optimization NAS can be formulated as a HPO problem NAS can be formulated as a HPO problem E.g., cell search space by [Zoph et al. 2018] has 5 categorical choices per block 2 categorical choices of hidden states I F For block N, the domain of these categorical variables is h ,h ,output of block 1,...,output of block N 1 i i 1 { } 2 categorical variables choosing between operations I 1 categorical variable choosing the combination method I Total number of hyperparameters for the cell: I 5B (with B=5 by default) In general: one may require conditional hyperparameters E.g., chain-structured search space I F Top-level hyperparameter: number of layers L F Hyperparameters of layer k conditional on L k
- Auto-ML | p40 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=40) — Brought NAS into the limelight For a fixed number of layers, select: - Filter width/height, stride width/height, number of filters Large computational demands (800 GPUs for 2 weeks, 12.800 architectures evaluated) State-of-the-art results for CIFAR-10 & Penn Treebank architecture Brought NAS into the limelight !
- Auto-ML | p47 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=47) — Kernels for GP-based NAS Encode the architecture space by categorical hyperparameters (like regularized evolution) Strong performance with tree-based models I TPE [Bergstra et al. 2013] I SMAC [Domhan et al. 2015; Mendoza et al. 2016; Zela et al. 2018] Kernels for GP-based NAS - Arc kernel [Swersky et al. 2013] - NASBOT [Kandasamy et al. 2018]
- Auto-ML | p48 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=48) — Kernels for GP-based NAS Encode the architecture space by categorical hyperparameters (like regularized evolution) Strong performance with tree-based models I TPE [Bergstra et al. 2013] I SMAC [Domhan et al. 2015; Mendoza et al. 2016; Zela et al. 2018] Kernels for GP-based NAS - Arc kernel [Swersky et al. 2013] - NASBOT [Kandasamy et al. 2018] There are also several recent promising BO approaches based on neural networks - BANANAS [White et al. 2019]
- Auto-ML | p49 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=49) — Kernels for GP-based NAS Encode the architecture space by categorical hyperparameters (like regularized evolution) Strong performance with tree-based models I TPE [Bergstra et al. 2013] I SMAC [Domhan et al. 2015; Mendoza et al. 2016; Zela et al. 2018] Kernels for GP-based NAS - Arc kernel [Swersky et al. 2013] - NASBOT [Kandasamy et al. 2018] There are also several recent promising BO approaches based on neural networks - BANANAS [White et al. 2019] BO is very competitive, has been shown to outperform RL [Ying et al. 2019]
- Auto-ML | p50 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=50) — Comprehensive experiments on a wide range of 12 di↵erent NAS benchmarks Comprehensive experiments on a wide range of 12 di↵erent NAS benchmarks [Awad et al. 2020]
- Auto-ML | p51 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=51) — Comprehensive experiments on a wide range of 12 di↵erent NAS benchmarks Comprehensive experiments on a wide range of 12 di↵erent NAS benchmarks [Awad et al. 2020] Results: Regularized evolution is very robust, typically amongst best of the methods discussed so far I Evolution variant of di↵erential evolution is yet better; most e cient and robust method I
- Auto-ML | p52 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=52) — Given enough resources, will blackbox NAS approaches always improve performance? What are some pros and cons of using black-box optimizers for NAS? How can NAS be modelled as a HPO problem?
- Auto-ML | p53 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=53) — AutoML: Neural Architecture Search (NAS) AutoML: Neural Architecture Search (NAS) Speedup Techniques Bernd Bischl Frank Hutter Lars Kottho↵ Marius Lindauer Joaquin Vanschoren
- Auto-ML | p54 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=54) — Overview of NAS Speedup Methods
- Auto-ML | p55-p57 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=55) — NAS Speedup Technique 1: Multi-fidelity optimization
- Auto-ML | p58-p59 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=58) — NAS Speedup Technique 2: Learning Curve Prediction
- Auto-ML | p60 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=60) — Only little work on meta-learning for NAS NAS Speedup Technique 3: Meta-Learning Lots of work on meta-learning for HPO Only little work on meta-learning for NAS - Find a set of good architectures to initialize BOHB in Auto-Pytorch [Zimmer et al. 2020] - Learn RL agent’s policy network on previous datasets [Wong et al. 2018] - Learn neural architecture that can be quickly adapted [Lian et al. 2019; Elsken et al. 2019]
- Auto-ML | p61 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=61) — NAS Speedup Technique 4: Network Morphisms
- Auto-ML | p66-p68 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=66) — Network Morphisms for Multi-objective NAS Network Morphisms for Multi-objective NAS [Elsken et al. 2019]
- Auto-ML | p69-p72 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=69) — NAS Speedup Technique 5: Weight Sharing and One-shot Models NAS Speedup Technique 5: Weight Sharing and One-shot Models [Pham et al. 2018; Bender et al. 2018]
- Auto-ML | p73 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=73) — Which speedup techniques directly carry over from HPO to NAS? List five methods to speed up NAS over blackbox approaches Why do network morphisms and the one-shot model only apply to NAS, and not to HPO?
- Auto-ML | p74 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=74) — AutoML: Neural Architecture Search (NAS) AutoML: Neural Architecture Search (NAS) Issues and Best Practices in NAS Research Bernd Bischl Frank Hutter Lars Kottho↵ Marius Lindauer Joaquin Vanschoren Issues and Best Practices in NAS Research
- Auto-ML | p75-p77 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=75) — For benchmarks used in almost all NAS papers: Issues in NAS Research & Evaluations Most NAS methods are extremely di cult to
- Auto-ML | p78 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=78) — Best Practice Checklist for Scientific Research in NAS Unifying open-source implementation of modern NAS algorithms First NAS workshop at ICLR 2020
- Auto-ML | p79 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=79) — Unifying open-source implementation of modern NAS algorithms First NAS workshop at ICLR 2020 Building a Scientific Community for NAS
- Auto-ML | p80 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=80) — First NAS workshop at ICLR 2020 Building a Scientific Community for NAS - NAS-Bench-101 [Ying et al. 2019]
- Auto-ML | p81 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=81) — Building a Scientific Community for NAS - NAS-Bench-101 [Ying et al. 2019] - NAS-Bench-201 [Dong and Yang. 2020]
- Auto-ML | p82 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=82) — Code for your NAS method Hyperparameters for your NAS method, as well as random seeds Note that the easiest way to satisfy the first three is to use existing NAS benchmarks
- Auto-ML | p83 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=83) — Note that the easiest way to satisfy the first three is to use existing NAS benchmarks Definition: NAS Benchmark [Lindauer and Hutter. 2020] A NAS benchmark consists of a dataset (with a predifiend training-test
- Auto-ML | p84 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=84) — Best Practice Checklist for NAS Research Code for your NAS method Hyperparameters for your NAS method, as well as random seeds
- Auto-ML | p85-p92 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=85) — Best Practice Checklist for NAS Research Best practices for comparing NAS methods For all NAS methods you compare, did you use exactly the same NAS benchmark, including
- Auto-ML | p93 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=93) — Did you report the time for the entire end-to-end NAS method (rather than, e.g., only for Clean NAS benchmarks for new applications Open-source library of NAS methods to compare methods without confounding factors
- Auto-ML | p94-p96 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=94) — Clean NAS benchmarks for new applications Open-source library of NAS methods to compare methods without confounding factors Best Practice Checklist for NAS Research
- Auto-ML | p97 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=97) — Best Practice Checklist for NAS Research Did you report the time for the entire end-to-end NAS method (rather than, e.g., only for Clean NAS benchmarks for new applications
- Auto-ML | p98 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=98) — NAS-Bench-101: The First NAS Benchmark NAS-Bench-101: The First NAS Benchmark [Ying et al. 2019]
- Auto-ML | p99 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=99) — NAS-Bench-101: The First NAS Benchmark To limit the number of architectures, NAS-Bench-101 has the following constraints: NAS-Bench-101: The First NAS Benchmark [Ying et al. 2019]
- Auto-ML | p100-p101 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=100) — NAS-Bench-101: The First Tabular NAS Benchmark Based on this table, anyone can now run NAS experiments in seconds without a GPU. NAS-Bench-101: The First Tabular NAS Benchmark [Ying et al. 2019]
- Auto-ML | p102 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=102) — NAS-Bench-101: The First Tabular NAS Benchmark Based on this table, anyone can now run NAS experiments in seconds without a GPU. trial number, one can query from NAS-Bench-101
- Auto-ML | p103 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=103) — NAS [Zoph and Le. 2017] by 6 years - Only now, benchmarks like NAS-Bench-101 allow for e cient comparisons Evaluation of Blackbox NAS Methods on NAS-Bench-101
- Auto-ML | p104 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=104) — Evaluation of Blackbox NAS Methods on NAS-Bench-101 NAS [Zoph and Le. 2017] by 6 years - Only now, benchmarks like NAS-Bench-101 allow for e cient comparisons
- Auto-ML | p105 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=105) — For the most common NAS search space, how important is the NAS component Why do we need proper benchmarking of NAS algorithms? What does a NAS benchmark consist of?
- Auto-ML | p106 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=106) — AutoML: Neural Architecture Search (NAS)
- Auto-ML | p107-p112, p115-p117, p119, p125 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=107) — AutoML:NAS
- Auto-ML | p113 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=113) — What migth be some downsides of using the one-shot model for NAS? AutoML:NAS Repetition: How are the weights shared in the one-shot model? Repetition: What is the di↵erence between Random Search with Weight Sharing and ENAS? Discussion: What migth be some downsides of using the one-shot model for NAS?
- Auto-ML | p120 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=120) — What is the main di↵erence between DARTS and the other one-shot NAS methods we AutoML:NAS Repetition: What is the main di↵erence between DARTS and the other one-shot NAS methods we saw before? Repetition: How does DARTS optimize the architectural weights and one-shot weights? Repetition: What are DARTS’ main issues and how can they be fixed? Discussion: RobustDARTS stops the architecture optimization early, before the curvature of the validation loss becomes high. Why do you think this works? [Hint: think about the discretization step after the DARTS search.]
- Auto-ML | p121 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=121) — AutoML: Neural Architecture Search (NAS) NASLib: A Modular and Extensible NAS Library
- Auto-ML | p122 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=122) — NASLib is a framework for easily implementing di↵erent NAS methods, aiming to: Modularize di↵erent components of NAS optimizers to allow combining them O↵er researchers a convenient way of prototyping new NAS methods
- Auto-ML | p123 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=123) — NASLib implements a broad range of NAS optimizers Blackbox NAS methods, e.g., Regularized Evolution One-shot NAS methods, e.g., DARTS
- Auto-ML | p124 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=124) — - a MixedOp – for one-shot NAS optimizers, e.g. DARTS AutoML:NAS The optimizers are agnostic to the search space they are running on This facilitates their use for new types of search spaces I An optimizer takes the search space as a NetworkX object and builds the PyTorch computational graph ) Depending on the optimizer, each operation choice in the NetworkX object becomes: - a MixedOp – for one-shot NAS optimizers, e.g. DARTS - a CategoricalOp – for black-box optimizers, e.g. Regularized Evolution
- Auto-ML | p126 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=126) — Tabular benchmarks for one-shot NAS NAS-Bench-101 [Ying et al. 2019] is not directly compatible with one-shot NAS methods NAS-Bench-1Shot1 [Zela et al. 2020]
- Auto-ML | p127 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=127) — NASLib case study: Results on NAS-Bench-201 NAS-Bench-201 is already AutoML:NAS
- Auto-ML | p128 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=128) — NASLib is the first library that separates the NAS method from the search spaces Applications of NAS to your problem of interest, with interesting search spaces F Therefore, no changes are required in the NAS methods
- Auto-ML | p129 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=129) — NAS methods, which of the methods we discussed might make sense to combine? AutoML:NAS Repetition: What would one have to do in order to apply the methods in NASLib to a new search space? Discussion: Is there a problem of your interest that you would you like to apply the methods in NASLib to? Discussion: Given that NASLib’s modular design allows mixing and matching components of one-shot NAS methods, which of the methods we discussed might make sense to combine?
- Auto-ML | p130 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=130) — AutoML: Neural Architecture Search (NAS) Practical Recommendations for NAS and HPO
- Auto-ML | p131 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=131) — Neural architecture search is still a very young field Hyperparameter optimization is a mature field - Blackbox HPO has been researched for decades; there are many software packages - Multi-fidelity HPO has also become quite mature Neural architecture search is still a very young field - Blackbox is quite mature, but slow - Multi-fidelity NAS is also quite mature and faster - Meta-learning + multi-fidelity NAS is fast, but is still a very young field - Gradient-based NAS is fast, but can have failure modes with terrible performance - Gradient-based NAS hasn’t reached the hands-o↵ AutoML stage yet NAS is mainly used to create new architectures that many others can reuse Given a new dataset, HPO is crucial for good performance; NAS may not be necessary - The biggest gains typically come from tuning key hyperparameters (learning rate, etc) - Reusing a previous achitecture often yields competitive results Maturity of the Fields of NAS and HPO
- Auto-ML | p132 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=132) — Practical Recommendations for NAS and HPO Try NAS if you can How to combine NAS & HPO
- Auto-ML | p133 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=133) — Case Study: NAS & HPO in Auto-PyTorch Tabular models AutoML:NAS Case Study: NAS & HPO in Auto-PyTorch Tabular [Zimmer,Lindauer&Hutter,2020]
- Auto-ML | p134 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=134) — Case Study: NAS & HPO in Auto-DispNet Both NAS and HPO improved the state of the art AutoML:NAS
- Auto-ML | p135 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=135) — If you want to use both HPO and NAS for your problem, how could you proceed? you use to combine HPO and NAS, and why? AutoML:NAS
- Auto-ML | p136 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=136) — Survey on NAS: [Elsken and Metzen and Hutter, 2019] AutoML:NAS
- Auto-ML | p27 | [w01_t01_04_big_picture.pdf](../data/raw/Auto-ML/w01_t01_04_big_picture.pdf#page=27) — The neural architecture search (NAS) problem is to find an architecture that minimizes this Neural Architecture Search (NAS) Definition Let λλλ be an architecture for a deep neural network N with domain ΛΛΛ, be a dataset which is split into and opt train valid D D D c(N , , ) denote the cost of N trained on and evaluated on . λλλ train valid λλλ train valid D D D D The neural architecture search (NAS) problem is to find an architecture that minimizes this cost: λλλ argminc(N , , ) ∗ λλλ train valid ∈ D D λλλ ΛΛΛ ∈ Remark: very similar to the HPO definition In practice, you want jointly optimize HPO and NAS [Zela et al. 2018]
- Auto-ML | p28 | [w01_t01_04_big_picture.pdf](../data/raw/Auto-ML/w01_t01_04_big_picture.pdf#page=28) — For solving the HPO, CASH and NAS problem, we use some kind of optimization For solving the HPO, CASH and NAS problem, we use some kind of optimization approach to search for a solution A different view: Can we learn from data and thus predict an algorithm/ hyperparameter configuration/ neural architecture? Definition Let p( ) be a probability distribution over datasets D, D D ∈ P a portfolio of algorithms P, and A ∈ c : P D R be a cost metric × → the per-instance algorithm selection problem is to obtain a mapping s : such that D 7→ A argmin c(s( ), )p( )d D D D D s ZD
- Auto-ML | p30 | [w01_t01_04_big_picture.pdf](../data/raw/Auto-ML/w01_t01_04_big_picture.pdf#page=30) — NAS Search for the architecture of neural network HPO Search for the best hyperparameter configuration of a ML algorithm CASH Search for the best combination of algorithm and hyperparameter configuration NAS Search for the architecture of neural network Selection Predict the best algorithm (and its hyperparameter configuration) DAC Predict the best hyperparameter configuration for an algorithm state at a given time point

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.953
- evidence strength: 0.98
- definition quality: 0.9
- interview relevance: 0.98
- version: 7
- last updated: 2026-08-05T15:34:07.945816+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- assumptions not extracted
