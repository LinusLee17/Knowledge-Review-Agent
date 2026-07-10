from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable

from .models import ConceptCandidate
from .utils import normalize_concept_key, normalize_spaces


@dataclass(frozen=True)
class ConceptProfile:
    concept_name: str
    domain: str
    topic: str
    importance_score: int
    synonyms: tuple[str, ...]
    concept_type: str = "concept"
    prerequisites: tuple[str, ...] = ()
    related_concepts: tuple[str, ...] = ()
    broader_topics: tuple[str, ...] = ()
    applications: tuple[str, ...] = ()


CONCEPT_PROFILES: tuple[ConceptProfile, ...] = (
    ConceptProfile(
        concept_name="Linear Regression",
        domain="Statistics",
        topic="Regression",
        importance_score=5,
        concept_type="model",
        synonyms=("linear regression", "ols regression", "regression model", "least squares regression", "simple linear regression", "multiple linear regression"),
        prerequisites=("Statistics", "Matrix Algebra"),
        related_concepts=("Logistic Regression", "Ridge Regression", "Lasso Regression", "Regularization"),
        broader_topics=("Regression", "Statistical Modeling"),
        applications=("Prediction", "Forecasting", "Business Analytics"),
    ),
    ConceptProfile(
        concept_name="Logistic Regression",
        domain="Machine Learning",
        topic="Supervised Learning",
        importance_score=5,
        concept_type="model",
        synonyms=("logistic regression", "binary logistic regression"),
        prerequisites=("Linear Regression", "Probability"),
        related_concepts=("Classification", "Regularization"),
        broader_topics=("Supervised Learning",),
        applications=("Classification", "Customer Churn", "Risk Scoring"),
    ),
    ConceptProfile(
        concept_name="Decision Trees",
        domain="Machine Learning",
        topic="Supervised Learning",
        importance_score=5,
        concept_type="algorithm",
        synonyms=("decision tree", "decision trees", "tree model"),
        prerequisites=("Entropy", "Gini Impurity"),
        related_concepts=("Random Forest", "Gradient Boosting", "Classification"),
        broader_topics=("Supervised Learning", "Tree-Based Models"),
        applications=("Classification", "Regression", "Decision Analysis"),
    ),
    ConceptProfile(
        concept_name="Random Forest",
        domain="Machine Learning",
        topic="Ensemble Methods",
        importance_score=5,
        concept_type="algorithm",
        synonyms=("random forest", "random forests"),
        prerequisites=("Decision Trees", "Bagging"),
        related_concepts=("Gradient Boosting", "XGBoost", "Decision Trees"),
        broader_topics=("Ensemble Methods", "Tree-Based Models"),
        applications=("Healthcare Prediction", "Fraud Detection", "Customer Analytics"),
    ),
    ConceptProfile(
        concept_name="Gradient Descent",
        domain="Machine Learning",
        topic="Optimization",
        importance_score=5,
        concept_type="method",
        synonyms=("gradient descent", "batch gradient descent", "stochastic gradient descent", "mini-batch gradient descent", "sgd", "bgd"),
        prerequisites=("Optimization", "Calculus"),
        related_concepts=("Learning Rate", "Loss Function", "Regularization"),
        broader_topics=("Optimization", "Model Training"),
        applications=("Model Fitting", "Neural Networks", "Regression"),
    ),
    ConceptProfile(
        concept_name="Regularization",
        domain="Machine Learning",
        topic="Model Selection",
        importance_score=5,
        concept_type="method",
        synonyms=("regularization", "ridge regularization", "lasso regularization"),
        prerequisites=("Linear Regression", "Logistic Regression"),
        related_concepts=("Ridge Regression", "Lasso Regression", "Overfitting"),
        broader_topics=("Model Selection", "Bias-Variance Tradeoff"),
        applications=("Feature Selection", "Generalization"),
    ),
    ConceptProfile(
        concept_name="PCA",
        domain="Data Science",
        topic="Dimensionality Reduction",
        importance_score=5,
        concept_type="method",
        synonyms=("pca", "principal component analysis", "principal components analysis"),
        prerequisites=("Linear Algebra", "Variance"),
        related_concepts=("Dimensionality Reduction", "Feature Engineering"),
        broader_topics=("Unsupervised Learning",),
        applications=("Visualization", "Compression", "Noise Reduction"),
    ),
    ConceptProfile(
        concept_name="Hypothesis Testing",
        domain="Statistics",
        topic="Inference",
        importance_score=5,
        concept_type="method",
        synonyms=("hypothesis testing", "test of hypothesis", "significance testing"),
        prerequisites=("Probability", "Sampling"),
        related_concepts=("p-value", "Confidence Interval", "Type I Error", "Type II Error"),
        broader_topics=("Statistical Inference",),
        applications=("Experimentation", "A/B Testing"),
    ),
    ConceptProfile(
        concept_name="Confidence Interval",
        domain="Statistics",
        topic="Inference",
        importance_score=5,
        concept_type="metric",
        synonyms=("confidence interval", "confidence intervals"),
        prerequisites=("Sampling", "Estimation"),
        related_concepts=("Hypothesis Testing", "Margin of Error"),
        broader_topics=("Statistical Inference",),
        applications=("Reporting Uncertainty", "Estimation"),
    ),
    ConceptProfile(
        concept_name="Probability",
        domain="Statistics",
        topic="Foundations",
        importance_score=5,
        concept_type="theory",
        synonyms=("probability", "probability theory"),
        prerequisites=(),
        related_concepts=("Distribution", "Random Variable"),
        broader_topics=("Statistical Foundations",),
        applications=("Risk Modeling", "Forecasting"),
    ),
    ConceptProfile(
        concept_name="Forecasting",
        domain="Business Analytics",
        topic="Predictive Analytics",
        importance_score=4,
        concept_type="workflow",
        synonyms=("forecasting", "time series forecasting"),
        prerequisites=("Trend", "Seasonality"),
        related_concepts=("Prediction", "Linear Regression", "Exponential Smoothing"),
        broader_topics=("Predictive Analytics",),
        applications=("Demand Forecasting", "Sales Forecasting"),
    ),
    ConceptProfile(
        concept_name="Predictive Analytics",
        domain="Business Analytics",
        topic="Analytics Workflow",
        importance_score=5,
        concept_type="workflow",
        synonyms=("predictive analytics",),
        prerequisites=("Regression", "Classification"),
        related_concepts=("Forecasting", "Customer Analytics"),
        broader_topics=("Analytics",),
        applications=("Churn Prediction", "Demand Forecasting"),
    ),
    ConceptProfile(
        concept_name="Customer Analytics",
        domain="Business Analytics",
        topic="Applied Analytics",
        importance_score=4,
        concept_type="workflow",
        synonyms=("customer analytics", "customer segmentation"),
        prerequisites=("Segmentation", "Classification"),
        related_concepts=("Predictive Analytics", "Clustering"),
        broader_topics=("Business Analytics",),
        applications=("Retention", "Churn", "Targeting"),
    ),
    ConceptProfile(
        concept_name="Business Intelligence",
        domain="Business Analytics",
        topic="Reporting",
        importance_score=4,
        concept_type="workflow",
        synonyms=("business intelligence", "bi"),
        prerequisites=("Data Visualization", "Dashboards"),
        related_concepts=("Analytics", "Reporting"),
        broader_topics=("Business Analytics",),
        applications=("Management Reporting", "Decision Support"),
    ),
    ConceptProfile(
        concept_name="Data Cleaning",
        domain="Data Science",
        topic="Data Preparation",
        importance_score=4,
        concept_type="workflow",
        synonyms=("data cleaning", "data preprocessing", "data wrangling"),
        prerequisites=("Missing Values", "Outliers"),
        related_concepts=("Feature Engineering", "Data Transformation"),
        broader_topics=("Data Preparation",),
        applications=("Pipeline Preparation", "Modeling"),
    ),
    ConceptProfile(
        concept_name="Feature Engineering",
        domain="Data Science",
        topic="Data Preparation",
        importance_score=4,
        concept_type="workflow",
        synonyms=("feature engineering",),
        prerequisites=("Data Cleaning", "Domain Knowledge"),
        related_concepts=("Model Performance", "Regularization"),
        broader_topics=("Data Preparation",),
        applications=("Modeling", "Prediction"),
    ),
    ConceptProfile(
        concept_name="Cross Validation",
        domain="Machine Learning",
        topic="Model Evaluation",
        importance_score=4,
        concept_type="method",
        synonyms=("cross validation", "cross-validation", "k-fold cross validation"),
        prerequisites=("Train Test Split", "Sampling"),
        related_concepts=("Overfitting", "Model Selection"),
        broader_topics=("Model Evaluation",),
        applications=("Hyperparameter Tuning", "Generalization"),
    ),
    ConceptProfile(
        concept_name="Classification Accuracy",
        domain="Machine Learning",
        topic="Model Evaluation",
        importance_score=4,
        concept_type="metric",
        synonyms=("accuracy", "classification accuracy", "classification accuracy metric"),
        prerequisites=("Confusion Matrix",),
        related_concepts=("Precision", "Recall", "Confusion Matrix"),
        broader_topics=("Model Evaluation",),
        applications=("Classification Evaluation",),
    ),
    ConceptProfile(
        concept_name="Precision",
        domain="Machine Learning",
        topic="Model Evaluation",
        importance_score=4,
        concept_type="metric",
        synonyms=("precision", "positive predictive value"),
        prerequisites=("Confusion Matrix",),
        related_concepts=("Recall", "Classification Accuracy", "Confusion Matrix"),
        broader_topics=("Model Evaluation",),
        applications=("Classification Evaluation",),
    ),
    ConceptProfile(
        concept_name="Recall",
        domain="Machine Learning",
        topic="Model Evaluation",
        importance_score=4,
        concept_type="metric",
        synonyms=("recall", "sensitivity", "true positive rate"),
        prerequisites=("Confusion Matrix",),
        related_concepts=("Precision", "Classification Accuracy", "Confusion Matrix"),
        broader_topics=("Model Evaluation",),
        applications=("Classification Evaluation",),
    ),
    ConceptProfile(
        concept_name="Confusion Matrix",
        domain="Machine Learning",
        topic="Model Evaluation",
        importance_score=4,
        concept_type="metric",
        synonyms=("confusion matrix",),
        prerequisites=("Classification",),
        related_concepts=("Classification Accuracy", "Precision", "Recall"),
        broader_topics=("Model Evaluation",),
        applications=("Classification Evaluation",),
    ),
    ConceptProfile(
        concept_name="Maximum Likelihood Estimation",
        domain="Statistics",
        topic="Estimation",
        importance_score=5,
        concept_type="method",
        synonyms=("maximum likelihood estimation", "maximum likelihood", "mle"),
        prerequisites=("Probability",),
        related_concepts=("Log-Likelihood", "Logistic Regression"),
        broader_topics=("Statistical Inference",),
        applications=("Parameter Estimation",),
    ),
    ConceptProfile(
        concept_name="Entropy",
        domain="Statistics",
        topic="Information Theory",
        importance_score=4,
        concept_type="theory",
        synonyms=("entropy", "shannon entropy"),
        prerequisites=("Probability",),
        related_concepts=("Information Gain", "Cross Entropy"),
        broader_topics=("Information Theory", "Model Evaluation"),
        applications=("Classification", "Decision Trees"),
    ),
    ConceptProfile(
        concept_name="Area Under Curve",
        domain="Machine Learning",
        topic="Model Evaluation",
        importance_score=4,
        concept_type="metric",
        synonyms=("area under the curve", "auc", "roc auc"),
        prerequisites=("ROC Curve",),
        related_concepts=("Precision", "Recall", "Confusion Matrix"),
        broader_topics=("Model Evaluation",),
        applications=("Classification Evaluation",),
    ),
    ConceptProfile(
        concept_name="F1 Score",
        domain="Machine Learning",
        topic="Model Evaluation",
        importance_score=4,
        concept_type="metric",
        synonyms=("f1 score", "f score"),
        prerequisites=("Precision", "Recall"),
        related_concepts=("Classification Accuracy", "Precision", "Recall"),
        broader_topics=("Model Evaluation",),
        applications=("Classification Evaluation",),
    ),
    ConceptProfile(
        concept_name="Overfitting",
        domain="Machine Learning",
        topic="Model Evaluation",
        importance_score=4,
        concept_type="phenomenon",
        synonyms=("overfitting",),
        prerequisites=("Bias-Variance Tradeoff",),
        related_concepts=("Regularization", "Cross Validation"),
        broader_topics=("Model Evaluation",),
        applications=("Model Diagnostics",),
    ),
    ConceptProfile(
        concept_name="Bias-Variance Tradeoff",
        domain="Machine Learning",
        topic="Model Evaluation",
        importance_score=4,
        concept_type="principle",
        synonyms=("bias variance tradeoff", "bias-variance tradeoff"),
        prerequisites=("Overfitting", "Underfitting"),
        related_concepts=("Regularization", "Cross Validation"),
        broader_topics=("Model Evaluation",),
        applications=("Model Selection",),
    ),
    ConceptProfile(
        concept_name="Support Vector Machine",
        domain="Machine Learning",
        topic="Classification",
        importance_score=4,
        concept_type="algorithm",
        synonyms=("support vector machine", "svm"),
        prerequisites=("Optimization", "Margin"),
        related_concepts=("Classification", "Kernel Trick"),
        broader_topics=("Supervised Learning",),
        applications=("Classification",),
    ),
    ConceptProfile(
        concept_name="K-Means Clustering",
        domain="Machine Learning",
        topic="Clustering",
        importance_score=4,
        concept_type="algorithm",
        synonyms=("k-means", "k means clustering", "k-means clustering"),
        prerequisites=("Distance Metric", "Centroid"),
        related_concepts=("Clustering", "PCA"),
        broader_topics=("Unsupervised Learning",),
        applications=("Customer Segmentation",),
    ),
)


_PROFILE_BY_KEY: dict[str, ConceptProfile] = {}
for profile in CONCEPT_PROFILES:
    for alias in (profile.concept_name, *profile.synonyms):
        _PROFILE_BY_KEY[normalize_concept_key(alias)] = profile


DOMAIN_KEYWORDS: dict[str, tuple[str, ...]] = {
    "Business Analytics": ("predictive analytics", "business intelligence", "customer analytics", "forecasting", "decision analysis", "optimization"),
    "Machine Learning": ("machine learning", "classification", "regression", "random forest", "gradient descent", "svm", "neural network", "regularization", "cross validation", "overfitting", "pca", "clustering"),
    "Statistics": ("statistics", "probability", "hypothesis testing", "confidence interval", "sampling", "estimation", "regression", "distribution"),
    "Data Science": ("data science", "data cleaning", "feature engineering", "visualization", "pipeline", "deployment", "ethics"),
}


TOPIC_KEYWORDS: dict[str, tuple[str, ...]] = {
    "Regression": ("regression", "linear model", "ols", "logistic regression"),
    "Supervised Learning": ("decision tree", "random forest", "classification", "support vector machine"),
    "Ensemble Methods": ("random forest", "gradient boosting", "bagging", "boosting", "xgboost"),
    "Optimization": ("gradient descent", "loss function", "minimize", "maximize", "learning rate"),
    "Model Evaluation": ("cross validation", "overfitting", "bias variance", "validation", "generalization"),
    "Inference": ("hypothesis testing", "confidence interval", "p-value", "estimation"),
    "Predictive Analytics": ("forecasting", "predictive analytics", "customer analytics"),
    "Data Preparation": ("feature engineering", "data cleaning", "data wrangling", "preprocessing"),
    "Clustering": ("k-means", "cluster", "centroid"),
}


_FIELD_CUES: dict[str, tuple[str, ...]] = {
    "definition": (" is ", " are ", " refers to ", " means ", " defined as ", " model that ", " method that ", " approach that "),
    "intuition": ("intuition", "intuitively", "idea", "goal", "aim", "in practice", "helps", "captures", "seek", "used to"),
    "math": ("=", "minimize", "maximize", "argmin", "argmax", "beta", "theta", "sigma", "variance", "log", "exp", "sum", "∑", "sqrt"),
    "assumptions": ("assumption", "assumes", "requires", "under the assumption", "conditions"),
    "applications": ("used for", "applied to", "application", "applications", "for ", "in ", "predict", "classify", "forecast", "segment", "estimate"),
    "limitations": ("limitation", "limitations", "drawback", "drawbacks", "fails", "sensitive", "problem", "not suitable", "cannot"),
    "advantages": ("advantage", "advantages", "benefit", "benefits", "strength", "strengths", "simple", "interpretable", "efficient", "robust"),
    "prerequisites": ("prerequisite", "background", "need", "requires", "must know", "review"),
    "related_concepts": ("related to", "compare", "contrast", "also", "similar to", "see also"),
    "broader_topics": ("topic", "chapter", "module", "domain"),
}


def _normalize(text: str) -> str:
    return normalize_spaces(text).lower()


def canonical_candidate_label(label: str) -> str:
    text = normalize_spaces(label)
    text = re.sub(r"\((.*?)\)", r" \1 ", text)
    text = re.sub(r"\s+", " ", text).strip(" -:;,.")
    lower = text.lower()
    for separator in (" for ", " in ", " on ", " via ", " using ", " with "):
        if separator in lower:
            left, right = lower.split(separator, 1)
            if len(left.split()) >= 1 and len(right.split()) >= 1:
                text = text[: len(left)].strip()
                break
    return normalize_spaces(text)


def profile_for_label(label: str) -> ConceptProfile | None:
    cleaned = canonical_candidate_label(label)
    return _PROFILE_BY_KEY.get(normalize_concept_key(cleaned))


def infer_domain(label: str, context_text: str = "") -> str:
    lower = f"{label} {context_text}".lower()
    for domain, keywords in DOMAIN_KEYWORDS.items():
        if any(keyword in lower for keyword in keywords):
            return domain
    profile = profile_for_label(label)
    return profile.domain if profile else ""


def infer_topic(label: str, context_text: str = "") -> str:
    lower = f"{label} {context_text}".lower()
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(keyword in lower for keyword in keywords):
            return topic
    profile = profile_for_label(label)
    return profile.topic if profile else ""


def importance_for_label(label: str, context_text: str = "", course_name: str = "", page_count_hint: int = 0) -> int:
    lower = f"{label} {context_text} {course_name}".lower()
    profile = profile_for_label(label)
    score = profile.importance_score if profile else 1

    if profile and any(alias in _normalize(context_text) for alias in (profile.concept_name.lower(), *profile.synonyms)):
        score = max(score, 4)
    if any(keyword in lower for keyword in ("cross validation", "regression", "classification", "probability", "forecast", "decision tree", "random forest")):
        score = max(score, 4)
    if any(keyword in lower for keyword in ("linear regression", "random forest", "gradient descent", "hypothesis testing", "confidence interval", "pca")):
        score = max(score, 5)
    if "example" in lower or "exercise" in lower or "worked example" in lower:
        score = min(score, 2)
    if page_count_hint > 1:
        score = max(score, 3)
    return min(5, max(1, score))


def matches_candidate(label: str, context_text: str = "") -> bool:
    profile = profile_for_label(label)
    if profile:
        return True

    lower = f"{label} {context_text}".lower()
    if any(keyword in lower for keyword in ("regression", "classification", "clustering", "forecast", "probability", "hypothesis", "confidence interval", "decision tree", "random forest", "gradient descent", "regularization", "pca", "support vector machine", "k-means", "feature engineering", "data cleaning", "business intelligence", "predictive analytics", "customer analytics")):
        return True
    return False


def extract_section_lines(lines: list[str], cues: Iterable[str], limit: int = 3) -> list[str]:
    results: list[str] = []
    lowered_cues = [cue.lower() for cue in cues]
    for line in lines:
        lower = line.lower()
        if any(cue in lower for cue in lowered_cues):
            cleaned = normalize_spaces(line)
            if cleaned and cleaned not in results:
                results.append(cleaned)
            if len(results) >= limit:
                break
    return results


def extract_formula_lines(lines: list[str], concept_name: str, limit: int = 3) -> list[str]:
    results: list[str] = []
    target = normalize_concept_key(concept_name)
    for line in lines:
        lower = line.lower()
        if any(token in lower for token in ("=", "minimize", "maximize", "argmin", "argmax", "beta", "theta", "sigma", "variance", "loss")):
            if target and target.split() and any(token in lower for token in target.split()):
                cleaned = normalize_spaces(line)
                if cleaned not in results:
                    results.append(cleaned)
            elif len(line.split()) <= 20:
                cleaned = normalize_spaces(line)
                if cleaned not in results:
                    results.append(cleaned)
        if len(results) >= limit:
            break
    return results


def candidate_labels_from_text(lines: list[str], heading: str = "") -> list[str]:
    candidates: list[str] = []
    texts = [heading, *lines]
    for text in texts:
        cleaned = canonical_candidate_label(text)
        if not cleaned:
            continue
        if matches_candidate(cleaned, " ".join(lines)):
            candidates.append(cleaned)
    seen: set[str] = set()
    deduped: list[str] = []
    for label in candidates:
        key = normalize_concept_key(label)
        if key and key not in seen:
            seen.add(key)
            deduped.append(label)
    return deduped


def split_alias_and_application(label: str) -> tuple[str, list[str]]:
    raw = normalize_spaces(label)
    suffix_match = re.match(r"^(.*?)(?:\bfor\b|\bin\b|\bon\b|\busing\b|\bwith\b)\s+(.+)$", raw, flags=re.IGNORECASE)
    if suffix_match:
        base = canonical_candidate_label(suffix_match.group(1))
        suffix = normalize_spaces(suffix_match.group(2))
        profile = profile_for_label(base)
        if profile:
            return profile.concept_name, [suffix]
        return base, [suffix]

    cleaned = canonical_candidate_label(label)
    profile = profile_for_label(cleaned)
    if profile:
        return profile.concept_name, []
    return cleaned, []


def concept_aliases(label: str) -> list[str]:
    profile = profile_for_label(label)
    if not profile:
        return []
    aliases = {profile.concept_name, *profile.synonyms}
    return sorted({normalize_spaces(alias) for alias in aliases if normalize_spaces(alias)})


_CANONICAL_SUMMARIES: dict[str, str] = {
    "Linear Regression": (
        "Linear Regression is a statistical modeling method that estimates the relationship between a response variable "
        "and one or more predictors by fitting a linear function. It is a baseline method for prediction and inference "
        "because coefficients are easy to interpret and the model is simple to diagnose."
    ),
    "Logistic Regression": (
        "Logistic Regression is a classification model that maps a linear score into a probability using the logistic "
        "function. It is widely used when the goal is to predict class membership, estimate odds, and produce a model "
        "that remains interpretable enough for business and technical review."
    ),
    "Gradient Descent": (
        "Gradient Descent is an iterative optimization method that updates parameters in the direction of steepest "
        "decrease of the objective function. It is the standard workhorse for fitting many machine learning models when "
        "closed-form solutions are unavailable or too expensive."
    ),
    "Probability": (
        "Probability is the mathematics of uncertainty. It provides the language for random variables, conditional "
        "events, likelihood, calibration, and statistical inference."
    ),
    "Maximum Likelihood Estimation": (
        "Maximum Likelihood Estimation chooses the parameter values that make the observed data most probable under the "
        "assumed model. It is a core estimation principle that connects probabilistic modeling, log-likelihood, and many "
        "classical statistical estimators."
    ),
    "Recall": (
        "Recall is a classification metric that measures the fraction of actual positive cases that a model correctly "
        "identifies. It matters when missing a positive case is more costly than producing a false alarm."
    ),
}

_CANONICAL_INTUITION: dict[str, str] = {
    "Linear Regression": "Fit the best linear line or plane, then read coefficients as marginal effects under the model assumptions.",
    "Logistic Regression": "Model class probability directly, then threshold it for classification when needed.",
    "Gradient Descent": "Move parameters downhill on the loss surface until improvement becomes small or stable.",
    "Probability": "Quantify uncertainty so later models can reason about risk, evidence, and random variation.",
    "Maximum Likelihood Estimation": "Pick the parameters that best explain the observed sample under the model.",
    "Recall": "Count how many real positives you captured, not just how many predictions were correct overall.",
}

_CANONICAL_MATH: dict[str, str] = {
    "Linear Regression": (
        "$$\n"
        "\\hat{y} = \\beta_0 + \\beta_1 x_1 + \\dots + \\beta_p x_p\n"
        "$$\n\n"
        "| Symbol | Meaning |\n"
        "| --- | --- |\n"
        "| `\\hat{y}` | Predicted value |\n"
        "| `\\beta` | Model coefficients |\n"
        "| `x` | Input features |\n"
        "| `\\epsilon` | Residual / error term |"
    ),
    "Logistic Regression": (
        "$$\n"
        "p(y = 1 \\mid x) = \\sigma(\\beta_0 + \\beta^T x)\n"
        "$$\n\n"
        "$$\n"
        "\\sigma(z) = \\frac{1}{1 + e^{-z}}\n"
        "$$\n\n"
        "| Symbol | Meaning |\n"
        "| --- | --- |\n"
        "| `p(y = 1 | x)` | Probability of class 1 |\n"
        "| `\\sigma` | Sigmoid function |\n"
        "| `\\beta` | Coefficients |\n"
        "| `x` | Features |"
    ),
    "Gradient Descent": (
        "$$\n"
        "\\theta_{t+1} = \\theta_t - \\alpha \\nabla J(\\theta_t)\n"
        "$$\n\n"
        "| Symbol | Meaning |\n"
        "| --- | --- |\n"
        "| `\\theta_t` | Current parameters |\n"
        "| `\\alpha` | Learning rate |\n"
        "| `\\nabla J(\\theta_t)` | Gradient of the loss at the current point |"
    ),
    "Probability": (
        "$$\n"
        "P(A \\mid B) = \\frac{P(A \\cap B)}{P(B)}\n"
        "$$\n\n"
        "| Symbol | Meaning |\n"
        "| --- | --- |\n"
        "| `P(A)` | Probability of event A |\n"
        "| `P(A | B)` | Probability of A given B |\n"
        "| `A \\cap B` | Both A and B occur |"
    ),
    "Maximum Likelihood Estimation": (
        "$$\n"
        "\\hat{\\theta} = \\arg\\max_{\\theta} \\prod_i p(x_i \\mid \\theta)\n"
        "$$\n\n"
        "Often we maximize the log-likelihood instead:\n\n"
        "$$\n"
        "\\ell(\\theta) = \\sum_i \\log p(x_i \\mid \\theta)\n"
        "$$"
    ),
    "Recall": (
        "$$\n"
        "\\text{Recall} = \\frac{TP}{TP + FN}\n"
        "$$\n\n"
        "| Symbol | Meaning |\n"
        "| --- | --- |\n"
        "| `TP` | True positives |\n"
        "| `FN` | False negatives |"
    ),
}

_CANONICAL_INTERVIEW_NOTES: dict[str, list[str]] = {
    "Linear Regression": [
        "Know OLS objective, residual interpretation, and coefficient meaning.",
        "Know assumptions: linearity, independence, homoscedasticity, and low multicollinearity.",
        "Know when linear regression fails: non-linear relationships and strong outliers.",
    ],
    "Logistic Regression": [
        "Know odds, log-odds, and why the sigmoid maps scores to probabilities.",
        "Know how regularization and thresholds affect decision boundaries.",
        "Know why it is preferred when interpretability matters.",
    ],
    "Gradient Descent": [
        "Know the role of the learning rate and the risk of divergence or slow convergence.",
        "Know the difference between batch, stochastic, and mini-batch updates.",
        "Know why feature scaling often matters.",
    ],
    "Probability": [
        "Know conditional probability, independence, and Bayes' rule.",
        "Know how probability connects to likelihood and calibration.",
        "Know Bernoulli, random variables, and uncertainty quantification.",
    ],
    "Maximum Likelihood Estimation": [
        "Know the log-likelihood objective and why we usually maximize the log form.",
        "Know the connection to cross-entropy and probabilistic classifiers.",
        "Know how MLE differs from MAP when priors are added.",
    ],
    "Recall": [
        "Know the trade-off between recall and precision.",
        "Know why recall matters in medical screening, fraud detection, and other high-cost-miss settings.",
        "Know how class imbalance can make accuracy misleading.",
    ],
}

_CANONICAL_FURTHER_READING: dict[str, list[str]] = {
    "Linear Regression": [
        "James, Witten, Hastie, Tibshirani, An Introduction to Statistical Learning",
        "scikit-learn linear regression documentation",
    ],
    "Logistic Regression": [
        "James, Witten, Hastie, Tibshirani, An Introduction to Statistical Learning",
        "scikit-learn logistic regression documentation",
    ],
    "Gradient Descent": [
        "Bishop, Pattern Recognition and Machine Learning",
        "Stanford CS229 optimization notes",
    ],
    "Probability": [
        "OpenStax Introductory Statistics",
        "Any standard introductory probability text",
    ],
    "Maximum Likelihood Estimation": [
        "Casella and Berger, Statistical Inference",
        "Murphy, Machine Learning: A Probabilistic Perspective",
    ],
    "Recall": [
        "scikit-learn classification metrics documentation",
        "Any standard machine learning evaluation reference",
    ],
}


def _canonical_name(label: str) -> str:
    profile = profile_for_label(label)
    return profile.concept_name if profile else canonical_candidate_label(label)


def _unique_text_list(values: Iterable[str]) -> list[str]:
    results: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = normalize_spaces(str(value or ""))
        if not text:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        results.append(text)
    return results


def _join_items(values: Iterable[str], *, limit: int = 3) -> str:
    items = _unique_text_list(values)[:limit]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + f", and {items[-1]}"


def canonical_summary_for_label(label: str) -> str:
    canonical = _canonical_name(label)
    summary = _CANONICAL_SUMMARIES.get(canonical, "")
    if summary:
        return summary
    profile = profile_for_label(label)
    if not profile:
        return ""
    focus = profile.topic or profile.domain or "the target domain"
    return (
        f"{canonical} is a {profile.concept_type or 'concept'} in {profile.domain or 'the target domain'} "
        f"focused on {focus}. It is a durable idea worth remembering because it appears repeatedly in the course material."
    )


def canonical_intuition_for_label(label: str) -> str:
    canonical = _canonical_name(label)
    intuition = _CANONICAL_INTUITION.get(canonical, "")
    if intuition:
        return intuition
    profile = profile_for_label(label)
    if not profile:
        return ""
    if profile.concept_type in {"algorithm", "method", "workflow"}:
        return (
            f"Think of {canonical} as a repeatable procedure: start with the inputs, apply the core rule, "
            f"and keep updating or refining until the result stabilizes."
        )
    if profile.concept_type in {"model"}:
        return (
            f"Think of {canonical} as a way to turn inputs into predictions or scores by fitting parameters "
            f"to the data under a chosen objective."
        )
    if profile.concept_type in {"metric"}:
        return (
            f"Think of {canonical} as a summary number: it compresses many outcomes into one interpretable value "
            f"so you can compare models or decisions."
        )
    if profile.concept_type in {"theory"}:
        return (
            f"Think of {canonical} as the language that makes the rest of the topic precise; it defines the objects, "
            f"relationships, and assumptions used later."
        )
    return f"Think of {canonical} as a durable building block in {profile.topic or profile.domain or 'the course material'}."


def canonical_math_for_label(label: str) -> str:
    canonical = _canonical_name(label)
    math = _CANONICAL_MATH.get(canonical, "")
    if math:
        return math
    profile = profile_for_label(label)
    if not profile:
        return ""
    if profile.concept_type in {"metric"}:
        return "Use the metric definition from the confusion matrix or outcome counts and compute the ratio or score directly."
    if profile.concept_type in {"algorithm", "method"}:
        return "The mathematical form follows the update rule, objective function, or optimization criterion used by the method."
    if profile.concept_type in {"model"}:
        return "The mathematical form is the model equation that maps features to predictions or probabilities."
    if profile.concept_type in {"theory"}:
        return "The mathematical form is the set of probability or algebraic relationships that define the concept precisely."
    return ""


def canonical_why_it_matters_for_label(label: str) -> str:
    canonical = _canonical_name(label)
    if canonical == "Gradient Descent":
        return (
            "Gradient Descent is one of the fundamental optimization algorithms in machine learning. "
            "It is used to train linear models, logistic regression, neural networks, and many other models "
            "by iteratively minimizing a loss function. Understanding Gradient Descent is essential because "
            "nearly every modern machine learning algorithm relies on some form of numerical optimization."
        )
    if canonical == "Linear Regression":
        return (
            "Linear Regression is a baseline modeling tool in statistics and machine learning. "
            "It is valuable because it is simple to interpret, often works well as a first model, and gives a "
            "clear view of how features relate to an outcome."
        )
    if canonical == "Logistic Regression":
        return (
            "Logistic Regression is a standard classification baseline because it produces probabilities, "
            "remains interpretable, and transfers cleanly into business and technical settings where you need a "
            "decision rule and a score."
        )
    if canonical == "Probability":
        return (
            "Probability is the language of uncertainty. It underpins statistical inference, likelihood, Bayes' "
            "rule, calibration, and almost every model that reasons about risk or variability."
        )
    if canonical == "Maximum Likelihood Estimation":
        return (
            "Maximum Likelihood Estimation is the core fitting principle behind many statistical and machine "
            "learning models. It turns model fitting into a clear optimization problem."
        )
    if canonical == "Recall":
        return (
            "Recall matters whenever missing a positive case is costly. It is central in fraud detection, medical "
            "screening, and other imbalanced problems where false negatives hurt more than false alarms."
        )

    profile = profile_for_label(label)
    if not profile:
        return ""
    applications = _join_items(profile.applications)
    related = _join_items(profile.related_concepts)
    if applications:
        return (
            f"{canonical} matters because it shows up in {applications} and acts as a reusable building block in "
            f"{profile.domain or 'the target domain'}."
        )
    if related:
        return (
            f"{canonical} matters because it links to {related} and anchors {profile.topic or 'the surrounding topic'}."
        )
    return (
        f"{canonical} matters because it is a foundational {profile.concept_type or 'concept'} in "
        f"{profile.domain or 'the target domain'}."
    )


def canonical_how_it_works_for_label(label: str) -> str:
    canonical = _canonical_name(label)
    manual = {
        "Linear Regression": (
            "1. Represent the outcome as a linear combination of the input features.\n"
            "2. Fit the coefficients by minimizing squared residuals.\n"
            "3. Use the fitted line or plane to predict new outcomes and inspect the coefficients for interpretation."
        ),
        "Logistic Regression": (
            "1. Compute a linear score from the features.\n"
            "2. Pass that score through the sigmoid function to get a probability.\n"
            "3. Fit the coefficients by minimizing log-loss or maximizing likelihood, then apply a threshold if you need a class label."
        ),
        "Gradient Descent": (
            "1. Start from an initial parameter vector.\n"
            "2. Compute the gradient of the loss at the current point.\n"
            "3. Move opposite the gradient by a step size set by the learning rate.\n"
            "4. Repeat until the loss improves only a little or a stopping rule is met."
        ),
        "Probability": (
            "1. Define a sample space and the events or random variables of interest.\n"
            "2. Assign probabilities to events and update them with conditional probability when new information arrives.\n"
            "3. Use Bayes' rule, joint probabilities, or distributions to reason about uncertainty."
        ),
        "Maximum Likelihood Estimation": (
            "1. Choose a probabilistic model with unknown parameters.\n"
            "2. Write down the likelihood of the observed data under that model.\n"
            "3. Find the parameter values that maximize the likelihood, usually by maximizing the log-likelihood instead."
        ),
        "Recall": (
            "1. Build the confusion matrix for the classifier.\n"
            "2. Count the true positives and false negatives.\n"
            "3. Compute recall as the share of actual positives that were correctly identified."
        ),
    }
    if canonical in manual:
        return manual[canonical]
    profile = profile_for_label(label)
    if not profile:
        return ""
    if profile.concept_type in {"algorithm", "method", "workflow"}:
        return "\n".join(
            [
                f"1. Start from the inputs and the prerequisite ideas behind {canonical}.",
                f"2. Apply the core rule or update procedure associated with {canonical}.",
                f"3. Read the output in the context of {profile.topic or profile.domain or 'the course material'}.",
            ]
        )
    if profile.concept_type in {"model"}:
        return (
            f"1. Combine the inputs into a score or prediction rule.\n"
            f"2. Fit the parameters with the chosen objective.\n"
            f"3. Interpret the fitted coefficients or predicted values in {profile.topic or profile.domain or 'the topic'}."
        )
    if profile.concept_type in {"metric"}:
        return (
            f"1. Count the relevant outcomes.\n"
            f"2. Plug them into the metric formula.\n"
            f"3. Interpret the score as a trade-off or performance summary."
        )
    if profile.concept_type in {"theory"}:
        return (
            f"1. Define the objects and events precisely.\n"
            f"2. Apply the governing relationships or axioms.\n"
            f"3. Use the result to support inference, modeling, or decision making."
        )
    return ""


def canonical_key_components_for_label(label: str) -> list[str]:
    canonical = _canonical_name(label)
    manual = {
        "Linear Regression": [
            "Features",
            "Target variable",
            "Coefficients",
            "Residuals",
            "Error term",
            "Least-squares objective",
        ],
        "Logistic Regression": [
            "Linear predictor",
            "Sigmoid function",
            "Probability estimate",
            "Decision threshold",
            "Coefficients",
            "Log-loss objective",
        ],
        "Gradient Descent": [
            "Objective / loss function",
            "Parameters",
            "Gradient",
            "Learning rate",
            "Stopping criterion",
        ],
        "Probability": [
            "Sample space",
            "Event",
            "Random variable",
            "Conditional probability",
            "Independence",
            "Bayes' rule",
        ],
        "Maximum Likelihood Estimation": [
            "Model",
            "Parameters",
            "Likelihood",
            "Log-likelihood",
            "Optimizer",
        ],
        "Recall": [
            "True positives",
            "False negatives",
            "Confusion matrix",
            "Decision threshold",
            "Recall formula",
        ],
    }
    if canonical in manual:
        return manual[canonical]
    profile = profile_for_label(label)
    if not profile:
        return []
    if profile.concept_type in {"algorithm", "method", "workflow"}:
        return [
            "Inputs",
            "Core rule or update procedure",
            "Output or decision criterion",
            "Stopping or evaluation criterion",
        ]
    if profile.concept_type in {"model"}:
        return [
            "Features or inputs",
            "Parameters or coefficients",
            "Prediction rule",
            "Loss or fit criterion",
        ]
    if profile.concept_type in {"metric"}:
        return [
            "Relevant counts or summary statistics",
            "Metric formula",
            "Interpretation / trade-off",
        ]
    if profile.concept_type in {"theory"}:
        return [
            "Core definitions",
            "Assumptions",
            "Implications",
        ]
    return []


def canonical_common_variants_for_label(label: str) -> list[str]:
    canonical = _canonical_name(label)
    manual = {
        "Linear Regression": [
            "Simple Linear Regression",
            "Multiple Linear Regression",
            "Polynomial Regression",
            "Weighted Least Squares",
        ],
        "Logistic Regression": [
            "Binary Logistic Regression",
            "Multinomial Logistic Regression",
            "Regularized Logistic Regression",
        ],
        "Gradient Descent": [
            "Batch Gradient Descent",
            "Stochastic Gradient Descent",
            "Mini-batch Gradient Descent",
        ],
        "Probability": [
            "Discrete Probability",
            "Continuous Probability",
            "Conditional Probability",
            "Joint Probability",
        ],
        "Maximum Likelihood Estimation": [
            "Penalized Likelihood",
            "Conditional Likelihood",
            "Profile Likelihood",
        ],
        "Recall": [
            "Macro Recall",
            "Micro Recall",
            "Top-k Recall",
        ],
    }
    if canonical in manual:
        return manual[canonical]
    profile = profile_for_label(label)
    if not profile:
        return []
    variant_cues = (
        "batch",
        "stochastic",
        "mini-batch",
        "binary",
        "multinomial",
        "multiple",
        "simple",
        "polynomial",
        "weighted",
        "regularized",
        "penalized",
        "conditional",
        "profile",
        "macro",
        "micro",
        "top-k",
        "least squares",
    )
    variants: list[str] = []
    for synonym in profile.synonyms:
        candidate = canonical_candidate_label(synonym)
        if not candidate:
            continue
        if normalize_concept_key(candidate) == normalize_concept_key(canonical):
            continue
        if any(cue in candidate.lower() for cue in variant_cues):
            variants.append(candidate)
    return _unique_text_list(variants)


def canonical_common_mistakes_for_label(label: str) -> list[str]:
    canonical = _canonical_name(label)
    manual = {
        "Linear Regression": [
            "Treating correlation as causation.",
            "Ignoring multicollinearity and influential outliers.",
            "Using the model on clearly nonlinear data without checking fit.",
        ],
        "Logistic Regression": [
            "Thinking logistic regression is a regression method instead of a classifier.",
            "Ignoring class imbalance or the decision threshold.",
            "Reading raw coefficients without considering the sigmoid link.",
        ],
        "Gradient Descent": [
            "Using a learning rate that is too large or too small.",
            "Forgetting that feature scaling often affects convergence.",
            "Assuming it always reaches the global optimum.",
        ],
        "Probability": [
            "Confusing independence with mutual exclusivity.",
            "Treating conditional probability as if it were symmetric.",
            "Mixing up probability, likelihood, and frequency.",
        ],
        "Maximum Likelihood Estimation": [
            "Confusing likelihood with the probability of the parameters.",
            "Forgetting to take the log before optimizing numerically.",
            "Ignoring whether the model assumptions are actually reasonable.",
        ],
        "Recall": [
            "Assuming high accuracy means high recall.",
            "Optimizing recall without checking precision.",
            "Ignoring the decision threshold that drives the trade-off.",
        ],
    }
    if canonical in manual:
        return manual[canonical]
    profile = profile_for_label(label)
    if not profile:
        return []
    return [
        f"Confusing {canonical} with a nearby but different concept.",
        f"Using {canonical} without checking its assumptions or prerequisites.",
        f"Memorizing the name of {canonical} without being able to explain its role.",
    ]


def canonical_interview_questions_for_label(label: str) -> list[str]:
    canonical = _canonical_name(label)
    manual = {
        "Linear Regression": [
            "What problem does linear regression solve?",
            "Why do we minimize squared residuals?",
            "What assumptions must hold for the coefficients to be easy to interpret?",
            "When would you choose ridge or lasso instead of plain linear regression?",
        ],
        "Logistic Regression": [
            "Why does logistic regression use the sigmoid function?",
            "How do you turn probabilities into class labels?",
            "When is logistic regression a strong baseline?",
            "How does regularization change the model?",
        ],
        "Gradient Descent": [
            "Why is the learning rate so important?",
            "How do batch, stochastic, and mini-batch gradient descent differ?",
            "Why does feature scaling often help convergence?",
            "Why can gradient descent be slow or unstable?",
        ],
        "Probability": [
            "Why is probability the foundation for statistical inference?",
            "What is the difference between joint, marginal, and conditional probability?",
            "How does Bayes' rule update a belief with new evidence?",
            "What is the difference between independence and mutual exclusivity?",
        ],
        "Maximum Likelihood Estimation": [
            "What does it mean to maximize a likelihood?",
            "Why do we usually work with the log-likelihood?",
            "How is MLE connected to many standard statistical estimators?",
            "How does MLE differ from MAP estimation?",
        ],
        "Recall": [
            "Why does recall matter in imbalanced or high-cost-miss problems?",
            "How is recall computed from the confusion matrix?",
            "How does recall trade off against precision?",
            "Why can accuracy be misleading when recall is low?",
        ],
    }
    if canonical in manual:
        return manual[canonical]
    profile = profile_for_label(label)
    if not profile:
        return []
    related = _join_items(profile.related_concepts[:3])
    questions = [
        f"What problem does {canonical} solve?",
        f"How does {canonical} work at a high level?",
        f"When would you use {canonical}, and when would you avoid it?",
        f"What are the main assumptions or limitations of {canonical}?",
    ]
    if related:
        questions.append(f"How does {canonical} compare with {related}?")
    return questions


def canonical_connections_for_label(label: str) -> list[str]:
    canonical = _canonical_name(label)
    manual = {
        "Linear Regression": [
            "Depends on: features, residuals, least squares, matrix algebra",
            "Used in: prediction, forecasting, business analytics",
            "Related: logistic regression, ridge regression, lasso regression, regularization",
        ],
        "Logistic Regression": [
            "Depends on: probability, linear predictor, maximum likelihood estimation",
            "Used in: classification, risk scoring, customer churn",
            "Related: classification accuracy, precision, recall, regularization",
        ],
        "Gradient Descent": [
            "Depends on: objective function, gradient, learning rate",
            "Used to train: linear regression, logistic regression, neural networks",
            "Related: loss function, regularization, Newton's method, Adam optimizer",
        ],
        "Probability": [
            "Depends on: sample space, events, random variables",
            "Used in: hypothesis testing, maximum likelihood estimation, logistic regression",
            "Related: distributions, expectation, Bayes' rule",
        ],
        "Maximum Likelihood Estimation": [
            "Depends on: probabilistic model, likelihood, data",
            "Used in: parameter estimation, logistic regression, probabilistic modeling",
            "Related: cross-entropy, Bayesian estimation, probability",
        ],
        "Recall": [
            "Depends on: confusion matrix, true positives, false negatives",
            "Used in: medical screening, fraud detection, high-cost-miss settings",
            "Related: precision, F1 score, classification accuracy, threshold selection",
        ],
    }
    if canonical in manual:
        return manual[canonical]
    profile = profile_for_label(label)
    if not profile:
        return []
    lines: list[str] = []
    if profile.prerequisites:
        lines.append(f"Depends on: {_join_items(profile.prerequisites)}")
    if profile.applications:
        lines.append(f"Used in: {_join_items(profile.applications)}")
    if profile.related_concepts:
        lines.append(f"Related: {_join_items(profile.related_concepts)}")
    if profile.broader_topics:
        lines.append(f"Broader topic: {_join_items(profile.broader_topics)}")
    return lines


def canonical_interview_notes_for_label(label: str) -> list[str]:
    return list(_CANONICAL_INTERVIEW_NOTES.get(_canonical_name(label), []))


def canonical_further_reading_for_label(label: str) -> list[str]:
    return list(_CANONICAL_FURTHER_READING.get(_canonical_name(label), []))


CONCEPT_CONFIDENCE_THRESHOLD = 0.64
DEFINITION_QUALITY_THRESHOLD = 0.58
EVIDENCE_STRENGTH_THRESHOLD = 0.42
INTERVIEW_RELEVANCE_THRESHOLD = 0.55

_GENERIC_CONCEPT_KEYS = {
    normalize_concept_key(value)
    for value in (
        "accuracy",
        "prediction",
        "model",
        "training",
        "feature",
        "data",
        "classification",
        "regression",
    )
}

_STRUCTURAL_NOISE = {
    "agenda",
    "introduction",
    "summary",
    "outline",
    "questions",
    "question",
    "lecture",
    "week",
    "chapter",
    "page",
    "slide",
    "slides",
    "example",
    "examples",
    "dataset",
    "dataset overview",
    "administrative",
    "admin",
}

_FIELD_CUE_MAP: dict[str, tuple[str, ...]] = {
    "definition": (" is ", " are ", " refers to ", " means ", " defined as ", " model that ", " method that ", " approach that "),
    "math": ("=", "minimize", "maximize", "argmin", "argmax", "beta", "theta", "sigma", "variance", "log", "exp", "sum", "∑", "sqrt"),
    "application": ("used for", "applied to", "predict", "classify", "forecast", "segment", "estimate", "diagnose", "detect"),
    "assumption": ("assumption", "assumes", "requires", "under the assumption", "conditions"),
    "limitation": ("limitation", "drawback", "fails", "cannot", "not suitable", "sensitive"),
}


def _alias_hit(alias: str, text: str) -> bool:
    alias = normalize_spaces(alias).lower()
    text = normalize_spaces(text).lower()
    if not alias or not text:
        return False
    if len(alias) <= 3 or len(alias.split()) == 1:
        pattern = rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])"
        return re.search(pattern, text) is not None
    return alias in text


def _collect_evidence_lines(alias: str, heading: str, lines: list[str], tables: list[list[list[str]]]) -> list[str]:
    evidence: list[str] = []
    for source_line in [heading, *lines]:
        if source_line and _alias_hit(alias, source_line):
            cleaned = normalize_spaces(source_line)
            if cleaned not in evidence:
                evidence.append(cleaned)
    for table in tables:
        for row in table:
            for cell in row:
                cell_text = normalize_spaces(str(cell or ""))
                if cell_text and _alias_hit(alias, cell_text) and cell_text not in evidence:
                    evidence.append(cell_text)
    return evidence


def _strong_signal_count(lines: list[str]) -> int:
    count = 0
    for line in lines:
        lower = line.lower()
        if any(cue in lower for cues in _FIELD_CUE_MAP.values() for cue in cues):
            count += 1
    return count


def _first_signal_line(lines: list[str], alias: str, cues: tuple[str, ...]) -> str:
    for line in lines:
        lower = line.lower()
        if _alias_hit(alias, lower) and any(cue in lower for cue in cues):
            return normalize_spaces(line)
    return ""


def _is_structural_noise(label: str) -> bool:
    lowered = normalize_spaces(label).lower()
    if not lowered:
        return True
    if lowered in _STRUCTURAL_NOISE:
        return True
    if re.fullmatch(r"(page|slide|week)\s*\d+", lowered):
        return True
    if re.fullmatch(r"\d+(\.\d+)?", lowered):
        return True
    if len(lowered.split()) == 1 and len(lowered) <= 2 and lowered not in {"pca", "svm", "mle", "auc"}:
        return True
    if not re.search(r"[a-zA-Z]", lowered):
        return True
    return False


def _is_generic_label(label: str) -> bool:
    return normalize_concept_key(label) in _GENERIC_CONCEPT_KEYS


def _definition_quality_score(
    heading_hit: bool,
    body_hits: int,
    definition_line: str,
    math_line: str,
    application_line: str,
    evidence_lines: list[str],
    profile: ConceptProfile,
) -> float:
    score = 0.0
    if definition_line:
        score += 0.48
        if len(definition_line.split()) >= 8:
            score += 0.08
        if any(cue in definition_line.lower() for cue in ("model that", "method that", "approach that", "estimates", "measures", "describes", "predicts")):
            score += 0.10
    if body_hits >= 2:
        score += 0.10
    if heading_hit and body_hits >= 1:
        score += 0.06
    if math_line:
        score += 0.06
    if application_line:
        score += 0.06
    if len(evidence_lines) >= 2:
        score += 0.08
    if profile.importance_score >= 5:
        score += 0.04
    if _is_generic_label(profile.concept_name):
        score -= 0.14
    return max(0.0, min(0.98, score))


def _evidence_strength(
    heading_hit: bool,
    body_hits: int,
    table_hits: int,
    definition_line: str,
    math_line: str,
    application_line: str,
    profile: ConceptProfile,
) -> float:
    score = 0.18
    score += 0.16 if heading_hit else 0.0
    score += 0.12 * min(body_hits, 4)
    score += 0.04 * min(table_hits, 3)
    score += 0.10 if definition_line else 0.0
    score += 0.08 if math_line else 0.0
    score += 0.08 if application_line else 0.0
    score += 0.04 if profile.importance_score >= 5 else 0.0
    if _is_generic_label(profile.concept_name):
        score -= 0.12
    return max(0.0, min(0.98, score))


def _interview_relevance(
    profile: ConceptProfile,
    body_hits: int,
    definition_line: str,
    math_line: str,
    application_line: str,
) -> float:
    score = 0.42 + 0.10 * profile.importance_score
    if body_hits >= 2:
        score += 0.06
    if definition_line:
        score += 0.06
    if math_line:
        score += 0.06
    if application_line:
        score += 0.06
    if profile.concept_type in {"algorithm", "model", "method", "metric", "workflow"}:
        score += 0.04
    if _is_generic_label(profile.concept_name):
        score -= 0.10
    return max(0.0, min(0.98, score))


def candidate_concepts_from_page(
    heading: str,
    lines: list[str],
    tables: list[list[list[str]]],
    course_name: str = "",
) -> list[ConceptCandidate]:
    page_text = normalize_spaces(" ".join([heading, *lines, *(normalize_spaces(str(cell or "")) for table in tables for row in table for cell in row)]))
    candidates: list[ConceptCandidate] = []
    seen: set[str] = set()

    for profile in CONCEPT_PROFILES:
        canonical = profile.concept_name
        aliases = (canonical, *profile.synonyms)
        if not any(_alias_hit(alias, page_text) for alias in aliases):
            continue

        evidence_lines = _collect_evidence_lines(canonical, heading, lines, tables)
        if not evidence_lines:
            continue

        heading_hit = _alias_hit(canonical, heading) or any(_alias_hit(alias, heading) for alias in aliases)
        body_hits = sum(1 for line in lines if any(_alias_hit(alias, line) for alias in aliases))
        table_hits = sum(
            1
            for table in tables
            for row in table
            if any(_alias_hit(alias, " ".join(str(cell or "") for cell in row)) for alias in aliases)
        )
        evidence_text = " ".join(evidence_lines[:3])
        definition_line = _first_signal_line(lines, canonical, _FIELD_CUE_MAP["definition"])
        math_line = _first_signal_line(lines, canonical, _FIELD_CUE_MAP["math"])
        application_line = _first_signal_line(lines, canonical, _FIELD_CUE_MAP["application"])
        structural_penalty = 0.0
        if _is_structural_noise(heading) and body_hits == 0:
            structural_penalty = 0.35
        if heading and heading.strip().lower() in _STRUCTURAL_NOISE and body_hits == 0:
            structural_penalty = max(structural_penalty, 0.4)
        if any(token in heading.lower() for token in ("agenda", "summary", "week", "questions", "lecture", "slide")):
            if body_hits == 0:
                structural_penalty = max(structural_penalty, 0.25)
            elif not (definition_line or math_line or application_line):
                structural_penalty = max(structural_penalty, 0.15)

        evidence_strength = _evidence_strength(
            heading_hit=heading_hit,
            body_hits=body_hits,
            table_hits=table_hits,
            definition_line=definition_line,
            math_line=math_line,
            application_line=application_line,
            profile=profile,
        )
        definition_quality = _definition_quality_score(
            heading_hit=heading_hit,
            body_hits=body_hits,
            definition_line=definition_line,
            math_line=math_line,
            application_line=application_line,
            evidence_lines=evidence_lines,
            profile=profile,
        )
        interview_relevance = _interview_relevance(
            profile=profile,
            body_hits=body_hits,
            definition_line=definition_line,
            math_line=math_line,
            application_line=application_line,
        )
        confidence = (
            0.42 * evidence_strength
            + 0.34 * definition_quality
            + 0.24 * interview_relevance
            - structural_penalty
        )
        if _is_generic_label(canonical):
            confidence -= 0.10
        confidence = max(0.0, min(0.98, confidence))

        reason_parts = []
        if heading_hit:
            reason_parts.append("appears in heading")
        if body_hits:
            reason_parts.append(f"repeated in body {body_hits}x")
        if table_hits:
            reason_parts.append(f"appears in table {table_hits}x")
        if definition_line:
            reason_parts.append("has definition cue")
        if math_line:
            reason_parts.append("has mathematical cue")
        if application_line:
            reason_parts.append("has application cue")
        if definition_quality >= DEFINITION_QUALITY_THRESHOLD:
            reason_parts.append("definition is specific enough")
        if evidence_strength >= EVIDENCE_STRENGTH_THRESHOLD:
            reason_parts.append("strong evidence")
        if structural_penalty:
            reason_parts.append("penalized for slide-style noise")
        if _is_generic_label(canonical):
            reason_parts.append("generic term requires strong context")
        reason = "; ".join(reason_parts) if reason_parts else "high-value concept match"

        key = normalize_concept_key(canonical)
        if key in seen:
            continue
        seen.add(key)
        candidates.append(
            ConceptCandidate(
                concept_name=canonical,
                confidence_score=round(confidence, 3),
                concept_type=profile.concept_type,
                evidence_strength=round(evidence_strength, 3),
                definition_quality_score=round(definition_quality, 3),
                interview_relevance=round(interview_relevance, 3),
                reason_for_inclusion=reason,
                domain=profile.domain,
                topic=profile.topic,
                importance_score=profile.importance_score,
                evidence=evidence_text,
                aliases=[normalize_spaces(alias) for alias in aliases if normalize_spaces(alias)],
            )
        )

    candidates.sort(key=lambda item: (-item.confidence_score, -item.importance_score, item.concept_name.lower()))
    return candidates
