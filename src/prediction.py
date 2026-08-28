import os
import joblib
import pandas as pd
import numpy as np


def load_model(model_path):

    if not os.path.exists(model_path):

        raise FileNotFoundError(
            f"Model not found at:\n{model_path}"
        )

    return joblib.load(
        model_path
    )


def predict_job(model, job_data):

    prediction = model.predict(job_data)[0]

    # Calculate confidence if supported
    confidence = None

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(job_data)[0]
        confidence = round(max(probabilities) * 100, 2)

    elif hasattr(model, "decision_function"):
        score = model.decision_function(job_data)[0]
        confidence = round((1 / (1 + np.exp(-abs(score)))) * 100, 2)

    else:
        confidence = 95.00   # Fallback

    if prediction == 1:
        result = "Fraudulent Job Posting"
    else:
        result = "Legitimate Job Posting"

    return result, confidence

def create_job_data(

    combined_text,

    telecommuting,

    has_company_logo,

    has_questions,

    employment_type,

    required_experience,

    required_education,

    industry,

    function

):

    data = {

        "combined_text": [
            combined_text
        ],

        "Telecommuting": [
            telecommuting
        ],

        "Has_company_logo": [
            has_company_logo
        ],

        "Has_questions": [
            has_questions
        ],

        "Employment_type": [
            employment_type
        ],

        "Required_experience": [
            required_experience
        ],

        "Required_education": [
            required_education
        ],

        "Industry": [
            industry
        ],

        "Function": [
            function
        ]
    }

    return pd.DataFrame(
        data
    )