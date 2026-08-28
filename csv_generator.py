import pandas as pd
import os
import io
from datetime import datetime



REPORT_FOLDER = "reports"

CSV_FILE = os.path.join(
    REPORT_FOLDER,
    "prediction_history.csv"
)



def save_prediction_csv(

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
    prediction

):


    # Create reports folder

    if not os.path.exists(REPORT_FOLDER):

        os.makedirs(REPORT_FOLDER)



    # Create new prediction record

    data = {


        "Date":

        datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        ),


        "Job Title":

        title,


        "Location":

        location,


        "Department":

        department,


        "Salary Range":

        salary_range,


        "Company Profile":

        company_profile,


        "Job Description":

        description,


        "Requirements":

        requirements,


        "Benefits":

        benefits,


        "Telecommuting":

        telecommuting,


        "Company Logo":

        has_company_logo,


        "Has Questions":

        has_questions,


        "Employment Type":

        employment_type,


        "Experience":

        required_experience,


        "Education":

        required_education,


        "Industry":

        industry,


        "Function":

        function,


        "Prediction":

        prediction

    }



    new_data = pd.DataFrame(
        [data]
    )



    # Append old history

    if os.path.exists(CSV_FILE):

        old_data = pd.read_csv(
            CSV_FILE
        )


        final_data = pd.concat(

            [
                old_data,
                new_data
            ],

            ignore_index=True

        )


    else:

        final_data = new_data



    # Save CSV file

    final_data.to_csv(

        CSV_FILE,

        index=False

    )



    # Return CSV for download button

    csv_buffer = io.StringIO()


    final_data.to_csv(

        csv_buffer,

        index=False

    )


    return csv_buffer.getvalue()