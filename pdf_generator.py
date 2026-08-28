from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from reportlab.lib.pagesizes import letter

from reportlab.lib import colors

from reportlab.lib.units import inch

from datetime import datetime

import io



def add_footer(canvas, document):

    canvas.saveState()

    canvas.setFont(
        "Helvetica",
        8
    )

    footer_text = (
    "Fake Job Posting Detection System | "
    "Secure Recruitment Through Machine Learning & Artificial Intelligence| "
    "Real-Time Job Prediction & Analysis"
)
    

    canvas.drawCentredString(
        letter[0] / 2,
        0.4 * inch,
        footer_text
    )

    canvas.restoreState()





def generate_pdf_report(

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


    buffer = io.BytesIO()


    document = SimpleDocTemplate(

        buffer,

        pagesize=letter,

        rightMargin=50,

        leftMargin=50,

        topMargin=50,

        bottomMargin=50

    )


    styles = getSampleStyleSheet()



    title_style = ParagraphStyle(

        "CustomTitle",

        parent=styles["Title"],

        alignment=1,

        textColor=colors.darkblue,

        fontSize=18,

        spaceAfter=20

    )



    heading_style = ParagraphStyle(

        "Heading",

        parent=styles["Heading2"],

        textColor=colors.darkblue,

        spaceBefore=15,

        spaceAfter=10

    )



    normal_style = ParagraphStyle(

        "NormalText",

        parent=styles["BodyText"],

        fontSize=10,

        leading=14

    )



    content = []



    # -----------------------------
    # TITLE
    # -----------------------------

    content.append(

        Paragraph(

            "FAKE JOB POSTING DETECTION REPORT",

            title_style

        )

    )


    content.append(

        Paragraph(

            f"Generated On: {datetime.now().strftime('%d %B %Y | %I:%M %p')}",

            normal_style

        )

    )


    content.append(
        Spacer(1,20)
    )



    # -----------------------------
    # JOB DETAILS TABLE
    # -----------------------------


    content.append(

        Paragraph(

            "JOB DETAILS",

            heading_style

        )

    )


    job_details = [


        ["Field","Information"],


        ["Job Title", title],

        ["Location", location],

        ["Department", department],

        ["Salary Range", salary_range],

        ["Employment Type", employment_type],

        ["Experience", required_experience],

        ["Education", required_education],

        ["Industry", industry],

        ["Function", function],

        ["Telecommuting", str(telecommuting)],

        ["Company Logo", str(has_company_logo)],

        ["Screening Questions", str(has_questions)]

    ]



    table = Table(

        job_details,

        colWidths=[2*inch, 3.5*inch]

    )



    table.setStyle(

        TableStyle([


            (
                "BACKGROUND",
                (0,0),
                (-1,0),
                colors.darkblue
            ),


            (
                "TEXTCOLOR",
                (0,0),
                (-1,0),
                colors.white
            ),


            (
                "GRID",
                (0,0),
                (-1,-1),
                0.5,
                colors.grey
            ),


            (
                "VALIGN",
                (0,0),
                (-1,-1),
                "TOP"
            ),


            (
                "BACKGROUND",
                (0,1),
                (-1,-1),
                colors.whitesmoke
            )

        ])

    )


    content.append(table)



    # -----------------------------
    # PREDICTION RESULT
    # -----------------------------


    content.append(

        Spacer(1,20)

    )


    content.append(

        Paragraph(

            "PREDICTION RESULT",

            heading_style

        )

    )


    if prediction == "Fraudulent Job Posting":

        result_color = colors.red

        risk = "HIGH"

    else:

        result_color = colors.green

        risk = "LOW"



    prediction_table = Table(

        [

            [

                "Prediction",

                prediction

            ],

            [

                "Risk Level",

                risk

            ]

        ],

        colWidths=[2*inch,3.5*inch]

    )



    prediction_table.setStyle(

        TableStyle([


            (
                "BACKGROUND",
                (0,0),
                (-1,-1),
                result_color
            ),


            (
                "TEXTCOLOR",
                (0,0),
                (-1,-1),
                colors.white
            ),


            (
                "GRID",
                (0,0),
                (-1,-1),
                0.5,
                colors.black
            )

        ])

    )



    content.append(prediction_table)



    # -----------------------------
    # TEXT SECTIONS
    # -----------------------------


    sections = [

        ("COMPANY PROFILE", company_profile),

        ("JOB DESCRIPTION", description),

        ("REQUIREMENTS", requirements),

        ("BENEFITS", benefits)

    ]



    for heading, text in sections:


        content.append(

            Paragraph(

                heading,

                heading_style

            )

        )


        content.append(

            Paragraph(

                str(text),

                normal_style

            )

        )


        content.append(

            Spacer(1,10)

        )




    # -----------------------------
    # SUMMARY
    # -----------------------------


    content.append(

        Paragraph(

            "REPORT SUMMARY",

            heading_style

        )

    )


    summary = f"""

    The machine learning model analyzed the provided job posting

    information and classified this posting as:

    <b>{prediction}</b>

    """


    content.append(

        Paragraph(

            summary,

            normal_style

        )

    )



    content.append(

        Spacer(1,20)

    )


    content.append(

        Paragraph(

        """Fake Job Posting Detection System<br/>
           Powered by Machine Learning | Scikit-learn | Streamlit<br/>
           Predict • Analyze • Detect • Download Reports<br/>
           Developed by: Sweta Chauhan<br/>
           B.Tech CSE (AI, ML & DL)<br/>
           Version 1.0.0 | © 2026 All Rights Reserved""",

            normal_style

        )

    )



    document.build(

        content,

        onFirstPage=add_footer,

        onLaterPages=add_footer

    )



    pdf = buffer.getvalue()


    buffer.close()


    return pdf