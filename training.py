import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    roc_curve,
    precision_recall_curve,
    roc_auc_score,
    average_precision_score,
    accuracy_score,
    f1_score,
    brier_score_loss,
    confusion_matrix
)
from sklearn.calibration import calibration_curve
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

# 1. Load data
df = pd.read_csv('/Users/david/crohn_ksef_app/gingivitis.cleaned.csv')
X = df.drop(columns=['Patient ID', 'Label'])
y = df['Label']

# 2. Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

# 3. Pipeline: impute + model
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('model', RandomForestClassifier(n_estimators=100, random_state=42))
])
pipeline.fit(X_train, y_train)
y_proba = pipeline.predict_proba(X_test)[:, 1]
y_pred = pipeline.predict(X_test)

# 4. Plots
# ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_proba)
plt.figure()
plt.plot(fpr, tpr)
plt.plot([0, 1], [0, 1], '--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.show()

# Precision-Recall Curve
precision_vals, recall_vals, _ = precision_recall_curve(y_test, y_proba)
plt.figure()
plt.plot(recall_vals, precision_vals)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.show()

# Calibration Curve
prob_true, prob_pred = calibration_curve(y_test, y_proba, n_bins=10)
plt.figure()
plt.plot(prob_pred, prob_true, 'o-')
plt.plot([0, 1], [0, 1], '--')
plt.xlabel('Mean Predicted Probability')
plt.ylabel('Observed Proportion')
plt.title('Calibration Curve')
plt.show()

# Scalar Metrics Bar Chart
auc_score = roc_auc_score(y_test, y_proba)
pr_auc = average_precision_score(y_test, y_proba)
acc = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
brier = brier_score_loss(y_test, y_proba)
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
sensitivity = tp / (tp + fn)
specificity = tn / (tn + fp)
precision = tp / (tp + fp)
npv = tn / (tn + fn)

metrics = {
    'AUC-ROC': auc_score,
    'AUC-PR': pr_auc,
    'Accuracy': acc,
    'F1-Score': f1,
    'Brier Score': brier,
    'Sensitivity': sensitivity,
    'Specificity': specificity,
    'Precision': precision,
    'NPV': npv
}

plt.figure(figsize=(8, 4))
plt.barh(list(metrics.keys()), list(metrics.values()))
plt.xlabel('Value')
plt.title('Key Performance Metrics')
plt.tight_layout()
plt.show()
