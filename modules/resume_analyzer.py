
import pymupdf
import re


def extract_text_from_pdf(pdf_file):
    """Extract text from an uploaded PDF resume."""

    document = pymupdf.open(
        stream=pdf_file.read(),
        filetype="pdf"
    )

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


def extract_skills(resume_text):
    """Identify technical skills from resume text."""

    skills_database = [
        "Python",
        "Java",
        "C",
        "C++",
        "SQL",
        "HTML",
        "CSS",
        "JavaScript",
        "Flask",
        "Django",
        "Machine Learning",
        "Deep Learning",
        "Data Science",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "TensorFlow",
        "React",
        "Git",
        "GitHub",
        "MySQL",
        "MongoDB",
        "AWS"
    ]

    found_skills = []

    for skill in skills_database:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, resume_text, re.IGNORECASE):
            found_skills.append(skill)

    return found_skills

def categorize_skills(skills):
    """Group detected skills into technical categories."""

    categories = {
        "Programming Languages": [
            "Python", "Java", "C", "C++", "JavaScript"
        ],

        "Web Technologies": [
            "HTML", "CSS", "Flask", "Django", "React"
        ],

        "Databases": [
            "SQL", "MySQL", "MongoDB"
        ],

        "Data Science & Machine Learning": [
            "Pandas", "NumPy", "Scikit-learn",
            "TensorFlow", "Machine Learning",
            "Deep Learning", "Data Science"
        ],

        "Tools & Cloud": [
            "Git", "GitHub", "AWS"
        ]
    }

    categorized = {}

    for category, category_skills in categories.items():

        matched = [
            skill for skill in skills
            if skill in category_skills
        ]

        if matched:
            categorized[category] = matched

    return categorized
