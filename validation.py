# validation.py

import sys
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB

def load_data(path):
    """
    Load the gingivitis dataset CSV and split into features X and label y.
    """
    df = pd.read_csv(path, sep=',')
    X = df.drop(columns=['Patient ID', 'Label'])
    y = df['Label']
    return X, y

def run_cv(models, X, y, cv=10):
    """
    Perform cv-fold stratified cross-validation with median imputation
    and print accuracy for each model.
    """
    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
    print(f"Running stratified {cv}-fold CV on {len(y)} samples…\n")

    for name, model in models.items():
        # Build a pipeline: median impute then fit model
        pipe = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('clf',     model)
        ])
        # Evaluate
        scores = cross_val_score(
            pipe, X, y,
            cv=skf,
            scoring='accuracy',
            error_score='raise'
        )
        mean, std = scores.mean(), scores.std()
        print(f"{name:15} Accuracy: {mean:.3f} ± {std:.3f}")

if __name__ == "__main__":
    # 1. Load data
    path = '/Users/david/crohn_ksef_app/gingivitis.cleaned.csv'
    try:
        X, y = load_data(path)
    except FileNotFoundError as e:
        print(f"Error: could not read data file: {e}")
        sys.exit(1)

    # 2. Define models
    models = {
        "LogisticReg" : LogisticRegression(solver='liblinear', random_state=42),
        "DecisionTree": DecisionTreeClassifier(random_state=42),
        "KNN(k=5)"    : KNeighborsClassifier(n_neighbors=5),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
        "NaiveBayes"  : GaussianNB(),
    }

    # 3. Run 10-fold stratified CV with imputation
    run_cv(models, X, y, cv=10)
