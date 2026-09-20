"""
Module 5: Model Trainer
Trains Logistic Regression + Random Forest for each species,
evaluates with 5-fold cross-validation AUC-ROC, saves the best model.
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler

FEATURES = ["sst", "sst_sq", "month_sin", "month_cos", "lat_abs"]

data = pd.read_csv("data/processed/training_data.csv")

absences = data[data["species"] == "pseudo_absence"]
species_list = [s for s in data["species"].unique() if s != "pseudo_absence"]

os.makedirs("models", exist_ok=True)

results = []

for species in species_list:
    presences = data[data["species"] == species]

    # Build this species' training set: its presences + the shared pseudo-absences
    species_data = pd.concat([presences, absences], ignore_index=True)

    X = species_data[FEATURES]
    y = species_data["presence"]

    # Logistic Regression needs scaled features; Random Forest doesn't, but scaling doesn't hurt it
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    log_reg = LogisticRegression(max_iter=1000)
    rf = RandomForestClassifier(n_estimators=200, random_state=42)

    log_reg_auc = cross_val_score(log_reg, X_scaled, y, cv=5, scoring="roc_auc").mean()
    rf_auc = cross_val_score(rf, X_scaled, y, cv=5, scoring="roc_auc").mean()

    # Pick and refit the better model on the full data
    if rf_auc >= log_reg_auc:
        best_model, best_name, best_auc = rf, "RandomForest", rf_auc
    else:
        best_model, best_name, best_auc = log_reg, "LogisticRegression", log_reg_auc

    best_model.fit(X_scaled, y)

    joblib.dump(best_model, f"models/{species}_model.pkl")
    joblib.dump(scaler, f"models/{species}_scaler.pkl")

    results.append({
        "species": species,
        "n_presences": len(presences),
        "logreg_auc": round(log_reg_auc, 3),
        "rf_auc": round(rf_auc, 3),
        "best_model": best_name,
        "best_auc": round(best_auc, 3),
    })

    print(f"{species}: LogReg AUC={log_reg_auc:.3f}, RF AUC={rf_auc:.3f} -> using {best_name}")

results_df = pd.DataFrame(results)
results_df.to_csv("models/model_comparison.csv", index=False)

print("\n--- Summary ---")
print(results_df)