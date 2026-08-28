Report
Problem Statement

Fake job postings can mislead job seekers and may be used to collect personal information or money. This project develops a machine learning system that automatically classifies job postings as fraudulent or legitimate using textual and structured job-related features.

Algorithms Used
1. Logistic Regression
2. Multinomial Naive Bayes
3. Linear Support Vector Machine


Text Processing
Text Cleaning
      ↓
TF-IDF Vectorization
      ↓
Numerical Representation


Evaluation Metrics:
Accuracy
Precision
Recall
F1-Score
Confusion Matrix

For this project, F1-score, precision, and recall are especially important, because a model should not simply achieve high accuracy while missing fraudulent job postings.

Final Execution Commands:

Open the terminal in:

D:\fake job posting detection

Then execute:

python src/preprocessing.py

After it finishes:

python src/model_training.py

After training:

python -m streamlit run app/app.py

Your final application will be:

Fake Job Posting Detection System

with the prediction:

✅ Legitimate Job Posting

or:

⚠️ Fraudulent Job Posting