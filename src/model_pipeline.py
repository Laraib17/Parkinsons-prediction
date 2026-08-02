from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


def load_dataset(path: str | Path) -> pd.DataFrame:
    """Load the Parkinson's dataset."""
    data_path = Path(path)
    dataset = pd.read_csv(data_path)
    if 'status' not in dataset.columns:
        raise ValueError("Dataset must contain a 'status' column.")
    return dataset


def train_pipeline(data_path: str | Path, test_size: float = 0.2, random_state: int = 42) -> Dict[str, Any]:
    """Train the support vector classifier and return the pipeline bundle."""
    dataset = load_dataset(data_path)
    feature_columns = [col for col in dataset.columns if col not in ['name', 'status']]
    X = dataset[feature_columns]
    y = dataset['status']

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = SVC(kernel='linear', probability=True, random_state=random_state)
    model.fit(X_train_scaled, y_train)

    train_predictions = model.predict(X_train_scaled)
    test_predictions = model.predict(X_test_scaled)

    train_accuracy = accuracy_score(y_train, train_predictions)
    test_accuracy = accuracy_score(y_test, test_predictions)

    return {
        'dataset': dataset,
        'feature_columns': feature_columns,
        'scaler': scaler,
        'model': model,
        'train_accuracy': train_accuracy,
        'test_accuracy': test_accuracy,
        'positive_rate': float(y.mean() * 100),
        'sample_count': int(len(dataset)),
        'healthy_count': int((y == 0).sum()),
        'parkinson_count': int((y == 1).sum()),
    }


def predict_record(model_bundle: Dict[str, Any], record_values: List[float]) -> Dict[str, Any]:
    """Predict one record based on the trained pipeline."""
    feature_columns = model_bundle['feature_columns']
    if len(record_values) != len(feature_columns):
        raise ValueError(f"Expected {len(feature_columns)} feature values, received {len(record_values)}.")

    values = np.asarray(record_values, dtype=float).reshape(1, -1)
    scaled_values = model_bundle['scaler'].transform(values)
    prediction = int(model_bundle['model'].predict(scaled_values)[0])
    probabilities = model_bundle['model'].predict_proba(scaled_values)[0]
    risk_probability = float(probabilities[1]) if len(probabilities) > 1 else float(probabilities[0])

    return {
        'prediction': prediction,
        'risk_probability': risk_probability,
        'healthy_probability': float(probabilities[0]) if len(probabilities) > 1 else 1.0 - risk_probability,
        'label': 'Parkinson’s Disease Detected' if prediction == 1 else 'Healthy / No Parkinson’s Signs',
        'status': 'At Risk' if prediction == 1 else 'Low Risk',
    }
