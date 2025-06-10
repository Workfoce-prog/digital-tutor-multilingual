import streamlit as st
import re
import math
from langdetect import detect
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

st.set_page_config(page_title="Digital Tutor Multilingual Demo", page_icon="🌍")
st.title("🌍 Digital Tutor (Multilingual + Algebra Solver)")

subjects = [
    "Algebra", "Quadratic Equations", "Radicals", "Exponential Functions",
    "Parabolas", "College Algebra", "Statistics", "Data Science"
]

languages = {
    "Auto-detect": None,
    "English": "en",
    "French": "fr",
    "Spanish": "es",
    "Arabic": "ar",
    "Swahili": "sw"
}

translations = {
    "fr": "Ce résultat est une simulation de réponse traduite en français.",
    "es": "Este resultado es una simulación de respuesta traducida al español.",
    "sw": "Huu ni mfano wa majibu yaliyotafsiriwa kwa Kiswahili.",
    "ar": "هذه نتيجة محاكاة لإجابة مترجمة إلى العربية."
}

def fake_translate(text, lang_code):
    if lang_code in translations:
        return f"{translations[lang_code]}\n\n{text}"
    return text

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def solve_linear_equation(equation):
    try:
        match = re.match(r'([-+]?\d*)x\s*([+-]\s*\d+)?\s*=\s*([-+]?\d+)', equation.replace(" ", ""))
        if not match:
            return None
        a = match.group(1)
        b = match.group(2)
        c = match.group(3)
        a = int(a) if a not in [None, "", "+"] else 1
        a = -1 if a == "-" else a
        b = int(b.replace(" ", "")) if b else 0
        c = int(c)
        x = (c - b) / a
        return f"Let's solve: {equation}\n\nStep 1: Move the constant term\n{a}x = {c - b}\nStep 2: Divide by {a}\n→ x = {x}"
    except:
        return None

def solve_quadratic(eq_text):
    match = re.findall(r"([-+]?\d*)x\^2\s*([-+]\s*\d*)x\s*([-+]\s*\d+)", eq_text.replace(" ", ""))
    if not match:
        return "Please provide a quadratic in the form ax² + bx + c = 0"
    a, b, c = match[0]
    a = int(a) if a not in ["", "+"] else 1
    b = int(b.replace(" ", "")) if b else 0
    c = int(c.replace(" ", ""))
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return f"The equation has no real roots (discriminant = {discriminant})."
    elif discriminant == 0:
        root = -b / (2*a)
        return f"The equation has one real root: x = {root}"
    else:
        root1 = (-b + math.sqrt(discriminant)) / (2*a)
        root2 = (-b - math.sqrt(discriminant)) / (2*a)
        return f"The equation has two real roots: x = {root1:.2f}, x = {root2:.2f}"

def simplify_radical(expr):
    match = re.match(r"√(\d+)", expr.replace(" ", ""))
    if not match:
        return "Try a format like √50"
    num = int(match.group(1))
    factor = int(math.sqrt(num))
    while factor > 1:
        if num % (factor**2) == 0:
            outside = factor
            inside = num // (factor**2)
            return f"Simplified: √{num} = {outside}√{inside}"
        factor -= 1
    return f"√{num} cannot be simplified further."

def solve_exponential(expr):
    match = re.match(r"(\d+)\^x=(\d+)", expr.replace(" ", ""))
    if not match:
        return "Try a format like 2^x=8"
    base, result = int(match.group(1)), int(match.group(2))
    x = math.log(result, base)
    return f"{base}^x = {result} → x = log_{base}({result}) = {x:.2f}"

def tutor_response(question, subject):
    if subject == "Algebra":
        solution = solve_linear_equation(question)
        return solution or "Try a linear equation like x + 2 = 5"
    elif subject == "Quadratic Equations":
        return solve_quadratic(question)
    elif subject == "Radicals":
        return simplify_radical(question)
    elif subject == "Exponential Functions":
        return solve_exponential(question)
    elif subject == "Parabolas":
        return "y = ax² + bx + c → Vertex: x = -b/(2a); Symmetry: vertical line; Shape: opens up if a > 0"
    elif subject == "College Algebra":
        return "College Algebra covers factoring, expressions, and functions. Example: x² - 4 = (x - 2)(x + 2)"
    elif subject == "Statistics":
        return "Mean = average; Median = middle; Mode = most frequent; Std Dev = spread of data"
    elif subject == "Data Science":
        return "Data science includes: data wrangling, visualization, and basic machine learning."
    return "Try asking a math question related to the selected subject."

def generate_pdf(questions, answers):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, 740, "Grade 6–12 Worksheet (Demo)")
    c.setFont("Helvetica", 12)
    y = 700
    for q, a in zip(questions, answers):
        c.drawString(72, y, q)
        y -= 20
        c.drawString(92, y, f"Answer: {a}")
        y -= 30
    c.save()
    buffer.seek(0)
    return buffer

tab1, tab2 = st.tabs(["🎓 Tutor", "📝 Worksheet Generator"])

with tab1:
    st.header("Ask the Digital Tutor")
    col1, col2 = st.columns(2)
    with col1:
        student_name = st.text_input("Student Name (optional)")
    with col2:
        language_selection = st.selectbox("Select Language", list(languages.keys()))
    subject = st.selectbox("Select a Subject", subjects)
    question = st.text_area("Enter your question:")
    if question:
        lang_code = languages[language_selection] or detect_language(question)
        raw_response = tutor_response(question, subject)
        response = fake_translate(raw_response, lang_code)
        st.markdown("### 📘 Demo Response:")
        st.markdown(response)

with tab2:
    st.header("Generate Practice Worksheets (Demo)")
    subject = st.selectbox("Worksheet Subject", subjects, key="worksheet_subject")
    num_q = st.slider("Number of Questions", 1, 5, 3)
    difficulty = st.radio("Select Difficulty", ["Easy", "Medium", "Hard"], horizontal=True)
    if st.button("Generate Worksheet PDF"):
        questions = [f"{i+1}. Sample {difficulty} question in {subject}" for i in range(num_q)]
        answers = [f"Sample Answer {i+1}" for i in range(num_q)]
        pdf = generate_pdf(questions, answers)
        st.download_button("📄 Download PDF", pdf, file_name="worksheet_demo.pdf")
