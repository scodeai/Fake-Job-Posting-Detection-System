import os
import re
import pandas as pd


REQUIRED_COLUMNS = [
    "Job_id",
    "Title",
    "Location",
    "Department",
    "Salary_range",
    "Company_profile",
    "Description",
    "Requirements",
    "Benefits",
    "Telecommuting",
    "Has_company_logo",
    "Has_questions",
    "Employment_type",
    "Required_experience",
    "Required_education",
    "Industry",
    "Function",
    "Fraudulent"
]


TEXT_COLUMNS = [
    "Title",
    "Location",
    "Department",
    "Salary_range",
    "Company_profile",
    "Description",
    "Requirements",
    "Benefits",
    "Employment_type",
    "Required_experience",
    "Required_education",
    "Industry",
    "Function"
]


def clean_text(text):
    """
    Clean text data.
    """

    if pd.isna(text):
        return ""

    text = str(text).lower()

    # Remove HTML tags
    text = re.sub(r"<.*?>", " ", text)

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", " ", text)

    # Remove email addresses
    text = re.sub(r"\S+@\S+", " ", text)

    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def load_data(file_path):
    """
    Load CSV dataset.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Dataset not found at:\n{file_path}"
        )

    df = pd.read_csv(file_path)

    print(f"Dataset loaded successfully.")
    print(f"Shape: {df.shape}")

    return df


def validate_columns(df):
    """
    Check whether required columns exist.
    """

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns in dataset:\n{missing_columns}\n\n"
            f"Available columns are:\n{list(df.columns)}"
        )

    print("All required columns are present.")


def preprocess_data(df):
    """
    Complete preprocessing pipeline.
    """

    df = df.copy()

    # Validate columns
    validate_columns(df)

    # Remove duplicate rows
    before_duplicates = len(df)

    df = df.drop_duplicates()

    after_duplicates = len(df)

    print(
        f"Removed duplicates: "
        f"{before_duplicates - after_duplicates}"
    )

    # Convert target column to numeric
    df["Fraudulent"] = pd.to_numeric(
        df["Fraudulent"],
        errors="coerce"
    )

    # Remove rows with missing target
    df = df.dropna(subset=["Fraudulent"])

    # Ensure target is integer
    df["Fraudulent"] = df["Fraudulent"].astype(int)

    # Clean all text columns
    for column in TEXT_COLUMNS:

        if column in df.columns:
            df[column] = df[column].fillna("")
            df[column] = df[column].apply(clean_text)

    # Fill numeric columns
    numeric_columns = [
        "Telecommuting",
        "Has_company_logo",
        "Has_questions"
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

            df[column] = df[column].fillna(0)

    # Create combined text
    df["combined_text"] = (
        df["Title"] + " " +
        df["Location"] + " " +
        df["Department"] + " " +
        df["Salary_range"] + " " +
        df["Company_profile"] + " " +
        df["Description"] + " " +
        df["Requirements"] + " " +
        df["Benefits"] + " " +
        df["Employment_type"] + " " +
        df["Required_experience"] + " " +
        df["Required_education"] + " " +
        df["Industry"] + " " +
        df["Function"]
    )

    # Remove rows with empty text
    df = df[
        df["combined_text"].str.strip() != ""
    ]

    print("Preprocessing completed.")
    print(f"Final shape: {df.shape}")

    return df


if __name__ == "__main__":

    project_root = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    input_path = os.path.join(
        project_root,
        "data",
        "fake_job_posting.csv"
    )

    output_path = os.path.join(
        project_root,
        "data",
        "processed_fake_jobs.csv"
    )

    df = load_data(input_path)

    df_processed = preprocess_data(df)

    df_processed.to_csv(
        output_path,
        index=False
    )

    print(
        f"Processed dataset saved at:\n{output_path}"
    )