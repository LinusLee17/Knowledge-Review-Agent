---
concept_name: "Entropy"
canonical_key: "entropy"
concept_type: "theory"
domain: "Statistics"
topic: "Information Theory"
importance_score: 4
scope_level: 4
study_priority: 4
version_number: 3
last_updated_timestamp: "2026-08-05T16:27:50.400785+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Entropy

## Classification
- domain: Statistics
- topic: Information Theory
- type: theory
- scope: 4/5 (topic or workflow)
- study priority: 4/5
- also known as: shannon entropy
- broader topic(s): Model Evaluation

## Contributing Courses
- BT4240
- CS3244

## Definition
Entropy is a formal account that connects assumptions, objects, and implications in Information Theory. It is used in Classification, Decision Trees.

## Why it Matters
Entropy turns an informal question—“how uncertain or mixed is this distribution?”—into a quantity used to compare splits, evaluate predictive distributions, and reason about information. Decision-tree algorithms use entropy reduction to prefer features that make child nodes more class-pure.

## Core Intuition
Think of probability mass as uncertainty. If one class dominates, the next label is predictable and entropy is low. If classes are balanced, the next label is harder to predict and entropy is high. A split is useful when its weighted child distributions are less uncertain than the parent distribution.

## How it Works
1. Define outcome classes and estimate valid probabilities \(p_1,\ldots,p_c\) that sum to 1.
2. Compute parent entropy from the probability distribution.
3. For a candidate decision-tree split, compute each child entropy and weight it by child size.
4. Compare parent entropy with weighted child entropy using information gain.
5. Select the split only in context: high gain can favor many-valued features, noisy estimates, or unstable small leaves.

## Key Components
- Outcome classes or events
- Probability distribution \(p_1,\ldots,p_c\)
- Logarithm base and unit (bits for base 2)
- Parent and child distributions for split evaluation
- Weighted conditional entropy and information gain

## Mathematical Foundation
For discrete random variable \(X\) with outcomes \(x_1,\ldots,x_c\) and probabilities \(p_i=P(X=x_i)\):

\[
H(X)=-\sum_{i=1}^{c}p_i\log_b p_i.
\]

Here \(p_i\ge 0\), \(\sum_i p_i=1\), and convention \(0\log 0=0\) applies. Base \(b=2\) measures entropy in bits; changing base rescales value but not ordering of distributions. For binary class with probability (p):

\[
H(p)=-p\log_2p-(1-p)\log_2(1-p).
\]

For split (A) with child sets (S_v), remaining entropy is:

\[
H(S\mid A)=\sum_v\frac{|S_v|}{|S|}H(S_v),
\qquad
IG(S,A)=H(S)-H(S\mid A).
\]

## Advantages
- Gives interpretable uncertainty and impurity values.
- Supports multiclass distributions and decision-tree split selection.
- Connects probability, coding intuition, and information gain.

## Limitations
- Value depends on the estimated distribution and can be unstable with small samples.
- Entropy alone does not identify which class is wrong or whether a feature is causally useful.
- Information gain can favor features with many possible values; compare with alternatives such as gain ratio or Gini impurity.
- Cross-entropy and entropy are related but not interchangeable: cross-entropy evaluates a predicted distribution against a target distribution.

## Common Mistakes
- Calling entropy high when one class dominates; concentration lowers entropy.
- Forgetting that probabilities must form a valid distribution.
- Treating information gain as causal evidence rather than a split-quality criterion.
- Confusing entropy of a target distribution with cross-entropy loss of predictions.

## Real-world Applications
- Classification
- Decision Trees

## Interview Questions
- Derive entropy for a fair binary distribution and for a distribution where one class has probability 1. Why do values differ?
- What do the probability values, logarithm base, and units mean in (H(X))?
- How does a decision tree use entropy to calculate information gain?
- Why can information gain prefer a feature with many distinct values?
- Distinguish entropy, conditional entropy, cross-entropy, and Gini impurity.
- When would you inspect calibration or log loss instead of entropy alone?

## Related Concepts
- Cross Entropy
- Information Gain

## Connections
- Depends on: Probability
- Used in: Classification and Decision Trees
- Related: Information Gain and Cross Entropy
- Broader topic: Information Theory and Model Evaluation

## Prerequisites
- Probability

## Background Enrichment
The coding interpretation explains why logarithms appear: independent information amounts add because logarithms turn probability products into sums. In modeling, entropy describes a target or predictive distribution; cross-entropy measures mismatch between target and predicted distributions.

## Slide-derived Evidence
- BT4240 | p10 | [L4-InformationBasedLearning.pdf](../data/raw/BT4240/L4-InformationBasedLearning.pdf#page=10) — Shannon’s Entropy model • Entropy is computed to measure the amount of information in a message. • The overall measure of expected surprise is given by the entropy formula
- BT4240 | p12 | [L4-InformationBasedLearning.pdf](../data/raw/BT4240/L4-InformationBasedLearning.pdf#page=12) — Shannon’s Entropy model • Suppose the collection S consists of positive examples and negative examples of same target concept, the entropy S Entropy = - p log p - p log p
- BT4240 | p13 | [L4-InformationBasedLearning.pdf](../data/raw/BT4240/L4-InformationBasedLearning.pdf#page=13) — Shannon’s Entropy model • Entropy specifies the number of bits of information needed to encode classification of a member of S that has been • If p = 1, then Entropy = 0. The receiver knows that a random example will be positive so that no message need be
- CS3244 | p15 | [Lecture03_decision_trees.pdf](../data/raw/CS3244/Lecture03_decision_trees.pdf#page=15) — The entropy of the subsets S ,…,S is defined as Finally, the information gain (IG) is the difference between the entropy of the original set S and the weighted sum of the entropy of the subset S .

## Provenance
- BT4240 | p10 | [L4-InformationBasedLearning.pdf](../data/raw/BT4240/L4-InformationBasedLearning.pdf#page=10) — Shannon’s Entropy model • Entropy is computed to measure the amount of information in a message. • The overall measure of expected surprise is given by the entropy formula
- BT4240 | p12 | [L4-InformationBasedLearning.pdf](../data/raw/BT4240/L4-InformationBasedLearning.pdf#page=12) — Shannon’s Entropy model • Suppose the collection S consists of positive examples and negative examples of same target concept, the entropy S Entropy = - p log p - p log p
- BT4240 | p13 | [L4-InformationBasedLearning.pdf](../data/raw/BT4240/L4-InformationBasedLearning.pdf#page=13) — Shannon’s Entropy model • Entropy specifies the number of bits of information needed to encode classification of a member of S that has been • If p = 1, then Entropy = 0. The receiver knows that a random example will be positive so that no message need be
- CS3244 | p15 | [Lecture03_decision_trees.pdf](../data/raw/CS3244/Lecture03_decision_trees.pdf#page=15) — The entropy of the subsets S ,…,S is defined as Finally, the information gain (IG) is the difference between the entropy of the original set S and the weighted sum of the entropy of the subset S .

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.86
- evidence strength: 0.84
- definition quality: 0.8
- interview relevance: 0.98
- version: 3
- last updated: 2026-08-05T16:27:50.400785+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- no meaningful equation or formal relationship extracted
- assumptions not extracted
- trade-offs or limitations not extracted
