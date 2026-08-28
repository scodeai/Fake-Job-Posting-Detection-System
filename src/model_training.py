import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)

from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression

from sklearn.naive_bayes import MultinomialNB

from sklearn.svm import LinearSVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


def load_processed_data(file_path):

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"Processed dataset not found:\n{file_path}"
        )

    df = pd.read_csv(file_path)

    return df


def prepare_data(df):

    target_column = "Fraudulent"

    text_column = "combined_text"

    numeric_columns = [
        "Telecommuting",
        "Has_company_logo",
        "Has_questions"
    ]

    categorical_columns = [
        "Employment_type",
        "Required_experience",
        "Required_education",
        "Industry",
        "Function"
    ]

    required_columns = (
        [target_column, text_column]
        + numeric_columns
        + categorical_columns
    )

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f"Missing columns:\n{missing_columns}"
        )

    X = df[
        [
            text_column
        ]
        + numeric_columns
        + categorical_columns
    ]

    y = df[target_column]

    return X, y


def create_preprocessor():

    text_pipeline = Pipeline(
        steps=[

            (
                "tfidf",

                TfidfVectorizer(

                    max_features=10000,

                    ngram_range=(1, 2),

                    stop_words="english",

                    sublinear_tf=True
                )
            )
        ]
    )

    numeric_pipeline = Pipeline(
        steps=[

            (
                "imputer",

                SimpleImputer(
                    strategy="constant",
                    fill_value=0
                )
            ),

            (
                "scaler",

                StandardScaler(
                    with_mean=False
                )
            )
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[

            (
                "imputer",

                SimpleImputer(
                    strategy="most_frequent"
                )
            ),

            (
                "onehot",

                OneHotEncoder(
                    handle_unknown="ignore"
                )
            )
        ]
    )

    preprocessor = ColumnTransformer(

        transformers=[

            (
                "text",

                text_pipeline,

                "combined_text"
            ),

            (
                "numeric",

                numeric_pipeline,

                [
                    "Telecommuting",
                    "Has_company_logo",
                    "Has_questions"
                ]
            ),

            (
                "categorical",

                categorical_pipeline,

                [
                    "Employment_type",
                    "Required_experience",
                    "Required_education",
                    "Industry",
                    "Function"
                ]
            )
        ]
    )

    return preprocessor


def create_models():

    models = {

        "Logistic Regression":

        LogisticRegression(

            max_iter=1000,

            class_weight="balanced",

            random_state=42
        ),

        "Naive Bayes":

        MultinomialNB(),

        "Linear SVM":

        LinearSVC(

            class_weight="balanced",

            random_state=42
        )
    }

    return models


def train_and_compare_models(
    X_train,
    X_test,
    y_train,
    y_test
):

    models = create_models()

    results = []

    best_model = None

    best_f1 = 0

    best_model_name = None

    for model_name, classifier in models.items():

        print(
            f"\nTraining {model_name}..."
        )

        preprocessor = create_preprocessor()

        pipeline = Pipeline(

            steps=[

                (
                    "preprocessor",

                    preprocessor
                ),

                (
                    "classifier",

                    classifier
                )
            ]
        )

        pipeline.fit(
            X_train,
            y_train
        )

        predictions = pipeline.predict(
            X_test
        )

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        precision = precision_score(
            y_test,
            predictions,
            zero_division=0
        )

        recall = recall_score(
            y_test,
            predictions,
            zero_division=0
        )

        f1 = f1_score(
            y_test,
            predictions,
            zero_division=0
        )

        results.append(

            {

                "Model": model_name,

                "Accuracy": accuracy,

                "Precision": precision,

                "Recall": recall,

                "F1_Score": f1
            }
        )

        print(
            f"{model_name} completed."
        )

        print(
            f"Accuracy: {accuracy:.4f}"
        )

        print(
            f"Precision: {precision:.4f}"
        )

        print(
            f"Recall: {recall:.4f}"
        )

        print(
            f"F1 Score: {f1:.4f}"
        )

        if f1 > best_f1:

            best_f1 = f1

            best_model = pipeline

            best_model_name = model_name

    results_df = pd.DataFrame(
        results
    )

    return (
        results_df,
        best_model,
        best_model_name
    )


if __name__ == "__main__":

    project_root = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    processed_path = os.path.join(

        project_root,

        "data",

        "processed_fake_jobs.csv"
    )

    models_folder = os.path.join(

        project_root,

        "models"
    )

    os.makedirs(
        models_folder,

        exist_ok=True
    )

    df = load_processed_data(
        processed_path
    )

    X, y = prepare_data(
        df
    )

    X_train, X_test, y_train, y_test = train_test_split(

        X,

        y,

        test_size=0.2,

        random_state=42,

        stratify=y
    )

    results_df, best_model, best_model_name = (

        train_and_compare_models(

            X_train,

            X_test,

            y_train,

            y_test
        )
    )

    print("\nMODEL COMPARISON")
    print(results_df)

    results_path = os.path.join(

        models_folder,

        "model_comparison.csv"
    )

    results_df.to_csv(

        results_path,

        index=False
    )

    best_model_path = os.path.join(

        models_folder,

        "best_model.pkl"
    )

    joblib.dump(

        best_model,

        best_model_path
    )

    print(
        f"\nBest Model: {best_model_name}"
    )

    print(
        f"Best model saved at:\n{best_model_path}"
    )