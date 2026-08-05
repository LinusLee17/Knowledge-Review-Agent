---
concept_name: "Gradient Descent"
canonical_key: "gradient descent"
concept_type: "method"
domain: "Machine Learning"
topic: "Optimization"
importance_score: 5
scope_level: 3
study_priority: 5
version_number: 23
last_updated_timestamp: "2026-08-05T17:21:13.199037+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Gradient Descent

## Classification
- domain: Machine Learning
- topic: Optimization
- type: method
- scope: 3/5 (core concept or method)
- study priority: 5/5
- also known as: bgd, sgd
- broader topic(s): Model Training

## Contributing Courses
- BT4240
- CS3244

## Definition
Gradient Descent is an iterative optimization method that updates parameters in the direction of steepest decrease of the objective function. It is the standard workhorse for fitting many machine learning models when closed-form solutions are unavailable or too expensive.

## Why it Matters
Gradient Descent is one of the fundamental optimization algorithms in machine learning. It is used to train linear models, logistic regression, neural networks, and many other models by iteratively minimizing a loss function. Understanding Gradient Descent is essential because nearly every modern machine learning algorithm relies on some form of numerical optimization.

## Core Intuition
Move parameters downhill on the loss surface until improvement becomes small or stable.

## How it Works
1. Start from an initial parameter vector.
2. Compute the gradient of the loss at the current point.
3. Move opposite the gradient by a step size set by the learning rate.
4. Repeat until the loss improves only a little or a stopping rule is met.

## Mathematical Foundation
$$
\theta_{t+1} = \theta_t - \alpha \nabla J(\theta_t)
$$

| Symbol | Meaning |
| --- | --- |
| `\theta_t` | Current parameters |
| `\alpha` | Learning rate |
| `\nabla J(\theta_t)` | Gradient of the loss at the current point |

## Key Components
- Objective / loss function
- Parameters
- Gradient
- Learning rate
- Stopping criterion

## Advantages
- Works for large parameter spaces where closed-form optimization is impractical.
- Applies to many differentiable objectives and model architectures.

## Limitations
- A poor learning rate can cause slow convergence or divergence.
- Convergence depends on the objective, initialization, conditioning, and stopping rule.

## Common Mistakes
- Using a learning rate that is too large or too small.
- Forgetting that feature scaling often affects convergence.
- Assuming it always reaches the global optimum.

## Common Variants
- Batch Gradient Descent
- Stochastic Gradient Descent
- Mini-batch Gradient Descent

## Real-world Applications
- Model Fitting
- Neural Networks
- Regression

## Interview Questions
- Why is the learning rate so important?
- How do batch, stochastic, and mini-batch gradient descent differ?
- Why does feature scaling often help convergence?
- Why can gradient descent be slow or unstable?

## Related Concepts
- Learning Rate
- Loss Function
- Regularization

## Connections
- Depends on: objective function, gradient, learning rate
- Used to train: linear regression, logistic regression, neural networks
- Related: loss function, regularization, Newton's method, Adam optimizer

## Prerequisites
- Calculus
- Optimization

## Further Reading
- Bishop, Pattern Recognition and Machine Learning
- Stanford CS229 optimization notes

## Slide-derived Evidence
- BT4240 | p5 | [L1-ContinuousOptimization.pdf](../data/raw/BT4240/L1-ContinuousOptimization.pdf#page=5) — 1. Unconstrained optimization: gradient descent • Gradient descent is a first-order optimization algorithm: start with initial point x , and iterate:
- BT4240 | p21 | [L1-ContinuousOptimization.pdf](../data/raw/BT4240/L1-ContinuousOptimization.pdf#page=21) — 1. Unconstrained optimization: gradient descent Stochastic gradient descent • Stochastic gradient descent is a stochastic approximation of the gradient descent method for minimizing
- BT4240 | p10 | [L2-Regression.pdf](../data/raw/BT4240/L2-Regression.pdf#page=10) — 2. Gradient descent • One way is to apply a guided search algorithm known as gradient descent
- BT4240 | p23 | [L7-NeuralNetworks.pdf](../data/raw/BT4240/L7-NeuralNetworks.pdf#page=23) — • With stochastic gradient descent, when an error occurs, the weight is updated as follows: 2. Objective function in perceptron learning Consider the perceptron criterion: • For y = +1, we want 𝑊. 𝑋 ˃ 0 ; and for y = -1, we want 𝑊. 𝑋 < 0 i i i i • Equivalently, we want y 𝑊. 𝑋 ˃ 0 for all samples (𝑋 , y) i i i i • Any misclassified sample will have y 𝑊. 𝑋 < 0 i i • Hence, we minimize E(𝑊) = - ∑ y𝑊. 𝑋 (cid:3036)(cid:2987)M i i where M denotes the set of all misclassified samples. • With stochastic gradient descent, when an error occurs, the weight is updated as follows: 𝑊 ⇦ 𝑊-  𝛻E(𝑊) where 𝛻E(𝑊) = - 𝑦 𝑋 𝑖 i • Hence: 𝑊 ⇦ 𝑊 +  𝑦 𝑋 (compare with the update on page 12: 𝑊 ⇦ 𝑊 +  E(𝑋) 𝑋 ) 𝑖 i
- CS3244 | p45 | [Lecture04_linear_models_svm.pdf](../data/raw/CS3244/Lecture04_linear_models_svm.pdf#page=45) — Stochastic gradient descent A fast variation of gradient descent that considers only a small set of data points to update the value of the parameters is stochastic gradient descent (SGD):

## Provenance
- BT4240 | p5 | [L1-ContinuousOptimization.pdf](../data/raw/BT4240/L1-ContinuousOptimization.pdf#page=5) — 1. Unconstrained optimization: gradient descent • Gradient descent is a first-order optimization algorithm: start with initial point x , and iterate:
- BT4240 | p21 | [L1-ContinuousOptimization.pdf](../data/raw/BT4240/L1-ContinuousOptimization.pdf#page=21) — 1. Unconstrained optimization: gradient descent Stochastic gradient descent • Stochastic gradient descent is a stochastic approximation of the gradient descent method for minimizing
- BT4240 | p10 | [L2-Regression.pdf](../data/raw/BT4240/L2-Regression.pdf#page=10) — 2. Gradient descent • One way is to apply a guided search algorithm known as gradient descent
- BT4240 | p23 | [L7-NeuralNetworks.pdf](../data/raw/BT4240/L7-NeuralNetworks.pdf#page=23) — • With stochastic gradient descent, when an error occurs, the weight is updated as follows: 2. Objective function in perceptron learning Consider the perceptron criterion: • For y = +1, we want 𝑊. 𝑋 ˃ 0 ; and for y = -1, we want 𝑊. 𝑋 < 0 i i i i • Equivalently, we want y 𝑊. 𝑋 ˃ 0 for all samples (𝑋 , y) i i i i • Any misclassified sample will have y 𝑊. 𝑋 < 0 i i • Hence, we minimize E(𝑊) = - ∑ y𝑊. 𝑋 (cid:3036)(cid:2987)M i i where M denotes the set of all misclassified samples. • With stochastic gradient descent, when an error occurs, the weight is updated as follows: 𝑊 ⇦ 𝑊-  𝛻E(𝑊) where 𝛻E(𝑊) = - 𝑦 𝑋 𝑖 i • Hence: 𝑊 ⇦ 𝑊 +  𝑦 𝑋 (compare with the update on page 12: 𝑊 ⇦ 𝑊 +  E(𝑋) 𝑋 ) 𝑖 i
- CS3244 | p45 | [Lecture04_linear_models_svm.pdf](../data/raw/CS3244/Lecture04_linear_models_svm.pdf#page=45) — Stochastic gradient descent A fast variation of gradient descent that considers only a small set of data points to update the value of the parameters is stochastic gradient descent (SGD):
- CS3244 | p47 | [Lecture04_linear_models_svm.pdf](../data/raw/CS3244/Lecture04_linear_models_svm.pdf#page=47) — Gradient Descent is a universal optimization technique as long as the considered loss is continuous
- CS3244 | p4 | [Lecture10_perceptron_neural_networks.pdf](../data/raw/CS3244/Lecture10_perceptron_neural_networks.pdf#page=4) — 4. Describe how Neural Networks are trained with gradient descent Week 10a: Learning Outcomes 1. Describe the structure of Perceptron and how it performs classification, as well as its relationship with neurons in human brains 2. Understand how Perceptrons are trained with the Perceptron Learning Algorithm 3. Understand how to compose multiple Perceptrons into a Neural Network 4. Describe how Neural Networks are trained with gradient descent and backpropagation [W10b] NUS CS3244: Machine Learning 4

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.924
- evidence strength: 0.96
- definition quality: 0.84
- interview relevance: 0.98
- version: 23
- last updated: 2026-08-05T17:21:13.199037+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- assumptions not extracted
