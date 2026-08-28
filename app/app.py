import os
import sys

import streamlit as st
import pandas as pd


# ---------------------------------------------------
# Add Project Root Path
# ---------------------------------------------------

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(PROJECT_ROOT)


# ---------------------------------------------------
# Import Project Functions
# ---------------------------------------------------

from src.prediction import (
    load_model,
    predict_job,
    create_job_data
)

from pdf_generator import generate_pdf_report
from csv_generator import save_prediction_csv



# ---------------------------------------------------
# Streamlit Page Configuration
# ---------------------------------------------------

st.set_page_config(

    page_title="Fake Job Detection System",

    page_icon="🔍",

    layout="wide"

)


# ---------------------------------------------------
# Application Title
# ---------------------------------------------------

st.title(
    "🔍 Fake Job Posting Detection System"
)


st.write(
    "Machine Learning based system to classify "
    "job postings as legitimate or fraudulent."
)



# ---------------------------------------------------
# Load Model
# ---------------------------------------------------

MODEL_PATH = os.path.join(

    PROJECT_ROOT,

    "models",

    "model.pkl"

)


try:

    model = load_model(
        MODEL_PATH
    )

    st.success(
        "✅ Model loaded successfully"
    )


except Exception as error:

    st.error(
        f"❌ Model loading failed: {error}"
    )

    st.stop()



# ---------------------------------------------------
# Input Section
# ---------------------------------------------------

st.header(
    "Enter Job Posting Details"
)



title = st.text_input(
    "Job Title"
)


location = st.text_input(
    "Location"
)


department = st.text_input(
    "Department"
)


salary_range = st.text_input(
    "Salary Range"
)



company_profile = st.text_area(
    "Company Profile"
)



description = st.text_area(
    "Job Description"
)



requirements = st.text_area(
    "Requirements"
)



benefits = st.text_area(
    "Benefits"
)



# ---------------------------------------------------
# Binary Features
# ---------------------------------------------------

col1, col2, col3 = st.columns(3)


with col1:

    telecommuting = st.selectbox(

        "Telecommuting",

        [0,1]

    )


with col2:

    has_company_logo = st.selectbox(

        "Has Company Logo",

        [0,1]

    )


with col3:

    has_questions = st.selectbox(

        "Has Questions",

        [0,1]

    )



employment_type = st.text_input(
    "Employment Type"
)



required_experience = st.text_input(
    "Required Experience"
)



required_education = st.text_input(
    "Required Education"
)



industry = st.text_input(
    "Industry"
)



function = st.text_input(
    "Function"
)




# ---------------------------------------------------
# Prediction Button
# ---------------------------------------------------

if st.button(
    "🔍 Predict Job Posting"
):


    try:


        # Combine text fields

        combined_text = " ".join([

            str(title),

            str(location),

            str(department),

            str(salary_range),

            str(company_profile),

            str(description),

            str(requirements),

            str(benefits),

            str(employment_type),

            str(required_experience),

            str(required_education),

            str(industry),

            str(function)

        ])



        # Create model input

        job_data = create_job_data(

            combined_text=combined_text,

            telecommuting=telecommuting,

            has_company_logo=has_company_logo,

            has_questions=has_questions,

            employment_type=employment_type,

            required_experience=required_experience,

            required_education=required_education,

            industry=industry,

            function=function

        )



        # Prediction

        result, confidence = predict_job(

            model,

            job_data

        )



        # Display Result

        if result == "Fraudulent Job Posting":

            st.error("⚠️ This job posting is predicted as FRAUDULENT.")

            st.metric(
             "🎯 AI Confidence",
             f"{confidence:.2f}%"
    )

            st.progress(confidence / 100)

        else:

             st.success("✅ This job posting is predicted as LEGITIMATE.")

             st.metric(
             "🎯 AI Confidence",
             f"{confidence:.2f}%"
    )

        st.progress(confidence / 100)

        # ---------------------------------------------------
        # Generate PDF
        # ---------------------------------------------------

        pdf_file = generate_pdf_report(

            title,

            location,

            department,

            salary_range,

            company_profile,

            description,

            requirements,

            benefits,

            telecommuting,

            has_company_logo,

            has_questions,

            employment_type,

            required_experience,

            required_education,

            industry,

            function,

            result

        )



        st.download_button(

            label="📄 Download PDF Report",

            data=pdf_file,

            file_name="Job_Prediction_Report.pdf",

            mime="application/pdf"

        )




        # ---------------------------------------------------
        # Save CSV History
        # ---------------------------------------------------

        csv_file = save_prediction_csv(

            title,

            location,

            department,

            salary_range,

            company_profile,

            description,

            requirements,

            benefits,

            telecommuting,

            has_company_logo,

            has_questions,

            employment_type,

            required_experience,

            required_education,

            industry,

            function,

            result

        )



        st.download_button(

            label="📊 Download CSV Report",

            data=csv_file,

            file_name="prediction_history.csv",

            mime="text/csv"

        )



    except Exception as error:


        st.error(

            f"Prediction failed: {error}"

        )