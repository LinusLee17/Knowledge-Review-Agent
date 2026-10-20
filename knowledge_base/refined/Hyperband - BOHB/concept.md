---
concept_name: "Hyperband / BOHB"
canonical_key: "hyperband bohb"
concept_type: "algorithm"
domain: "Machine Learning"
topic: "AutoML"
importance_score: 4
scope_level: 3
study_priority: 4
version_number: 4
last_updated_timestamp: "2026-08-05T15:34:07.902137+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Hyperband / BOHB

## Classification
- domain: Machine Learning
- topic: AutoML
- type: algorithm
- scope: 3/5 (core concept or method)
- study priority: 4/5
- also known as: BOHB, BOHB hyperband, bandit based hyperparameter optimization, hyperband
- broader topic(s): Resource Allocation

## Contributing Courses
- Auto-ML

## Definition
Hyperband is a resource-allocation and successive-halving strategy for rapidly discarding weak configurations. BOHB combines this multi-fidelity racing idea with a model-based sampler so promising regions of the hyperparameter space receive more trials.

## Why it Matters
Hyperband and BOHB connect search quality to resource allocation. They address the central AutoML problem that evaluating every configuration to completion is too costly.

## Core Intuition
Run many cheap candidates, repeatedly halve the pool, and give more resources to survivors; BOHB biases new candidates toward regions that already look good.

## How it Works
1. Create brackets with different numbers of configurations and initial resource levels.
2. Run each configuration briefly, rank results, and retain only the strongest fraction.
3. Increase resources for survivors through successive-halving rounds.
4. In BOHB, sample new configurations from a model of good observations while Hyperband controls resource allocation.

## Mathematical Foundation
$$
n_{j+1} = \left\lfloor n_j / \eta \right\rfloor, \qquad r_{j+1} = \eta r_j
$$

Successive halving keeps roughly the best `1/\eta` fraction while increasing their resource. BOHB supplies model-based candidates to the brackets.

## Key Components
- Brackets
- Initial configurations
- Resource levels
- Successive halving
- Reduction factor
- Model-based sampler in BOHB

## Advantages
- Allocates more budget to promising trials and stops weak trials early.
- Works well when low-resource performance is informative about final performance.

## Limitations
- Successive halving can discard late-blooming configurations when early performance is misleading.
- The reduction factor and resource brackets affect the allocation strategy.

## Common Mistakes
- Stopping promising late-learning configurations because early scores look weak.
- Confusing a Hyperband bracket and its successive-halving schedule with a single search trial.
- Calling BOHB ordinary Bayesian optimization without accounting for its multi-fidelity budget allocation.

## Real-world Applications
- Budgeted Hyperparameter Search
- Early Stopping

## Interview Questions
- How does successive halving decide which configurations continue?
- What does Hyperband add beyond one successive-halving schedule?
- How does BOHB use model-based sampling within Hyperband?
- What failure mode appears when early scores poorly predict final scores?

## Related Concepts
- HPO Speedup Techniques
- Hyperparameter Optimization

## Connections
- Depends on: Multi-fidelity Optimization and Bayesian Optimization
- Used in: Early Stopping and Budgeted Hyperparameter Search
- Related: Hyperparameter Optimization and HPO Speedup Techniques
- Broader topic: AutoML and Resource Allocation

## Prerequisites
- Bayesian Optimization
- Multi-fidelity Optimization

## Slide-derived Evidence
- Auto-ML | p7 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=7) — Explain the Successive Halving and Hyperband algorithms Explain how to combine Bayesian optimization and Hyperband in BOHB Describe many different ways of using meta-learning to speed up HPO Explain the concept of multi-fidelity optimization to speed up HPO Explain the Successive Halving and Hyperband algorithms Explain how to combine Bayesian optimization and Hyperband in BOHB Describe how to exploit multiple fidelities in Bayesian optimization Discuss several ways of predicting learning curves Discuss success stories of speeding up Bayesian optimization
- Auto-ML | p35 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=35) — An Extension of SH with Theoretical Guarantees: Hyperband
- Auto-ML | p37 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=37) — Discussion. How do you think Hyperband would compare to successive halving using the Discussion. How slow is Hyperband in the worst case? Discussion. How do you think Hyperband would compare to successive halving using the most aggressive fidelity? Discussion. How slow is Hyperband in the worst case?
- Auto-ML | p39 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=39) — Optimization with Hyperband Desiderata for a practical solution to the hyperparamenter optimization problem: Strong Anytime Performance Strong Final Performance Scalability Robustness & Flexibility Computational Efficiency Effective Use of Parallel Resources Conceptual / Algorithmic Simplicity To fulfill all of these desiderata, BOHB [Falkner, Klein and Hutter, ICML 2018] combines Bayesian Optimization with Hyperband To fulfill all of these desiderata, BOHB [Falkner, Klein and Hutter, ICML 2018] combines Bayesian
- Auto-ML | p40 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=40) — BOHB combines the advantages of Bayesian Optimization and Hyperband (cid:73) Hyperband to choose the budgets for good anytime performance BOHB combines the advantages of Bayesian Optimization and Hyperband (cid:73) Bayesian Optimization for choosing configurations to achieve strong final performance (cid:73) Hyperband to choose the budgets for good anytime performance BOHB replaces the random selection of configurations at the beginning of each HB iteration by a model-based search Details of the model (cid:73) Variant of the Tree Parzen Estimator, with a product kernel (cid:73) Models are fitted independently to the data for one budget at a time (cid:70) Specifically, always the highest budget that has enough data points

## Provenance
- Auto-ML | p7 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=7) — Explain the Successive Halving and Hyperband algorithms Explain how to combine Bayesian optimization and Hyperband in BOHB Describe many different ways of using meta-learning to speed up HPO Explain the concept of multi-fidelity optimization to speed up HPO Explain the Successive Halving and Hyperband algorithms Explain how to combine Bayesian optimization and Hyperband in BOHB Describe how to exploit multiple fidelities in Bayesian optimization Discuss several ways of predicting learning curves Discuss success stories of speeding up Bayesian optimization
- Auto-ML | p35 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=35) — An Extension of SH with Theoretical Guarantees: Hyperband
- Auto-ML | p37 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=37) — Discussion. How do you think Hyperband would compare to successive halving using the Discussion. How slow is Hyperband in the worst case? Discussion. How do you think Hyperband would compare to successive halving using the most aggressive fidelity? Discussion. How slow is Hyperband in the worst case?
- Auto-ML | p39 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=39) — Optimization with Hyperband Desiderata for a practical solution to the hyperparamenter optimization problem: Strong Anytime Performance Strong Final Performance Scalability Robustness & Flexibility Computational Efficiency Effective Use of Parallel Resources Conceptual / Algorithmic Simplicity To fulfill all of these desiderata, BOHB [Falkner, Klein and Hutter, ICML 2018] combines Bayesian Optimization with Hyperband To fulfill all of these desiderata, BOHB [Falkner, Klein and Hutter, ICML 2018] combines Bayesian
- Auto-ML | p40 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=40) — BOHB combines the advantages of Bayesian Optimization and Hyperband (cid:73) Hyperband to choose the budgets for good anytime performance BOHB combines the advantages of Bayesian Optimization and Hyperband (cid:73) Bayesian Optimization for choosing configurations to achieve strong final performance (cid:73) Hyperband to choose the budgets for good anytime performance BOHB replaces the random selection of configurations at the beginning of each HB iteration by a model-based search Details of the model (cid:73) Variant of the Tree Parzen Estimator, with a product kernel (cid:73) Models are fitted independently to the data for one budget at a time (cid:70) Specifically, always the highest budget that has enough data points
- Auto-ML | p41 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=41) — BOHB: Algorithm Pseudocode for sampling in BOHB Pseudocode for sampling in BOHB Input : observations D, fraction of random runs ρ, percentile γ, num- ber of samples N , minimum number of points N to build s min a model, and bandwidth factor b w Output: next configuration to evaluate 1 if rand() < ρ then return random configuration 2 b = argmax D b : D b N min +2 { | | ≥ } 3 if b = ∅ then return random configuration 4 Fit KDEs according to Equation 1 5 Draw N s samples acoording to l(cid:48)(λλλ) 6 return sample with highest ratio l(λλλ)/g(λλλ) l(λλλ) = p(c(λλλ) γ D ) g(λλλ) = p(c(λλλ) > γ D ) (1) b b ≤ | | Note: l (cid:48) (λλλ) is similar to l(λλλ,) but has larger bandwidths
- Auto-ML | p46 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=46) — Figure: Performance of BOHB with different number of parallel workers on the letter surrogate BOHB: Different number of parallel workers Figure: Performance of BOHB with different number of parallel workers on the letter surrogate benchmark for 128 iterations
- Auto-ML | p78 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=78) — Followed by BOHB-like approach (uses successive halving instead of Hyperband) Idea: integrate warmstarting and a BOHB-like approach for Auto-sklearn Uses task-independent meta-learning to warmstart Bayesian optimization (cid:73) Therefore, no need for (potentially unreliable) meta-features Uses successive halving to quickly go through proposed configurations (cid:73) Therefore, scales better to larger datasets Followed by BOHB-like approach (uses successive halving instead of Hyperband) Won the 2nd AutoML challenge Idea: integrate warmstarting and a BOHB-like approach for Auto-sklearn
- Auto-ML | p82 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=82) — Just submitted: DEHB combines differential evolution and Hyperband and largely If multiple fidelities available: BOHB [Falkner, Klein and Hutter, ICML 2018] Otherwise (cid:73) Low-dimensional continuous parameter space: (cid:70) GP-based BO, e.g., Spearmint [Snoek et al. 2012] (cid:73) High-dimensional discrete parameter space: (cid:70) RF-based BO, e.g., SMAC [Hutter et al. 2011] (cid:73) Purely continuous, cheap function evaluations: (cid:70) CMA-ES [Hansen et al., since 2001]; evaluated for HPO by [Loshchilov & Hutter, ICLR WS 2016] Just submitted: DEHB combines differential evolution and Hyperband and largely dominates BOHB. Especially good for high dimensions. If multiple fidelities available: BOHB [Falkner, Klein and Hutter, ICML 2018]

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.613
- evidence strength: 0.74
- definition quality: 0.24
- interview relevance: 0.92
- version: 4
- last updated: 2026-08-05T15:34:07.902137+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- assumptions not extracted
