
from flask import Flask, render_template, request

from modules.resume_analyzer import (
    extract_text_from_pdf,
    extract_skills,
    categorize_skills
)

app = Flask(__name__)

# Maximum upload size: 5 MB
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


@app.route("/", methods=["GET", "POST"])
def home():

    skills = []
    skill_categories = {}
    error = None
    analyzed = False

    if request.method == "POST":

        uploaded_file = request.files.get("resume")

        if not uploaded_file or uploaded_file.filename == "":
            error = "Please select a PDF resume."

        elif not uploaded_file.filename.lower().endswith(".pdf"):
            error = "Only PDF files are allowed."

        else:
            try:
                # STEP 1: Extract text from uploaded PDF
                resume_text = extract_text_from_pdf(uploaded_file)

                # STEP 2: Debug information
                print("PDF TEXT LENGTH:", len(resume_text))

                # STEP 3: Check whether PDF contains readable text
                if not resume_text.strip():

                    error = (
                        "No readable text found. "
                        "Please upload a text-based PDF resume."
                    )

                else:
                    # STEP 4: Identify technical skills
                    skills = extract_skills(resume_text)

                    print("EXTRACTED SKILLS:", skills)

                    # STEP 5: Categorize detected skills
                    skill_categories = categorize_skills(skills)

                    # STEP 6: Mark analysis as completed
                    analyzed = True

            except Exception as exc:

                print("RESUME ANALYSIS ERROR:", repr(exc))

                error = (
                    "Unable to read this PDF. "
                    "Please upload a valid, unprotected PDF."
                )

    return render_template(
        "index.html",
        skills=skills,
        skill_categories=skill_categories,
        error=error,
        analyzed=analyzed
    )


@app.route("/health")
def health():

    return {
        "status": "success",
        "message": "SkillBridge AI backend is running!"
    }


@app.errorhandler(413)
def file_too_large(error):

    return render_template(
        "index.html",
        skills=[],
        skill_categories={},
        error="File is too large. Maximum size is 5 MB.",
        analyzed=False
    ), 413


if __name__ == "__main__":
    app.run(debug=True)
