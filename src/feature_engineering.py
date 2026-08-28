import pandas as pd


def create_features(df):

    df = df.copy()

    # Text length features
    df["description_length"] = (
        df["Description"]
        .fillna("")
        .astype(str)
        .str.len()
    )

    df["requirements_length"] = (
        df["Requirements"]
        .fillna("")
        .astype(str)
        .str.len()
    )

    df["company_profile_length"] = (
        df["Company_profile"]
        .fillna("")
        .astype(str)
        .str.len()
    )

    df["benefits_length"] = (
        df["Benefits"]
        .fillna("")
        .astype(str)
        .str.len()
    )

    # Word count
    df["description_word_count"] = (
        df["Description"]
        .fillna("")
        .astype(str)
        .str.split()
        .str.len()
    )

    df["requirements_word_count"] = (
        df["Requirements"]
        .fillna("")
        .astype(str)
        .str.split()
        .str.len()
    )

    # Count suspicious terms
    suspicious_words = [
        "urgent",
        "easy money",
        "work from home",
        "no experience",
        "quick money",
        "guaranteed",
        "investment",
        "fee",
        "payment"
    ]

    df["suspicious_word_count"] = 0

    combined_text = (
        df["combined_text"]
        .fillna("")
        .astype(str)
    )

    for word in suspicious_words:

        df["suspicious_word_count"] += (
            combined_text
            .str.lower()
            .str.count(word)
        )

    return df