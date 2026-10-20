---
concept_name: "Multi-fidelity Optimization"
canonical_key: "multi fidelity optimization"
concept_type: "method"
domain: "Machine Learning"
topic: "AutoML"
importance_score: 5
scope_level: 3
study_priority: 5
version_number: 12
last_updated_timestamp: "2026-08-05T17:21:13.265392+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Multi-fidelity Optimization

## Classification
- domain: Machine Learning
- topic: AutoML
- type: method
- scope: 3/5 (core concept or method)
- study priority: 5/5
- also known as: multi-fidelity methods, multi-fidelity optimisation
- broader topic(s): Optimization, Resource Allocation

## Contributing Courses
- Auto-ML

## Definition
Multi-fidelity Optimization uses cheap, lower-fidelity evaluations, such as fewer epochs or fewer data points, to allocate computation toward promising configurations before spending the full budget.

## Why it Matters
Multi-fidelity methods make AutoML practical under limited compute by using partial training signals to reserve full budgets for candidates that deserve them.

## Core Intuition
Use cheap imperfect signals to eliminate weak trials early; reserve full training budgets for candidates that survive.

## How it Works
1. Define a resource axis, such as epochs, training data, or resolution, and the maximum fidelity.
2. Start many configurations at a cheap fidelity.
3. Observe partial learning curves or validation costs and stop clearly weak trials.
4. Promote promising trials to higher fidelities and return the best fully evaluated candidate.

## Mathematical Foundation
$$
c(\lambda, r), \quad r \in \mathcal{R}
$$

`r` is a resource or fidelity level, such as epochs, data volume, or resolution. Low `r` gives a cheaper but noisier estimate of final cost.

## Key Components
- Configuration
- Fidelity/resource axis
- Partial evaluation
- Promotion rule
- Early-stopping rule
- Maximum budget

## Advantages
- Rejects weak configurations before full training.
- Converts partial learning-curve information into search savings.
- Can trade fidelity bias against much lower evaluation cost.

## Limitations
- Low-fidelity performance may not rank configurations reliably at full budget.
- The method needs a meaningful resource axis and a useful early signal.

## Common Mistakes
- Assuming low-fidelity rankings always match rankings at the final resource level.
- Changing resource levels without defining what resource means for the task.
- Comparing methods at unequal total compute and calling the result an algorithm comparison.

## Real-world Applications
- Budgeted Optimization
- Early Stopping
- Expensive Model Training

## Interview Questions
- What is fidelity, and why can it reduce optimization cost?
- When is early performance a useful proxy for final performance?
- How does multi-fidelity search differ from simply running fewer trials?
- How should total compute be reported in a fair comparison?

## Related Concepts
- HPO Speedup Techniques
- Hyperband / BOHB

## Connections
- Depends on: Hyperparameter Optimization and Bayesian Optimization
- Used in: Early Stopping, Budgeted Optimization, and Expensive Model Training
- Related: Hyperband / BOHB and HPO Speedup Techniques
- Broader topic: AutoML, Resource Allocation, and Optimization

## Prerequisites
- Bayesian Optimization
- Hyperparameter Optimization

## Slide-derived Evidence
- Auto-ML | p5 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=5) — Multi-fidelity optimization Sum of little black boxes (cid:73) Each little black box is fast but only yields a noisy estimate (cid:80)N (cid:73) SMAC [Hutter et al. 2011] directly solves argmin c(λλλ,i) λλλ∈ΛΛΛ i=1 (cid:73) Auto-WEKA [Thornton et al, 2013] used this to optimize 10-fold cross-validation performance Meta-learning across problems / datasets Multi-fidelity optimization
- Auto-ML | p6 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=6) — Multi-fidelity optimization Sum of little black boxes (cid:73) Each little black box is fast but only yields a noisy estimate (cid:80)N (cid:73) SMAC [Hutter et al. 2011] directly solves argmin c(λλλ,i) λλλ∈ΛΛΛ i=1 (cid:73) Auto-WEKA [Thornton et al, 2013] used this to optimize 10-fold cross-validation performance Meta-learning across problems / datasets Multi-fidelity optimization Graybox optimization / learning curve prediction
- Auto-ML | p7 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=7) — Explain the concept of multi-fidelity optimization to speed up HPO Describe many different ways of using meta-learning to speed up HPO Explain the concept of multi-fidelity optimization to speed up HPO Explain the Successive Halving and Hyperband algorithms Explain how to combine Bayesian optimization and Hyperband in BOHB Describe how to exploit multiple fidelities in Bayesian optimization Discuss several ways of predicting learning curves Discuss success stories of speeding up Bayesian optimization
- Auto-ML | p28 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=28) — Multi-Fidelity Optimization In General
- Auto-ML | p29 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=29) — For multi-fidelity optimization to be helpful, performance with low budgets should be General Remarks on Multi-Fidelity Optimization Often, we have a choice which resources we use as budget For multi-fidelity optimization to be helpful, performance with low budgets should be informative about performance with high budgets In the simplest case: good with low resources good with high resources. ↔ (cid:73) In practice, this is of course not always true

## Provenance
- Auto-ML | p5 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=5) — Multi-fidelity optimization Sum of little black boxes (cid:73) Each little black box is fast but only yields a noisy estimate (cid:80)N (cid:73) SMAC [Hutter et al. 2011] directly solves argmin c(λλλ,i) λλλ∈ΛΛΛ i=1 (cid:73) Auto-WEKA [Thornton et al, 2013] used this to optimize 10-fold cross-validation performance Meta-learning across problems / datasets Multi-fidelity optimization
- Auto-ML | p6 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=6) — Multi-fidelity optimization Sum of little black boxes (cid:73) Each little black box is fast but only yields a noisy estimate (cid:80)N (cid:73) SMAC [Hutter et al. 2011] directly solves argmin c(λλλ,i) λλλ∈ΛΛΛ i=1 (cid:73) Auto-WEKA [Thornton et al, 2013] used this to optimize 10-fold cross-validation performance Meta-learning across problems / datasets Multi-fidelity optimization Graybox optimization / learning curve prediction
- Auto-ML | p7 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=7) — Explain the concept of multi-fidelity optimization to speed up HPO Describe many different ways of using meta-learning to speed up HPO Explain the concept of multi-fidelity optimization to speed up HPO Explain the Successive Halving and Hyperband algorithms Explain how to combine Bayesian optimization and Hyperband in BOHB Describe how to exploit multiple fidelities in Bayesian optimization Discuss several ways of predicting learning curves Discuss success stories of speeding up Bayesian optimization
- Auto-ML | p28 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=28) — Multi-Fidelity Optimization In General
- Auto-ML | p29 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=29) — For multi-fidelity optimization to be helpful, performance with low budgets should be General Remarks on Multi-Fidelity Optimization Often, we have a choice which resources we use as budget For multi-fidelity optimization to be helpful, performance with low budgets should be informative about performance with high budgets In the simplest case: good with low resources good with high resources. ↔ (cid:73) In practice, this is of course not always true
- Auto-ML | p57-p58 | [5_Speedup_ALL.pdf](../data/raw/Auto-ML/5_Speedup_ALL.pdf#page=57) — Entropy Search for Multi-Fidelity Optimization Entropy Search for Multi-Fidelity Optimization [Klein, Falkner & Hutter, 2017]
- Auto-ML | p2-p5 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=2) — ▶ E.g., learning curve predictions, multi-fidelity optimization, ...
- Auto-ML | p6 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=6) — ▶ E.g., learning curve predictions, multi-fidelity optimization, ... Often we treat AutoML as a black-box problem ▶ Black box: We choose input to the black box and observe outcome ▶ E.g., classical hyperparameter optimizer: Input: Hyperparameter configuration → Output: Accuracy We discussed how to extend AutoML to a more grey-box approach: ▶ Grey Box: We still choose the input, but we can observe more than the outcome, e.g, intermediate results ▶ We might can control the “box” a bit, e.g., early termination ▶ E.g., learning curve predictions, multi-fidelity optimization, ...
- Auto-ML | p7 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=7) — ▶ E.g., learning curve predictions, multi-fidelity optimization, ... Often we treat AutoML as a black-box problem ▶ Black box: We choose input to the black box and observe outcome ▶ E.g., classical hyperparameter optimizer: Input: Hyperparameter configuration → Output: Accuracy We discussed how to extend AutoML to a more grey-box approach: ▶ Grey Box: We still choose the input, but we can observe more than the outcome, e.g, intermediate results ▶ We might can control the “box” a bit, e.g., early termination ▶ E.g., learning curve predictions, multi-fidelity optimization, ... ⇝ often more efficient than black-box approaches (if done right)
- Auto-ML | p8 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=8) — ▶ E.g., learning curve predictions, multi-fidelity optimization, ... Often we treat AutoML as a black-box problem ▶ Black box: We choose input to the black box and observe outcome ▶ E.g., classical hyperparameter optimizer: Input: Hyperparameter configuration → Output: Accuracy We discussed how to extend AutoML to a more grey-box approach: ▶ Grey Box: We still choose the input, but we can observe more than the outcome, e.g, intermediate results ▶ We might can control the “box” a bit, e.g., early termination ▶ E.g., learning curve predictions, multi-fidelity optimization, ... ⇝ often more efficient than black-box approaches (if done right) Ultimately, we would like to treat AutoML as a white-box problem ▶ White-box: We can observe and control all details of an algorithm run
- Auto-ML | p9 | [8_dac_lectures.pdf](../data/raw/Auto-ML/8_dac_lectures.pdf#page=9) — ▶ E.g., learning curve predictions, multi-fidelity optimization, ... Often we treat AutoML as a black-box problem ▶ Black box: We choose input to the black box and observe outcome ▶ E.g., classical hyperparameter optimizer: Input: Hyperparameter configuration → Output: Accuracy We discussed how to extend AutoML to a more grey-box approach: ▶ Grey Box: We still choose the input, but we can observe more than the outcome, e.g, intermediate results ▶ We might can control the “box” a bit, e.g., early termination ▶ E.g., learning curve predictions, multi-fidelity optimization, ... ⇝ often more efficient than black-box approaches (if done right) Ultimately, we would like to treat AutoML as a white-box problem ▶ White-box: We can observe and control all details of an algorithm run ⇝ Goal: Replace hyperparameter heuristics or even algorithm components by learned policies
- Auto-ML | p54 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=54) — Multi-fidelity optimization Multi-fidelity optimization Learning curve prediction Meta-learning across datasets Network morphisms & weight inheritance Weight sharing & the one-shot model
- Auto-ML | p55 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=55) — NAS Speedup Technique 1: Multi-fidelity optimization Analogous to multi-fidelity optimization in HPO Analogous to multi-fidelity optimization in HPO - Many evaluations for cheaper fidelities (less epochs, smaller datasets, down-sampled images, shallower networks, etc) - Fewer evaluations necessary for more expensive fidelities
- Auto-ML | p56 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=56) — NAS Speedup Technique 1: Multi-fidelity optimization Analogous to multi-fidelity optimization in HPO Analogous to multi-fidelity optimization in HPO - Many evaluations for cheaper fidelities (less epochs, smaller datasets, down-sampled images, shallower networks, etc) - Fewer evaluations necessary for more expensive fidelities Compatible with any blackbox optimization method - Using random search: ASHA [Li and Talwalkar. 2019] - Using Bayesian optimization: BOHB [Zela et al. 2018] - Using di↵erential evolution: DEHB [Awad et al. under review] - Using regularized evolution: progressive dynamic hurdles [So et al. 2019]
- Auto-ML | p57 | [ss25-AutoML-lecture-6 NAS .pdf](../data/raw/Auto-ML/ss25-AutoML-lecture-6 NAS .pdf#page=57) — NAS Speedup Technique 1: Multi-fidelity optimization Analogous to multi-fidelity optimization in HPO Analogous to multi-fidelity optimization in HPO - Many evaluations for cheaper fidelities (less epochs, smaller datasets, down-sampled images, shallower networks, etc) - Fewer evaluations necessary for more expensive fidelities Compatible with any blackbox optimization method - Using random search: ASHA [Li and Talwalkar. 2019] - Using Bayesian optimization: BOHB [Zela et al. 2018] - Using di↵erential evolution: DEHB [Awad et al. under review] - Using regularized evolution: progressive dynamic hurdles [So et al. 2019] Often used for joint optimization of architecture & hyperparameters - Auto-Pytorch [Mendoza et al. 2019; Zimmer et al. 2020] - “Auto-RL” [Runge et al. 2019]

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.624
- evidence strength: 0.7
- definition quality: 0.28
- interview relevance: 0.98
- version: 12
- last updated: 2026-08-05T17:21:13.265392+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- assumptions not extracted
