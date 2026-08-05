---
concept_name: "Probability"
canonical_key: "probability"
concept_type: "theory"
domain: "Statistics"
topic: "Foundations"
importance_score: 5
scope_level: 4
study_priority: 5
version_number: 3
last_updated_timestamp: "2026-07-11T11:37:30.889974+00:00"
explanation_basis: "slide evidence + background synthesis"
---

# Probability

## Classification
- domain: Statistics
- topic: Foundations
- type: theory
- scope: 4/5 (topic or workflow)
- study priority: 5/5
- also known as: probability theory
- broader topic(s): Statistical Foundations

## Contributing Courses
- BT4012
- BT4240
- CS3244
- ST1131

## Definition
Probability is the mathematics of uncertainty. It provides the language for random variables, conditional events, likelihood, calibration, and statistical inference.

## Why it Matters
Probability is the language of uncertainty. It underpins statistical inference, likelihood, Bayes' rule, calibration, and almost every model that reasons about risk or variability.

## Core Intuition
Quantify uncertainty so later models can reason about risk, evidence, and random variation.

## How it Works
1. Define a sample space and the events or random variables of interest.
2. Assign probabilities to events and update them with conditional probability when new information arrives.
3. Use Bayes' rule, joint probabilities, or distributions to reason about uncertainty.

## Mathematical Foundation
$$
P(A \mid B) = \frac{P(A \cap B)}{P(B)}
$$

| Symbol | Meaning |
| --- | --- |
| `P(A)` | Probability of event A |
| `P(A | B)` | Probability of A given B |
| `A \cap B` | Both A and B occur |

## Key Components
- Sample space
- Event
- Random variable
- Conditional probability
- Independence
- Bayes' rule

## Limitations
- Probability cannot be assessed or measured precisely in a small number of

## Common Mistakes
- Confusing independence with mutual exclusivity.
- Treating conditional probability as if it were symmetric.
- Mixing up probability, likelihood, and frequency.

## Common Variants
- Discrete Probability
- Continuous Probability
- Conditional Probability
- Joint Probability

## Real-world Applications
- Forecasting
- Risk Modeling

## Interview Questions
- Why is probability the foundation for statistical inference?
- What is the difference between joint, marginal, and conditional probability?
- How does Bayes' rule update a belief with new evidence?
- What is the difference between independence and mutual exclusivity?

## Related Concepts
- Distribution
- Random Variable

## Connections
- Depends on: sample space, events, random variables
- Used in: hypothesis testing, maximum likelihood estimation, logistic regression
- Related: distributions, expectation, Bayes' rule

## Further Reading
- OpenStax Introductory Statistics
- Any standard introductory probability text

## Slide-derived Evidence
- BT4012 | p40 | [02 Data Visualization and Analysis.pdf](../data/raw/BT4012/02 Data Visualization and Analysis.pdf#page=40) — • What is the probability of observing 60 or more fair, the probability of observing 60 or more
- BT4012 | p23 | [04 Predictive Analytics.pdf](../data/raw/BT4012/04 Predictive Analytics.pdf#page=23) — Many problems require a probability estimate as output. Handy because the probability estimates are calibrated. • Many problems require a probability estimate as output.
- BT4012 | p73 | [05 Deep Learning for Fraud Detection.pdf](../data/raw/BT4012/05 Deep Learning for Fraud Detection.pdf#page=73) — 4 Fraud probability score is generated Output Layer: Probability of transaction being fraudulent
- BT4012 | p23 | [L10_Detecting LLM-Generated Content.pdf](../data/raw/BT4012/L10_Detecting LLM-Generated Content.pdf#page=23) — ○ How surprised a model is by text, measured through probability ■ Perplexity = 2^(-average log probability) high-probability words
- BT4012 | p27 | [L7 Social Network Analysis.pdf](../data/raw/BT4012/L7 Social Network Analysis.pdf#page=27) — 2𝑥𝑦 is the expected probability that an probability 2𝑥𝑦

## Provenance
- BT4012 | p40 | [02 Data Visualization and Analysis.pdf](../data/raw/BT4012/02 Data Visualization and Analysis.pdf#page=40) — • What is the probability of observing 60 or more fair, the probability of observing 60 or more
- BT4012 | p23 | [04 Predictive Analytics.pdf](../data/raw/BT4012/04 Predictive Analytics.pdf#page=23) — Many problems require a probability estimate as output. Handy because the probability estimates are calibrated. • Many problems require a probability estimate as output.
- BT4012 | p73 | [05 Deep Learning for Fraud Detection.pdf](../data/raw/BT4012/05 Deep Learning for Fraud Detection.pdf#page=73) — 4 Fraud probability score is generated Output Layer: Probability of transaction being fraudulent
- BT4012 | p23 | [L10_Detecting LLM-Generated Content.pdf](../data/raw/BT4012/L10_Detecting LLM-Generated Content.pdf#page=23) — ○ How surprised a model is by text, measured through probability ■ Perplexity = 2^(-average log probability) high-probability words
- BT4012 | p27 | [L7 Social Network Analysis.pdf](../data/raw/BT4012/L7 Social Network Analysis.pdf#page=27) — 2𝑥𝑦 is the expected probability that an probability 2𝑥𝑦
- BT4012 | p54 | [L7 Social Network Analysis.pdf](../data/raw/BT4012/L7 Social Network Analysis.pdf#page=54) — Restart Probability • With a probability of 𝛼, the surfer will follow a link on the web page he/she is currently visitin,g and with a probability of (1 − 𝛼), the surfer visits a random other
- BT4240 | p51 | [L2-Regression.pdf](../data/raw/BT4240/L2-Regression.pdf#page=51) — • A Bernoulli trial is an experiment with 2 possible outcomes: success and failure with probability of success = π and probability of failure = 1 – π, where 0 ≤ π ≤ 1. • A Bernoulli random variable Y is defined by the probability mass function:
- BT4240 | p53 | [L2-Regression.pdf](../data/raw/BT4240/L2-Regression.pdf#page=53) — • The probability distribution function of Y is: log(a)N = N log(a) • Since the Y observations are independent, their joint probability function is: • Taking the logarithm of the joint probability function:
- BT4240 | p64 | [L2-Regression.pdf](../data/raw/BT4240/L2-Regression.pdf#page=64) — • There are 53 class 1 and 147 class 0 samples. Fit probability of class 1 with: = Y = 53/200.
- BT4240 | p10 | [L4-InformationBasedLearning.pdf](../data/raw/BT4240/L4-InformationBasedLearning.pdf#page=10) — • Shannon (1949) used the base 2 logarithm of the assigned probability: • Large probability of receiving a message P(M) leads to small I(M) and vice versa. P = 1 and P is the probability of receiving the i-th message.
- BT4240 | p27 | [L4-InformationBasedLearning.pdf](../data/raw/BT4240/L4-InformationBasedLearning.pdf#page=27) — ls ℓi∈n𝑙𝑙 𝑙𝑙t𝑙𝑙h𝑙𝑙e𝑙𝑙𝑙𝑙 d(𝑡𝑡o)main of target feature t, P(t = ℓ) is the probability of an instance in D having
- BT4240 | p8 | [L6-GeneticAlgorithm.pdf](../data/raw/BT4240/L6-GeneticAlgorithm.pdf#page=8) — • It is usually randomised, with the probability of selection proportional to the fitness. 2. The components of GA The components of GA 3. Selection strategy: (continued) • It is usually randomised, with the probability of selection proportional to the fitness. • If individual X scores twice as high as individual Y on the fitness function, then X is twice more likely to be selected for reproduction than Y. • Usually, selection is done with replacement, so that a very fit individual will get to reproduce several times.
- BT4240 | p32 | [L6-GeneticAlgorithm.pdf](../data/raw/BT4240/L6-GeneticAlgorithm.pdf#page=32) — Credit scoring is employed to identify customers’ default probability. 6. Applications of GA Applications of GA: A paper that describes the application of GP for predicting customer default: An artificial intelligence system for predicting customer default in e-commerce by L. Vanneschi, predicting customer default D.M. Horn, M. Castelli and A Popovic, Expert Systems with Applications, 104 (2018), pp. 1-21. Default payment: customer fails to settle a bill within 90 days upon receipt. Credit scoring is employed to identify customers’ default probability.
- BT4240 | p7 | [L8-BayesianLearning.pdf](../data/raw/BT4240/L8-BayesianLearning.pdf#page=7) — • A probability function describes the probability each possible value of a • A joint probability distribution is a probability distribution over more than • It is written as a matrix where each cell lists the probability of a particular
- BT4240 | p8 | [L8-BayesianLearning.pdf](../data/raw/BT4240/L8-BayesianLearning.pdf#page=8) — • The probability of an event X, given some evidence Y is defined in terms of the product of the inverse conditional probability P(Y|X) and the prior probabilities P(X).
- BT4240 | p9 | [L8-BayesianLearning.pdf](../data/raw/BT4240/L8-BayesianLearning.pdf#page=9) — • Bad news: patient tested positive for a serious disease, the test is 99% accurate: the probability of testing positive when the patient has the disease is 0.99 and the probability of testing negative when the patient does not have the disease is 0.99.
- BT4240 | p12 | [L8-BayesianLearning.pdf](../data/raw/BT4240/L8-BayesianLearning.pdf#page=12) — • The conditional probability: • Query: What is the probability that
- BT4240 | p15 | [L8-BayesianLearning.pdf](../data/raw/BT4240/L8-BayesianLearning.pdf#page=15) — • New query: what is the probability that a patient has Meningitis when Headache = true, Fever = true, Vomiting =
- BT4240 | p16 | [L8-BayesianLearning.pdf](../data/raw/BT4240/L8-BayesianLearning.pdf#page=16) — • Two events are said to be independent of each other if knowledge of one event has no effect on the probability of the other event, The probability that the patient has fever (X) is not changed even when we know that he has a headache (Y). If we already know the patient has meningitis (Z), knowing that he has a headache (Y) will not affect the probability of him having
- BT4240 | p3 | [L9-BayesianNetworks.pdf](../data/raw/BT4240/L9-BayesianNetworks.pdf#page=3) — Full joint probability distribution: Grow at an exponential rate as new features are added to the domain as joint probability distribution Full joint probability distributions are not tractable for any reasonable domain
- BT4240 | p14 | [L9-BayesianNetworks.pdf](../data/raw/BT4240/L9-BayesianNetworks.pdf#page=14) — Learning the parameters (Conditional probability tables): Probability of burglary P(B): Probability of alarm goes off when there is burglary and earthquake:
- BT4240 | p25 | [L9-BayesianNetworks.pdf](../data/raw/BT4240/L9-BayesianNetworks.pdf#page=25) — The calculation of a probability becomes computationally complex very quickly, particularly An alternative is to approximate probability distribution by sample generation.
- BT4240 | p30 | [L9-BayesianNetworks.pdf](../data/raw/BT4240/L9-BayesianNetworks.pdf#page=30) — true, there is a 0.9 probability that probability that rain is true.
- CS3244 | p30 | [Lecture04_linear_models_svm.pdf](../data/raw/CS3244/Lecture04_linear_models_svm.pdf#page=30) — Logistic regression predicts “soft” classes, i.e. is interpreted as a probability of class [0,1].
- CS3244 | p31 | [Lecture04_linear_models_svm.pdf](../data/raw/CS3244/Lecture04_linear_models_svm.pdf#page=31) — Prediction function is the probability in [0,1] that the person had a heart attack. Probability of having class y given the input data x Conditioned probability a.k.a. likelihood probability
- CS3244 | p9 | [Lecture05_bias_variance.pdf](../data/raw/CS3244/Lecture05_bias_variance.pdf#page=9) — A random variable (X,Ω,P) is a variable X that can have different values x Ω controlled by a probability probability of the outcome, i.e. . Random variable A random variable (X,Ω,P) is a variable X that can have different values x Ω controlled by a probability distribution, P(X x). ∈ For example, a coin can be represented by a random variable X. = The set Ω of all outcomes of the coin is Ω { Head , Tail }. The probabilities of the outcomes are P(X H) 1/2 and P(X T) 1/2 if the coin is fair, i.e. not = biased to any particular side. = = = = Expected value of X : Average value over all possible outcomes of a random variable X weighted by the probability of the outcome, i.e. . Example: Let X be the outco m e o f a fxa∈irX d i c e ro ll . T h en, the expected value is 𝔼𝔼 X = ∑ x P r ( X = x ) (X)=1/6.(1+2+3+4+5+6)=3.5. Variance of X : Variation of a random variable from the expected value, i.e. 𝔼𝔼 (X) . 2 2 Ex a m ple: L et X b e the ou tcxo∈Xme of a fair d ic e ro ll. T hen, the variance is Var(X ) = 𝔼𝔼 X − 𝔼𝔼 ( X ) = ∑ x − 𝔼𝔼 P r ( X = x ) Var(X)=1/6.( (1−3.5)2+…+(6−3.5)2 )=35/12. 9
- ST1131 | p1-p2, p4-p17, p19-p35 | [Topic0_Introduction.pdf](../data/raw/ST1131/Topic0_Introduction.pdf#page=1) — 1 Learn about simple distributions; basic probability; statistical concepts 4 Probability
- ST1131 | p3 | [Topic0_Introduction.pdf](../data/raw/ST1131/Topic0_Introduction.pdf#page=3) — 1 Learn about simple distributions; basic probability; statistical concepts 4 Probability Goals of This Course 1 Learn about simple distributions; basic probability; statistical concepts 2 Know how to produce and to use statistical graphics
- ST1131 | p18 | [Topic0_Introduction.pdf](../data/raw/ST1131/Topic0_Introduction.pdf#page=18) — 4 Probability 1 Learn about simple distributions; basic probability; statistical concepts Topics 1 Introduction to R programming 2 Exploratory Data Analysis (EDA) 3 Collecting Data 4 Probability 5 Random Variables (Discrete and Continuous Random Variables) 6 Sampling Distribution 7 Statistical Estimation 8 Hypothesis Testing 9 Linear Regression 10 Some Limitations of Linear Regression (extra topic if time permits)
- ST1131 | p32 | [Topic2_EDA_1.pdf](../data/raw/ST1131/Topic2_EDA_1.pdf#page=32) — Left histogram was created using probability (or density). Histograms for a BMI Variable Body mass index (BMI) of 34 people. From right histogram: one person has BMI from 10 to 15; 4 people have BMI 15 to 20; etc. Left histogram was created using probability (or density).
- ST1131 | p1-p30, p32-p35, p37 | [Topic2_EDA_3.pdf](../data/raw/ST1131/Topic2_EDA_3.pdf#page=1) — Histogram with bars of probability and more information added Form a histogram (by frequency and then by probability) with color, title.
- ST1131 | p31 | [Topic2_EDA_3.pdf](../data/raw/ST1131/Topic2_EDA_3.pdf#page=31) — Histogram with bars of probability and more information added Form a histogram (by frequency and then by probability) with color, title. Forming Histograms We once again consider variable of midterm marks. The simplest histogram: > # hist(mark) > # this produces a histogram with grey color and bars of frequency Histogram with bars of probability and more information added > # hist(mark, prob = TRUE, col = 2, xlab = "Midterm Marks", > # ylab = "Density", > # main = "Histogram of the Midterm Marks)
- ST1131 | p36 | [Topic2_EDA_3.pdf](../data/raw/ST1131/Topic2_EDA_3.pdf#page=36) — Form a histogram (by frequency and then by probability) with color, title. Histogram with bars of probability and more information added For Your Try Lets use variable BMI as given in the code (cid:28)le. Get the numerical summaries for this variable. Form a histogram (by frequency and then by probability) with color, title. Form a boxplot and identify if this variable has any outlier. Comment if the distribution of BMI is symmetric.
- ST1131 | p1-p11, p13-p27 | [Topic2_EDA_4.pdf](../data/raw/ST1131/Topic2_EDA_4.pdf#page=1) — The ratio 39.5/31.8 = 1.24 tells us: the probability of having breast cancer among PMH users is 1.24 times the probability of having breast cancer
- ST1131 | p12 | [Topic2_EDA_4.pdf](../data/raw/ST1131/Topic2_EDA_4.pdf#page=12) — The ratio 39.5/31.8 = 1.24 tells us: the probability of having breast cancer among PMH users is 1.24 times the probability of having breast cancer Contingency Tables: Comparing Proportions/Percentages When cancer status is the response, comparing the percentages of having cancer among 2 groups of pmh.use is helpful. The raw di(cid:27)erence: (39.5 - 31.8) is a statistic that can help to explore the association. The ratio 39.5/31.8 = 1.24 tells us: the probability of having breast cancer among PMH users is 1.24 times the probability of having breast cancer among non-users. If the ratio is signi(cid:28)cantly di(cid:27)erent from 1, we can infer the association between breast cancer and PMH usage.
- ST1131 | p8 | [Topic2_EDA_5.pdf](../data/raw/ST1131/Topic2_EDA_5.pdf#page=8) — If we want to compare the probability of cancer among PMH users versus Row-wise or Column-wise Percentage Contingency Table Percentage contingency table could be row-wise or column-wise, depending on the purpose of analysis. If we want to compare the probability of cancer among PMH users versus non-PMH users, then we need to condition our proportions on pmh.use. Since pmh.use is the rows, we do a row-wise percentage contingency table > prop.table(tab, "pmh.use")*100 cancer pmh.use Absent Present No 68.2 31.8 Yes 60.5 39.5 Sometimes, you might do a column-wise percentage contingency table > prop.table(tab, "cancer")*100 cancer pmh.use Absent Present No 84.93151 80.10076 Yes 15.06849 19.89924
- ST1131 | p1 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=1) — Probability Topic04-Probability ST1131 1/65 3 Probability
- ST1131 | p2-p3, p8-p9, p15, p20, p24, p37, p45, p51, p57 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=2) — 3 Probability Conditional Probability Law of Total Probability
- ST1131 | p4 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=4) — Topic04-Probability ST1131 4/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p5 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=5) — Conditional probability Law of total probability Topic04-Probability ST1131 5/65
- ST1131 | p6 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=6) — Why Do We Need Probability? probability. Topic04-Probability ST1131 6/65
- ST1131 | p7 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=7) — Why Do We Need Probability? Probability enables us to quantify this uncertainty. What is probability?
- ST1131 | p10 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=10) — Topic04-Probability ST1131 10/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p11 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=11) — Topic04-Probability ST1131 11/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p12 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=12) — We’ll discuss about this more when calculating probability. Topic04-Probability ST1131 12/65 Probability
- ST1131 | p13 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=13) — Topic04-Probability ST1131 13/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p14 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=14) — Topic04-Probability ST1131 14/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p16 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=16) — Topic04-Probability ST1131 16/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p17 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=17) — Topic04-Probability ST1131 17/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p18 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=18) — Topic04-Probability ST1131 18/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p19 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=19) — Topic04-Probability ST1131 19/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p21 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=21) — Probability De(cid:28)nition 5 (Probability) The probability of an event is the proportion of times that this event occurs, in
- ST1131 | p22 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=22) — Topic04-Probability ST1131 22/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p23 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=23) — Topic04-Probability ST1131 23/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p25 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=25) — Axioms of Probability Let A be an event within sample space S, P(A) = probability of event A. Topic04-Probability ST1131 25/65
- ST1131 | p26 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=26) — Axioms of Probability (cont) 5 (Additive Law of Probability) For any three events A, B, C: Topic04-Probability ST1131 26/65
- ST1131 | p27 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=27) — Tossing a fair coin (Probability of heads is 0.5) Topic04-Probability ST1131 27/65 Probability
- ST1131 | p28 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=28) — Topic04-Probability ST1131 28/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p29 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=29) — What is probability that Jack is right in front of Jill (no one else is between Topic04-Probability ST1131 29/65 Probability
- ST1131 | p30 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=30) — These results, along with the axioms, can be used to (cid:28)nd the probability of Topic04-Probability ST1131 30/65 Probability
- ST1131 | p31 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=31) — Topic04-Probability ST1131 31/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p32 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=32) — Topic04-Probability ST1131 32/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p33 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=33) — What is the probability that a sampled individual is Male, or someone who Topic04-Probability ST1131 33/65 Probability
- ST1131 | p34 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=34) — has equally likely outcomes, then the probability of event can be derived Topic04-Probability ST1131 34/65 Probability
- ST1131 | p35 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=35) — all possible) and then estimate the true probability. Thus, the sample Topic04-Probability ST1131 35/65 Probability
- ST1131 | p36 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=36) — Topic04-Probability ST1131 36/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p38 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=38) — Topic04-Probability ST1131 38/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p39 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=39) — Topic04-Probability ST1131 39/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p40 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=40) — Topic04-Probability ST1131 40/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p41 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=41) — Topic04-Probability ST1131 41/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p42 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=42) — Topic04-Probability ST1131 42/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p43 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=43) — Topic04-Probability ST1131 43/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p44 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=44) — Topic04-Probability ST1131 44/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p46 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=46) — De(cid:28)nition 7 (Conditional Probability) The conditional probability of A given B is de(cid:28)ned to be Topic04-Probability ST1131 46/65
- ST1131 | p47 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=47) — Topic04-Probability ST1131 47/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p48 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=48) — Q1 Estimate the probability of a positive test for a random pregnant woman. Q2 Given that the diagnostic test is positive, estimate the probability that Down Topic04-Probability ST1131 48/65
- ST1131 | p49 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=49) — Topic04-Probability ST1131 49/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p50 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=50) — The Connection Between Independence and Conditional Probability From the de(cid:28)nition of conditional probability, we know that Topic04-Probability ST1131 50/65
- ST1131 | p52-p53 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=52) — Topic04-Probability ST1131 52/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p54 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=54) — The Law of Total Probability Topic04-Probability ST1131 53/65 Probability
- ST1131 | p55 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=55) — If a product is randomly sampled, what is the probability that it is defective? Topic04-Probability ST1131 54/65 Probability
- ST1131 | p56 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=56) — Topic04-Probability ST1131 55/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p58 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=58) — Topic04-Probability ST1131 57/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p59 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=59) — Topic04-Probability ST1131 58/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p60 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=60) — Q A random sampled product was defective, what is the probability that it Topic04-Probability ST1131 59/65 Probability
- ST1131 | p61 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=61) — The sensitivity of a test is the probability that the test is positive, given that the Topic04-Probability ST1131 60/65 Probability
- ST1131 | p62 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=62) — The speci(cid:28)city of a test is the probability that the test is negative, given that Topic04-Probability ST1131 61/65 Probability
- ST1131 | p63 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=63) — Topic04-Probability ST1131 62/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p64 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=64) — What is the probability that a person with a positive test result actually has Topic04-Probability ST1131 63/65 Probability
- ST1131 | p65 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=65) — Topic04-Probability ST1131 64/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p66 | [Topic4_Probability.pdf](../data/raw/ST1131/Topic4_Probability.pdf#page=66) — Topic04-Probability ST1131 65/65 Probability Topic04-Probability ST1131 1/65
- ST1131 | p1-p9, p15-p18, p21, p23-p31, p34, p37-p43, p45, p51-p52, p54-p77, p79-p83 | [Topic5_RandomVariables.pdf](../data/raw/ST1131/Topic5_RandomVariables.pdf#page=1) — Probability Distribution of a Variable In Example 1, each possible outcome of variable X has a specific probability The probability distribution of a random variable specifies its possible
- ST1131 | p10 | [Topic5_RandomVariables.pdf](../data/raw/ST1131/Topic5_RandomVariables.pdf#page=10) — Its probability distribution assigns a probability p to each possible value of X. For each x, the probability p is between 0 and 1. Probability Distribution of a Variable
- ST1131 | p11 | [Topic5_RandomVariables.pdf](../data/raw/ST1131/Topic5_RandomVariables.pdf#page=11) — Probability Distribution when Tossing a Coin Twice Then X has probability distribution as below. Probability Distribution of a Variable
- ST1131 | p12 | [Topic5_RandomVariables.pdf](../data/raw/ST1131/Topic5_RandomVariables.pdf#page=12) — Probability Distribution when Rolling Two Dice Then Y is a discrete variable which has probability distribution below. Probability Distribution of a Variable
- ST1131 | p13 | [Topic5_RandomVariables.pdf](../data/raw/ST1131/Topic5_RandomVariables.pdf#page=13) — Bar Plot To Visualize a Probability Distribution For Discrete Random Probability Distribution of a Variable In Example 1, each possible outcome of variable X has a specific probability
- ST1131 | p14 | [Topic5_RandomVariables.pdf](../data/raw/ST1131/Topic5_RandomVariables.pdf#page=14) — follows this probability distribution: Probability Distribution of a Variable In Example 1, each possible outcome of variable X has a specific probability
- ST1131 | p19 | [Topic5_RandomVariables.pdf](../data/raw/ST1131/Topic5_RandomVariables.pdf#page=19) — random variable M that follows this probability distribution: Probability Distribution of a Variable In Example 1, each possible outcome of variable X has a specific probability
- ST1131 | p20 | [Topic5_RandomVariables.pdf](../data/raw/ST1131/Topic5_RandomVariables.pdf#page=20) — The mean of the probability distribution of a random variable X is also probability distribution, the sample mean of those observations would be close to the mean of that probability distribution.
- ST1131 | p22 | [Topic5_RandomVariables.pdf](../data/raw/ST1131/Topic5_RandomVariables.pdf#page=22) — have same probability distribution hence have the same mean µ. Probability Distribution of a Variable In Example 1, each possible outcome of variable X has a specific probability
- ST1131 | p32 | [Topic5_RandomVariables.pdf](../data/raw/ST1131/Topic5_RandomVariables.pdf#page=32) — Its probability distribution is specified by a curve that helps determine probabilities of intervals. This curve is referred to as a probability density Each interval will have probability between 0 and 1. This is the area under
- ST1131 | p33 | [Topic5_RandomVariables.pdf](../data/raw/ST1131/Topic5_RandomVariables.pdf#page=33) — Visualizing a Probability Distribution by PDF Curve We use a bar plot to represent the probability distribution for a discrete Probability Distribution of a Variable
- ST1131 | p35 | [Topic5_RandomVariables.pdf](../data/raw/ST1131/Topic5_RandomVariables.pdf#page=35) — If we were interested in the probability that the measurement of the If it’s given that this area is 0.232, then the required probability is Probability Distribution of a Variable
- ST1131 | p36 | [Topic5_RandomVariables.pdf](../data/raw/ST1131/Topic5_RandomVariables.pdf#page=36) — If we were interested in the probability that the measurement of the If it’s given that this area is 0.202 then the required probability is Probability Distribution of a Variable
- ST1131 | p44 | [Topic5_RandomVariables.pdf](../data/raw/ST1131/Topic5_RandomVariables.pdf#page=44) — When a probability distribution is given, we must be comfortable using statistical Find probability: given a value x, what is the area under the curve to the Find quantile: given a probability p, what is x such that the area to the left
- ST1131 | p46 | [Topic5_RandomVariables.pdf](../data/raw/ST1131/Topic5_RandomVariables.pdf#page=46) — Each trial has the same probability of success p. distribution with success probability p. Probability Distribution of a Variable
- ST1131 | p47 | [Topic5_RandomVariables.pdf](../data/raw/ST1131/Topic5_RandomVariables.pdf#page=47) — with probability 0.6. Then Z, a random variable for the total number of The probability of a woman developing breast cancer over a lifetime is 1/9. Probability Distribution of a Variable
- ST1131 | p48 | [Topic5_RandomVariables.pdf](../data/raw/ST1131/Topic5_RandomVariables.pdf#page=48) — Then the probability of x successes in these n trials is Probability Distribution of a Variable In Example 1, each possible outcome of variable X has a specific probability
- ST1131 | p49 | [Topic5_RandomVariables.pdf](../data/raw/ST1131/Topic5_RandomVariables.pdf#page=49) — Using the Binomial Probability Distribution Probability Distribution of a Variable In Example 1, each possible outcome of variable X has a specific probability
- ST1131 | p50 | [Topic5_RandomVariables.pdf](../data/raw/ST1131/Topic5_RandomVariables.pdf#page=50) — Probability of at Least Five Matches The outcome of interest is a match, which would happen with probability In essence, we need to find the probability of at least 5 matches out of 10.
- ST1131 | p53 | [Topic5_RandomVariables.pdf](../data/raw/ST1131/Topic5_RandomVariables.pdf#page=53) — What is the probability distribution of the number of deaths over a Let X be the number of deaths in 6 months. Find the probability Let Y be the number of deaths in 3 months. Find the probability
- ST1131 | p78 | [Topic5_RandomVariables.pdf](../data/raw/ST1131/Topic5_RandomVariables.pdf#page=78) — Find the probability P(X ≤ c) where c is given. Given a probability, find a quantile value from a distribution. Probability Distribution of a Variable
- ST1131 | p1-p5, p11-p13, p20-p24 | [Topic5_RandomVariables_R.pdf](../data/raw/ST1131/Topic5_RandomVariables_R.pdf#page=1) — Finding Probability What is the probability of having IQ of less than 135 in the population? pnorm: probability
- ST1131 | p6 | [Topic5_RandomVariables_R.pdf](../data/raw/ST1131/Topic5_RandomVariables_R.pdf#page=6) — What is the probability of having IQ of less than 135 in the population? Finding Probability pnorm: probability
- ST1131 | p7 | [Topic5_RandomVariables_R.pdf](../data/raw/ST1131/Topic5_RandomVariables_R.pdf#page=7) — pnorm: probability Finding Probability What is the probability of having IQ of less than 135 in the population?
- ST1131 | p8 | [Topic5_RandomVariables_R.pdf](../data/raw/ST1131/Topic5_RandomVariables_R.pdf#page=8) — Assuming IQ ∼ N(100,15 ), what is the probability of having IQ of less Finding Probability What is the probability of having IQ of less than 135 in the population?
- ST1131 | p9 | [Topic5_RandomVariables_R.pdf](../data/raw/ST1131/Topic5_RandomVariables_R.pdf#page=9) — What about the probability of having IQ of more than 135? Finding Probability What is the probability of having IQ of less than 135 in the population?
- ST1131 | p10 | [Topic5_RandomVariables_R.pdf](../data/raw/ST1131/Topic5_RandomVariables_R.pdf#page=10) — The function qnorm can be used with 3 main inputs (probability, mean, Finding Probability What is the probability of having IQ of less than 135 in the population?
- ST1131 | p14 | [Topic5_RandomVariables_R.pdf](../data/raw/ST1131/Topic5_RandomVariables_R.pdf#page=14) — What is the probability of having X less than or equal to 60 heads? Finding Probability What is the probability of having IQ of less than 135 in the population?
- ST1131 | p15 | [Topic5_RandomVariables_R.pdf](../data/raw/ST1131/Topic5_RandomVariables_R.pdf#page=15) — pbinom: probability Finding Probability What is the probability of having IQ of less than 135 in the population?
- ST1131 | p16 | [Topic5_RandomVariables_R.pdf](../data/raw/ST1131/Topic5_RandomVariables_R.pdf#page=16) — Assuming X ∼ Bin(100,0.5), what is the probability of having X less than Finding Probability What is the probability of having IQ of less than 135 in the population?
- ST1131 | p17 | [Topic5_RandomVariables_R.pdf](../data/raw/ST1131/Topic5_RandomVariables_R.pdf#page=17) — What about the probability of having X more than 60 heads? Finding Probability What is the probability of having IQ of less than 135 in the population?
- ST1131 | p18 | [Topic5_RandomVariables_R.pdf](../data/raw/ST1131/Topic5_RandomVariables_R.pdf#page=18) — What about the probability of having X less than 60 heads? Finding Probability What is the probability of having IQ of less than 135 in the population?
- ST1131 | p19 | [Topic5_RandomVariables_R.pdf](../data/raw/ST1131/Topic5_RandomVariables_R.pdf#page=19) — The function qbinom can be used with 3 main inputs (probability, n, Finding Probability What is the probability of having IQ of less than 135 in the population?
- ST1131 | p1-p11, p13, p15-p49 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=1) — pˆ hence is a random variable. What is the probability distribution of pˆ? A sampling distribution is merely a type of probability distribution. It The probability distribution of X is then
- ST1131 | p12 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=12) — A sampling distribution is merely a type of probability distribution. It pˆ hence is a random variable. What is the probability distribution of pˆ? The probability distribution of X is then
- ST1131 | p14 | [Topic6_SamplingDistribution.pdf](../data/raw/ST1131/Topic6_SamplingDistribution.pdf#page=14) — The probability distribution of X is then pˆ hence is a random variable. What is the probability distribution of pˆ? A sampling distribution is merely a type of probability distribution. It
- ST1131 | p1-p23, p25-p30, p32-p44, p46-p62 | [Topic7_CI.pdf](../data/raw/ST1131/Topic7_CI.pdf#page=1) — parameter. The probability that this method produces an interval that contains This ensures that there is a 0.95 probability that the interval contains the Error Probability
- ST1131 | p24 | [Topic7_CI.pdf](../data/raw/ST1131/Topic7_CI.pdf#page=24) — This ensures that there is a 0.95 probability that the interval contains the parameter. The probability that this method produces an interval that contains Error Probability
- ST1131 | p31 | [Topic7_CI.pdf](../data/raw/ST1131/Topic7_CI.pdf#page=31) — Error Probability For a 95% confidence interval, there is a probability of 0.05 that it does not parameter. The probability that this method produces an interval that contains
- ST1131 | p45 | [Topic7_CI.pdf](../data/raw/ST1131/Topic7_CI.pdf#page=45) — where t is quantile of probability 0.975 from a t . parameter. The probability that this method produces an interval that contains This ensures that there is a 0.95 probability that the interval contains the
- ST1131 | p1-p12, p15-p36, p38-p44, p46-p55, p61-p63 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=1) — It uses probability to quantify how plausible a value for a parameter is. We’ll use a probability to summarize the evidence against the null, H , that probability in the null distribution. The probability that“the test statistic
- ST1131 | p13 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=13) — We’ll use a probability to summarize the evidence against the null, H , that It uses probability to quantify how plausible a value for a parameter is. probability in the null distribution. The probability that“the test statistic
- ST1131 | p14 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=14) — probability in the null distribution. The probability that“the test statistic It uses probability to quantify how plausible a value for a parameter is. We’ll use a probability to summarize the evidence against the null, H , that
- ST1131 | p37 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=37) — H : µ (cid:54)= µ Two tail probability from t It uses probability to quantify how plausible a value for a parameter is. We’ll use a probability to summarize the evidence against the null, H , that
- ST1131 | p45 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=45) — probability (right area of 31.3 and left area of -31.3) which is close to 0. It uses probability to quantify how plausible a value for a parameter is. We’ll use a probability to summarize the evidence against the null, H , that
- ST1131 | p56-p58 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=56) — The probability that this happens is denoted by β. probability of correctly rejecting H , when it is in fact false. The probability that Type I error happens is denoted by α.
- ST1131 | p59 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=59) — The probability that Type I error happens is denoted by α. The probability that this happens is denoted by β. probability of correctly rejecting H , when it is in fact false.
- ST1131 | p60 | [Topic8_HypothesisTest.pdf](../data/raw/ST1131/Topic8_HypothesisTest.pdf#page=60) — chances of having a Type I error.However, this will increase the probability (cid:73) When H is retained more often, the probability to retain it when it is not correct will increase. Thus, probability of Type II error will increase.
- ST1131 | p15 | [Topic8_HypothesisTest_2.pdf](../data/raw/ST1131/Topic8_HypothesisTest_2.pdf#page=15) — H : µ −µ (cid:54)= 0 Two tail probability from t Steps 4 and 5: Derive p-Value p-value depends on whether the alternative hypothesis is one- or two-sided. Alternative hypothesis p-Value H : µ −µ (cid:54)= 0 Two tail probability from t 1 X Y n1+n2−2 H : µ −µ > 0 Right area of T from t 1 X Y n1+n2−2 H : µ −µ < 0 Left area of T from t 1 X Y n1+n2−2
- ST1131 | p4 | [Topic8_QQplots_R.pdf](../data/raw/ST1131/Topic8_QQplots_R.pdf#page=4) — probability that the population follows it as well. Normality Assumption One of the assumptions required in the test for a population mean µ is that the population distribution is approximately Normal. This assumption is crucial when n is small. We need to check if the population distribution is approximately Normal. However, we do not have the population distribution. Hence, we need to check this assumption using the sample distribution instead. If the sample distribution is approximately Normal, then there is a high probability that the population follows it as well.

## Extraction Metadata
- explanation basis: slide evidence + background synthesis
- confidence: 0.973
- evidence strength: 0.98
- definition quality: 0.96
- interview relevance: 0.98
- version: 3
- last updated: 2026-07-11T11:37:30.889974+00:00

## Quality Review
- This page needs human review before treated as authoritative:
- assumptions not extracted
