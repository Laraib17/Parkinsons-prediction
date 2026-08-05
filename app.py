from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from src.model_pipeline import load_dataset, predict_record, train_pipeline

ROOT_DIR = Path(__file__).resolve().parent
DATA_PATH = ROOT_DIR / 'data' / 'raw_data' / 'parkinsons.csv'


@st.cache_data
def get_model_bundle():
    return train_pipeline(DATA_PATH)


@st.cache_data
def get_dataset():
    return load_dataset(DATA_PATH)


def render_css():
    st.markdown(
        """
        <style>
            :root {
                --bg: #0f172a;
                --panel: #111827;
                --card: #1f2937;
                --primary: #4f46e5;
                --accent: #22c55e;
                --danger: #ef4444;
                --text: #e5e7eb;
                --muted: #94a3b8;
            }
            .stApp {
                background: linear-gradient(135deg, #0f172a 0%, #111827 35%, #1e293b 100%);
                color: var(--text);
            }
            .block-container {
                padding-top: 2rem;
                padding-bottom: 3rem;
            }
            .metric-card {
                background: rgba(31, 41, 55, 0.9);
                border: 1px solid rgba(148, 163, 184, 0.2);
                border-radius: 16px;
                padding: 1rem 1.2rem;
                box-shadow: 0 10px 30px rgba(15, 23, 42, 0.25);
            }
            .section-header {
                font-size: 1.2rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
            }
            h1 {
                color: #f8fafc;
                letter-spacing: -0.04em;
            }
            h2, h3 {
                color: #e2e8f0;
            }
            .stTabs [role="tablist"] {
                gap: 0.75rem;
            }
            .stTabs [role="tab"] {
                background: rgba(15, 23, 42, 0.6);
                border-radius: 0.8rem;
                padding: 0.6rem 1rem;
            }
            div[data-testid="stFormSubmitButton"] > button {
                width: 100%;
                border-radius: 0.8rem;
                font-weight: 700;
                background: linear-gradient(90deg, #4f46e5, #7c3aed);
                border: none;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_metrics(bundle):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Dataset Size', f"{bundle['sample_count']}")
    col2.metric('Healthy Cases', f"{bundle['healthy_count']}")
    col3.metric('Parkinson Cases', f"{bundle['parkinson_count']}")
    col4.metric('Model Accuracy', f"{bundle['test_accuracy'] * 100:.2f}%")


def build_prediction_form(bundle):
    feature_columns = bundle['feature_columns']
    dataset = bundle['dataset']
    defaults = {}

    for column in feature_columns:
        defaults[column] = float(dataset[column].median())

    inputs = {}
    columns = st.columns(3)
    for index, column in enumerate(feature_columns):
        value = defaults[column]
        feature_min = float(dataset[column].min())
        feature_max = float(dataset[column].max())
        with columns[index % 3]:
            inputs[column] = st.number_input(
                label=column,
                value=value,
                min_value=feature_min,
                max_value=feature_max,
                step=0.0001,
                format='%.6f',
            )
    return inputs


def show_result(results):
    status = results['status']
    probability = results['risk_probability'] * 100
    if results['prediction'] == 1:
        st.error(f"{results['label']} — {probability:.2f}% risk probability")
    else:
        st.success(f"{results['label']} — {probability:.2f}% risk probability")

    col1, col2 = st.columns(2)
    with col1:
        st.metric('Parkinson Probability', f'{probability:.2f}%')
    with col2:
        st.metric('Healthy Probability', f'{results["healthy_probability"] * 100:.2f}%')


def main():
    render_css()
    st.set_page_config(page_title='Parkinsons Prediction App', page_icon='🧠', layout='wide')

    st.title('Parkinsons Disease Prediction Dashboard')
    st.caption('Professional, single-page clinical risk assessment interface built with Streamlit.')

    model_bundle = get_model_bundle()
    dataset = get_dataset()

    render_metrics(model_bundle)

    tabs = st.tabs(['Prediction', 'Dataset Overview', 'Model Details'])

    with tabs[0]:
        st.markdown('<div class="section-header">Patient Assessment</div>', unsafe_allow_html=True)

        with st.form('prediction_form'):
            feature_inputs = build_prediction_form(model_bundle)
            submitted = st.form_submit_button('Predict Patient Status')

        if submitted:
            ordered_values = [float(feature_inputs[column]) for column in model_bundle['feature_columns']]
            prediction_result = predict_record(model_bundle, ordered_values)
            show_result(prediction_result)

    with tabs[1]:
        st.markdown('<div class="section-header">Dataset Snapshot</div>', unsafe_allow_html=True)
        st.dataframe(dataset.head(10), use_container_width=True)
        st.bar_chart(dataset['status'].value_counts().rename(index={0: 'Healthy', 1: 'Parkinson'}))

    with tabs[2]:
        st.markdown('<div class="section-header">Model Overview</div>', unsafe_allow_html=True)
        st.write(
            'This dashboard uses a StandardScaler + Linear SVM classifier trained on the Parkinsons disease dataset. '
            'The model was trained and evaluated using a stratified train-test split to preserve class balance.'
        )
        st.code(
            "model = SVC(kernel='linear', probability=True)\n"
            "scaler = StandardScaler()\n"
            "X_train_scaled = scaler.fit_transform(X_train)\n"
            "model.fit(X_train_scaled, y_train)",
            language='python',
        )
        col1, col2 = st.columns(2)
        with col1:
            st.metric('Training Accuracy', f"{model_bundle['train_accuracy'] * 100:.2f}%")
        with col2:
            st.metric('Test Accuracy', f"{model_bundle['test_accuracy'] * 100:.2f}%")


if __name__ == '__main__':
    main()
