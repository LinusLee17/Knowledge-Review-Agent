# Knowledge Schema

## Purpose

Canonical concept pages are study guides, not pipeline records. The page should read in the same order a student thinks while revising.

## Canonical Order

1. Title
2. Classification
3. Contributing Courses
4. Definition
5. Why it Matters
6. Core Intuition
7. How it Works
8. Mathematical Foundation
9. Key Components
10. Advantages
11. Limitations
12. Common Mistakes
13. Common Variants
14. Real-world Applications
15. Interview Questions
16. Related Concepts
17. Connections
18. Prerequisites
19. Further Reading
20. Slide-derived Evidence
21. Provenance
22. Extraction Metadata

## Section Rules

- `Classification` should hold domain, topic, concept type, importance, aliases, and broader topics.
- `Contributing Courses` should list source courses that contributed evidence.
- `Why it Matters` should answer why the student should remember this concept.
- `Core Intuition` should give the memorable mental model.
- `How it Works` should describe the mechanism or process in steps.
- `Mathematical Foundation` should use a clean display equation when math is real and complete.
- `Key Components` should name the parts a student needs to recall.
- `Common Variants` should list named variants or subtypes, not simple aliases.
- `Common Mistakes` should highlight misconceptions or failure modes.
- `Connections` should express graph-like relations in prose, such as `Depends on`, `Used in`, or `Related`.
- `Interview Questions` should be actual questions a student can practice.
- `Slide-derived Evidence`, `Provenance`, and `Extraction Metadata` belong at the bottom.

## Definition Quality Requirements

Every accepted concept must have a useful definition. A valid definition should explain:

- what it is
- what problem it solves
- why it matters

Example:

Linear Regression is a statistical modelling method that estimates the relationship between a dependent variable and one or more independent variables by fitting a linear function. It is commonly used for prediction, inference, and understanding variable relationships.

## Mathematical Field Improvements

Do not generate artificial mathematics.

Rules:

- Only populate mathematical foundations when the equation is meaningful.
- Use complete notation and explain the symbols.
- Leave the field empty if the math is incomplete or low value.

Example:

```text
Gradient Descent

\theta_{t+1} = \theta_t - \alpha \nabla J(\theta_t)

| Symbol | Meaning |
| --- | --- |
| \theta_t | Current parameters |
| \alpha | Learning rate |
| \nabla J(\theta_t) | Gradient of the loss |
```

## Application Field Improvements

Applications should represent real-world usage.

Reject:

- Used in examples
- Used in this lecture

Accept:

- Fraud detection
- Customer churn prediction
- Demand forecasting
- Medical diagnosis

## Concept Naming

Concept names should represent durable knowledge units.

Before:

- Accuracy

After:

- Classification Accuracy

Before:

- Regression

After:

- Linear Regression
- Logistic Regression

Avoid overly broad concepts when a more specific canonical name is available.
