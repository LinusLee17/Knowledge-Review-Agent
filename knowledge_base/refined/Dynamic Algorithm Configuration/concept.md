---
concept_name: "Dynamic Algorithm Configuration"
canonical_key: "dynamic algorithm configuration"
concept_type: "method"
domain: "Machine Learning"
topic: "AutoML"
importance_score: 5
scope_level: 3
study_priority: 5
version_number: 13
last_updated_timestamp: "2026-08-05T17:21:13.177260+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Dynamic Algorithm Configuration

## Classification
- domain: Machine Learning
- topic: AutoML
- type: method
- scope: 3/5 (core concept or method)
- study priority: 5/5
- also known as: DAC, algorithm configuration, dynamic configuration
- broader topic(s): Algorithm Configuration, Sequential Decision Making

## Contributing Courses
- Auto-ML

## Definition
Dynamic Algorithm Configuration (DAC) changes algorithm parameters or components during execution using a learned policy. It replaces fixed heuristics with state-dependent decisions that can adapt as the search or optimization process evolves.

## Why it Matters
DAC matters when the best action changes during execution. It lets AutoML adapt an algorithm rather than choosing one static configuration before the run starts.

## Core Intuition
The best setting can change during a run, so a policy observes algorithm state and chooses the next configuration or component.

## How it Works
1. Define the algorithm state observed during execution and the configurable actions.
2. Collect trajectories or optimize a policy against a runtime cost or performance reward.
3. Let the policy choose parameter values or components as state changes.
4. Compare the adaptive run with a fixed-configuration baseline on the same task and budget.

## Key Components
- Algorithm state
- Configurable actions
- Policy
- Reward/cost
- Execution trajectory
- Adaptation rule

## Advantages
- Adapts decisions to the current state of a running algorithm.
- Can replace brittle hand-designed parameter schedules with learned policies.

## Limitations
- Learning a policy requires state definitions, trajectories, and a reliable reward or cost signal.
- A policy that works for one workload may not generalize to another.

## Common Mistakes
- Defining actions that cannot be applied at the decision points available during a run.
- Optimizing a policy for one workload and assuming it transfers to another.
- Comparing dynamic control with static defaults without fixing seeds, budgets, and workloads.

## Real-world Applications
- Adaptive Algorithms
- Automated Machine Learning
- Online Configuration

## Interview Questions
- How does dynamic configuration differ from choosing parameters once before a run?
- What are the state, action, and reward in a DAC formulation?
- Why can a policy overfit a workload distribution?
- How would you evaluate a DAC policy against a strong static baseline?

## Related Concepts
- Hyperparameter Optimization
- Meta-learning for AutoML

## Connections
- Depends on: Algorithm Selection and Hyperparameter Optimization
- Used in: Online Configuration, Adaptive Algorithms, and Automated Machine Learning
- Related: Meta-learning for AutoML and Hyperparameter Optimization
- Broader topic: AutoML, Algorithm Configuration, and Sequential Decision Making

## Prerequisites
- Algorithm Selection
- Hyperparameter Optimization

## Slide-derived Evidence
- Auto-ML | p1 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=1) — AutoML: Dynamic Algorithm Configuration AutoML: Dynamic Algorithm Configuration Overview Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p15 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=15) — Dynamic Algorithm Configuration: DAC The goal of DAC is to learn a policy from data
- Auto-ML | p16 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=16) — Dynamic Algorithm Configuration: DAC Dynamic Adaptation of Hyperparameters The goal is to dynamically adapt hyperparameters based on some feedback from the algorithm. Dynamic Algorithm Configuration: DAC The goal of DAC is to learn a policy from data that adapts the hyperparameter settings of an IOH. The goal of DAC is to learn a policy from data
- Auto-ML | p17 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=17) — Dynamic Algorithm Configuration: DAC Dynamic Adaptation of Hyperparameters The goal is to dynamically adapt hyperparameters based on some feedback from the algorithm. Dynamic Algorithm Configuration: DAC The goal of DAC is to learn a policy from data that adapts the hyperparameter settings of an IOH. Learning to Learn: L2L The goal of L2L is to learn a proposal mechanism from data. (Not covered in this lecture.) The goal of DAC is to learn a policy from data
- Auto-ML | p19 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=19) — AutoML: Dynamic Algorithm Configuration AutoML: Dynamic Algorithm Configuration Problem Setup Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren MariusLindauer AutoML:DAC 1/1

## Provenance
- Auto-ML | p1 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=1) — AutoML: Dynamic Algorithm Configuration AutoML: Dynamic Algorithm Configuration Overview Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p15 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=15) — Dynamic Algorithm Configuration: DAC The goal of DAC is to learn a policy from data
- Auto-ML | p16 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=16) — Dynamic Algorithm Configuration: DAC Dynamic Adaptation of Hyperparameters The goal is to dynamically adapt hyperparameters based on some feedback from the algorithm. Dynamic Algorithm Configuration: DAC The goal of DAC is to learn a policy from data that adapts the hyperparameter settings of an IOH. The goal of DAC is to learn a policy from data
- Auto-ML | p17 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=17) — Dynamic Algorithm Configuration: DAC Dynamic Adaptation of Hyperparameters The goal is to dynamically adapt hyperparameters based on some feedback from the algorithm. Dynamic Algorithm Configuration: DAC The goal of DAC is to learn a policy from data that adapts the hyperparameter settings of an IOH. Learning to Learn: L2L The goal of L2L is to learn a proposal mechanism from data. (Not covered in this lecture.) The goal of DAC is to learn a policy from data
- Auto-ML | p19 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=19) — AutoML: Dynamic Algorithm Configuration AutoML: Dynamic Algorithm Configuration Problem Setup Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren MariusLindauer AutoML:DAC 1/1
- Auto-ML | p20-p23, p36 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=20) — MariusLindauer AutoML:DAC 2/1 AutoML:DAC
- Auto-ML | p24-p27 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=24) — the dynamic algorithm configuration problem is to obtain a policy π∗ : s×D (cid:55)→λλλ by Dynamic Algorithm Configuration MariusLindauer AutoML:DAC 3/1
- Auto-ML | p28 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=28) — Dynamic Algorithm Configuration the dynamic algorithm configuration problem is to obtain a policy π∗ : s×D (cid:55)→λλλ by So far, we assumed that an algorithm runs with static settings However, settings, such as learning rate, have to be adapted over time Definition Let λλλ ∈ΛΛΛ be a hyperparameter configuration of an algorithm A, p(D) be a probability distribution over datasets D ∈ D (or tasks), s(t) be a state description of A solving D at time point t, c : Π×D → R be a cost metric assessing the cost of a control policy π ∈ Π on D ∈ D the dynamic algorithm configuration problem is to obtain a policy π∗ : s×D (cid:55)→λλλ by optimizing its cost across a distribution of datasets: (cid:90) π∗ ∈ argmin p(D)c(π,D)dD π∈Π D
- Auto-ML | p29-p33 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=29) — Dynamic Algorithm Configuration as Contextual MDP Dynamic Algorithm Configuration as Contextual MDP [Biedenkapp et al. 2020] MariusLindauer AutoML:DAC 4/1
- Auto-ML | p34 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=34) — 2 How would you solve the dynamic algorithm configuration problem efficiently? 1 What kind of information can you make use of for state information in deep learning? 2 How would you solve the dynamic algorithm configuration problem efficiently? 3 How can we make use of the cost value in each state (and not only in the final state after training ended)? MariusLindauer AutoML:DAC 5/1
- Auto-ML | p35 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=35) — Approaches for Solving Dynamic Algorithm Configuration AutoML: Dynamic Algorithm Configuration AutoML: Dynamic Algorithm Configuration Approaches for Solving Dynamic Algorithm Configuration Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p37 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=37) — DAC by Configuring Hand-Designed Heuristics MariusLindauer AutoML:DAC 3/1 AutoML:DAC
- Auto-ML | p38 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=38) — DAC by Optimization (Direct Schedule) MariusLindauer AutoML:DAC 4/1 AutoML:DAC
- Auto-ML | p39-p41 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=39) — DAC by Optimization (Functional Schedule) MariusLindauer AutoML:DAC 5/1 AutoML:DAC
- Auto-ML | p42 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=42) — DAC by Reinforcement Learning Difference to DAC by Optimziation with a functional schedule: ▶ DAC by RL can make use of sequential structure of the problem
- Auto-ML | p43 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=43) — DAC by Optimization (Online) MariusLindauer AutoML:DAC 7/1 AutoML:DAC
- Auto-ML | p44 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=44) — DAC can be solved in different ways, incl. MariusLindauer AutoML:DAC 8/1 DAC can be solved in different ways, incl. ▶ Configuration of hand-designed heuristics ▶ Direct configuration of a schedule ▶ Optimization of a functional schedule ▶ Using Reinforcement Learning ▶ On-the-fly online optimization
- Auto-ML | p45 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=45) — 2 What are the advantages and disadvantages of using reinforcement learning for DAC or online DAC? MariusLindauer AutoML:DAC 9/1
- Auto-ML | p46 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=46) — AutoML: Dynamic Algorithm Configuration AutoML: Dynamic Algorithm Configuration Population-based Training Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p47 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=47) — Dynamic algorithm configuration assumes that we have access to Dynamic algorithm configuration assumes that we have access to a representative learning environment in an offline learning phase
- Auto-ML | p48 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=48) — Dynamic algorithm configuration assumes that we have access to Dynamic algorithm configuration assumes that we have access to a representative learning environment in an offline learning phase What if we don’t access to such an env or don’t have to time for offline learning?
- Auto-ML | p49 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=49) — Dynamic algorithm configuration assumes that we have access to Dynamic algorithm configuration assumes that we have access to a representative learning environment in an offline learning phase What if we don’t access to such an env or don’t have to time for offline learning? ⇝ Try to figure out best hyperparameter settings on the fly
- Auto-ML | p64 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=64) — PBT relates to dynamic algorithm configuration PBT returns an already trained model (e.g., DNN or RL policy) ▶ No explicit policy is returned ⇝ Drawback: cannot be transferred to other datasets/tasks PBT uses evolutionary computing to determine well-performing hyperparameter settings Since hyperparameter settings changes while training the models, PBT relates to dynamic algorithm configuration
- Auto-ML | p65 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=65) — PBT relates to dynamic algorithm configuration PBT returns an already trained model (e.g., DNN or RL policy) ▶ No explicit policy is returned ⇝ Drawback: cannot be transferred to other datasets/tasks PBT uses evolutionary computing to determine well-performing hyperparameter settings Since hyperparameter settings changes while training the models, PBT relates to dynamic algorithm configuration Since each population member (i.e., model) can be trained independently, PBT can be efficiently parallelized ⇝ Drawback: requires substantial parallel compute resources
- Auto-ML | p82 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=82) — AutoML: Dynamic Algorithm Configuration AutoML: Dynamic Algorithm Configuration Background: Reinforcement Learning Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren
- Auto-ML | p101 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=101) — AutoML: Dynamic Algorithm Configuration AutoML: Dynamic Algorithm Configuration Reinforcement Learning for DAC Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren Reinforcement Learning for DAC
- Auto-ML | p102, p112 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=102) — RL for DAC
- Auto-ML | p111 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=111) — AutoML: Dynamic Algorithm Configuration AutoML: Dynamic Algorithm Configuration Generalizing DAC Bernd Bischl Frank Hutter Lars Kotthoff Marius Lindauer Joaquin Vanschoren Generalizing DAC
- Auto-ML | p121 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=121) — So far, DAC is often used to replace existing manually designed heuristics, So far, DAC is often used to replace existing manually designed heuristics, e.g., learning rate schedules In some cases, these manually designed heuristics perform very well ⇝ Can we learn from these existing heuristics as an initial policy?
- Auto-ML | p122 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=122) — So far, DAC is often used to replace existing manually designed heuristics, So far, DAC is often used to replace existing manually designed heuristics, e.g., learning rate schedules In some cases, these manually designed heuristics perform very well ⇝ Can we learn from these existing heuristics as an initial policy? There are special RL algorithm that allow imitating existing episodes (here generated from these manual heuristics) [Shala et al. 2020] proposed to combine replies of existing heuristics and learned heuristics ▶ Guided Policy Search [Levine and Koltun 2013] allows to define a teacher which is imitated ▶ Teacher is our existing manually designed heuristic ▶ By replying the existing heuristics sufficiently often, a policy similar to the existing one can be learned, but is better on average
- Auto-ML | p123 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=123) — For dynamic algorithm configuration, the goal is to learn on a set of meta-train datasets
- Auto-ML | p124 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=124) — For dynamic algorithm configuration, the goal is to learn on a set of meta-train datasets Meta-RL deals with the problem on how to transfer knowledge between learning tasks ▶ E.g., how to initialize the policy weights effectively s.t. learning will be efficient on new tasks For dynamic algorithm configuration, the goal is to learn on a set of meta-train datasets and then apply the learned policy on a new (meta-test) datasets ⇝ no fine-tuning on the new data set ⇝ zero-short transfer
- Auto-ML | p125 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=125) — For dynamic algorithm configuration, the goal is to learn on a set of meta-train datasets Meta-RL deals with the problem on how to transfer knowledge between learning tasks ▶ E.g., how to initialize the policy weights effectively s.t. learning will be efficient on new tasks For dynamic algorithm configuration, the goal is to learn on a set of meta-train datasets and then apply the learned policy on a new (meta-test) datasets ⇝ no fine-tuning on the new data set ⇝ zero-short transfer Also related to offline Reinforcement Learning ▶ Only logged data from previous tasks is available ▶ Learn a new policy on a new task without interacting with environment again ▶ Special case of meta-RL Source: [Kumar and Singh 2020]
- Auto-ML | p29 | [w01_t01_04_big_picture.pdf](../data/raw/Auto-ML/w01_t01_04_big_picture.pdf#page=29) — the dynamic algorithm configuration problem (DAC) is to obtain a configuration policy Dynamic Algorithm Configuration So far, we assume that an algorithm runs with some given settings However, some settings, such as learning rate, have to be adapted over time Definition Let λλλ be a hyperparameter configuration of an algorithm , A p( ) be a probability distribution over datasets D, D D ∈ s be a state description of solving at time point t, t A D c : Π D R be a cost metric assessing the cost of a conf. policy π Π on D × → ∈ D ∈ the dynamic algorithm configuration problem (DAC) is to obtain a configuration policy π : s λλλ by optimizing its cost across a distribution of datasets: ∗ t ×D 7→ π argmin p( )c(π, )d ∗ ∈ D D D π Π ZD ∈
- Auto-ML | p30 | [w01_t01_04_big_picture.pdf](../data/raw/Auto-ML/w01_t01_04_big_picture.pdf#page=30) — DAC Predict the best hyperparameter configuration for an algorithm state HPO Search for the best hyperparameter configuration of a ML algorithm CASH Search for the best combination of algorithm and hyperparameter configuration NAS Search for the architecture of neural network Selection Predict the best algorithm (and its hyperparameter configuration) DAC Predict the best hyperparameter configuration for an algorithm state at a given time point

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.857
- evidence strength: 0.82
- definition quality: 0.84
- interview relevance: 0.98
- version: 13
- last updated: 2026-08-05T17:21:13.177260+00:00

## Assumptions
- Dynamic algorithm configuration assumes that we have access to
