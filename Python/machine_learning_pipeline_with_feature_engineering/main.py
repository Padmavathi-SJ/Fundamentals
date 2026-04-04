# =====================
# IMPORT LIBRARIES
# =====================

import pandas as pd # for data handling (tables)
import numpy as np # for numerical oeprations
import random # to generate sample dataset

from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from xgboost import XGBClassifier  # advanced boosting model

import joblib
import os

# ============================
# STEP 0: GENERATE SAMPLE DATA (if not exists)
# =============================

if not os.path.exists("data.csv"): # check if dataset already exists
    data = [] # empty list to store rows

    for i in range(200): # generate 200 rows
        data.append({
            "billing_amount": random.randint(100, 1000), # random billing value
            "tenure_months": random.randint(1, 60), # customer duration
            "days_since_last_login": random.randint(1, 30), # lastlogin gap
            "contract_type": random.choice(["monthly", "yearly"]), # category
            "churn": random.choice([0,1]) # target variable
        })

        df = pd.DataFrame(data) # convert list to DataFrame
        df.to_csv("data.csv", index=False) # save dataset


# ===========================
# STEP 1: LOAD DATA
# ===========================

print("=== Data Ingestion ===")

df = pd.read_csv("data.csv")  # load dataset from csv file

print(f"Loaded {df.shape[0]} records ({df.shape[1]} features)")


# =========================
# STEP 2: HANDLE MISSING VALUES
# =========================

for col in df.columns: # loop through columns
    if df[col].isnull().sum() > 0: # check missing values
        percent = df[col].isnull().mean() * 100 # calculate %
        print(f"Missing values filled: {col} ({round(percent, 2)}%)")


# =============================
# STEP 3: FEATURE ENGINEERING
# =============================

# Example: create new feature (avg spend)
df["avg_monthly_spend"] = df["billing_amount"] / (df["tenure_months"] + 1)

# create tenure category (binning)
df["tenure_bin"] = pd.cut(
    df["tenure_months"],
    bins=[0,12,24,60],
    labels=["0-1yr", "1-2yr", "2+yr"]
)

print("Feature Engineering Done")


# =============================
# STEP 4: DEFINE FEATURES & TARGET
# ============================

X = df.drop("churn", axis=1) # input features
y = df["churn"] # output (target)


# ===============================
# STEP 5: SPLIT DATA
# ===============================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42 # 80% train, 20% test
)


# ===============================
# STEP 6: PREPROCESSING
# ===============================

# identify numeric columns
num_cols = X.select_dtypes(include=["int64", "float64"]).columns

# identify categorical columns
cat_cols = X.select_dtypes(include=["object", "category", "string"]).columns

# numeric pipeline (fill missing + scale)
num_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")), # replace missing with mean
    ("scaler", StandardScaler())
])

# categorical pipeline (fill missing + encode)
cat_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")), # replace missing
    ("encoder", OneHotEncoder(handle_unknown="ignore")) # convert text -> numbers
])

# combine both pipelines
preprocessor = ColumnTransformer([
    ("num", num_pipeline, num_cols), # numeric processing
    ("cat", cat_pipeline, cat_cols) # categorical processing
])


# ==========================
# STEP 7: MODEL DEFINITIONS
# ==========================

models = {
    "Logistic Registration": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(),
    "SVM": SVC()
}


# ==========================
# STEP 8: MODEL COMPARISION
# ==========================

print("\n==== Model Comparision ===")
print(f"{'Model':25} {'F1 Score':10}")

for name, model in models.items():

    # combine preprocessing + model
    pipeline = Pipeline([
        ("preprocess", preprocessor),
        ("model", model)
    ])

    # perform cross-validation
    scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring="f1")

    f1 = scores.mean() # average F1 score

    print(f"{name:25} {round(f1,3)}")



# ==========================
# STEP 9: XGBOOST WITH TUNING
# ==========================

print("\nTraining XGBoost....")

xgb_pipeline = Pipeline([
    ("preprocess", preprocessor),
    ("model", XGBClassifier(eval_metric="logloss"))
])

# hyperparameter tuning
param_grid = {
    "model__max_depth": [4, 6],
    "model__learning_rate": [0.05, 0.1],
    "model__n_estimators": [100, 200]
}

grid = GridSearchCV(xgb_pipeline, param_grid, cv=3, scoring="f1")

grid.fit(X_train, y_train) # train model

best_model = grid.best_estimator_ # best model

print("Best Parameters: ", grid.best_params_)


# =======================
# STEP 10: FINAL EVALUATION
# =======================

y_pred = best_model.predict(X_test)  # predict test data

print("\n=== Final Evaluation ===")
print("Accuracy:", round(accuracy_score(y_test, y_pred), 3))
print("Precision:", round(precision_score(y_test, y_pred), 3))
print("Recall:", round(recall_score(y_test, y_pred), 3))
print("F1:", round(f1_score(y_test, y_pred), 3))

# =========================
# STEP 11: FEATURE IMPORTANCE
# =========================

model = best_model.named_steps["model"]  # extract model

if hasattr(model, "feature_importances_"):  # check if supported
    print("\nTop Feature Importances:")
    importances = model.feature_importances_

    for i, val in enumerate(importances[:5]):  # show top 5
        print(f"{i+1}. Feature {i} — {round(val,3)}")


# =========================
# STEP 12: SAVE MODEL
# =========================

os.makedirs("models", exist_ok=True)  # create folder if not exists

joblib.dump(best_model, "models/churn_model.pkl")  # save model

print("\nModel saved to models/churn_model.pkl")