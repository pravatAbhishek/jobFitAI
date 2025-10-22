# frontend/app.py

import streamlit as st
import requests
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from streamlit_option_menu import option_menu

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="Resume Skill Matcher", layout="wide")

# ----------------------------
# CSS for Sticky Navbar, Background, Overlay, Hover Effects
# ----------------------------
st.markdown("""
    <style>
    div[data-baseweb="option-menu"] {
        position: sticky;
        top: 0;
        z-index: 1000;
    }

    div[data-baseweb="option-menu"] > div {
        background-color: #1F2937;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        transition: background 0.3s ease;
    }

    div[data-baseweb="option-menu"] > div:hover {
        background: linear-gradient(90deg, #F97316, #F59E0B) !important;
    }

    .nav-link {
        color: white !important;
        transition: color 0.3s ease, transform 0.2s ease;
    }

    .nav-link:hover {
        color: #FBBF24 !important;
        transform: scale(1.05);
    }

    .nav-link-selected {
        background-color: #F97316 !important;
        color: white !important;
        font-weight: bold;
    }

    .stApp {
        background-image: url("https://images.unsplash.com/photo-1483685678470-3a8a6e8d7a6d");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .stApp::before {
        content: "";
        background-color: rgba(0,0,0,0.4);
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        z-index: -1;
    }

    .main .block-container {
        padding-top: 3rem;
        padding-left: 3rem;
        padding-right: 3rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# Backend Communication Function
# ----------------------------
def analyze_resume(resume_file, job_desc):
    backend_url = "http://127.0.0.1:5000/match"  # Flask endpoint

    try:
        # Ensure the uploaded file is sent as a file object
        files = {'resume': (resume_file.name, resume_file, resume_file.type)}
        data = {'job_description': job_desc}

        response = requests.post(backend_url, files=files, data=data)

        if response.status_code == 200:
            result = response.json()
            return {
                'match_score': result.get('match_score', 0),
                'matched_skills': result.get('common_skills', []),
                'missing_skills': result.get('missing_skills', [])
            }
        else:
            st.error(f"Backend Error ({response.status_code}): {response.text}")
            return {'match_score': 0, 'matched_skills': [], 'missing_skills': []}

    except Exception as e:
        st.error(f"Error connecting to backend: {e}")
        return {'match_score': 0, 'matched_skills': [], 'missing_skills': []}

# ----------------------------
# PDF Generation Function
# ----------------------------
def generate_pdf(result):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, "Resume Skill Matcher Report")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, 720, f"Match Score: {result['match_score']}%")
    
    c.drawString(50, 700, "Matched Skills:")
    y = 680
    for skill in result['matched_skills']:
        c.drawString(70, y, f"- {skill}")
        y -= 20
    
    c.drawString(50, y-10, "Missing Skills:")
    y -= 30
    for skill in result['missing_skills']:
        c.drawString(70, y, f"- {skill}")
        y -= 20
    
    c.save()
    buffer.seek(0)
    return buffer

# ----------------------------
# Top Menu Bar
# ----------------------------
selected = option_menu(
    menu_title=None,
    options=["Home", "Demo", "Info", "Contact"],
    icons=["house", "play-circle", "info-circle", "envelope"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#1F2937"},
        "icon": {"color": "white", "font-size": "20px"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color": "#374151"},
        "nav-link-selected": {"background-color": "#F97316", "color": "white"},
    }
)

# ----------------------------
# Home Page
# ----------------------------
if selected == "Home":
    st.title("📝 Resume Skill Matcher")
    st.write("""
    Welcome to the **Resume Skill Matcher**!  
    Quickly analyze your resume against any job description.  
    Navigate to the **Demo** tab to try it out, or **Info** to learn more about the tool.
    """)

# ----------------------------
# Demo Page
# ----------------------------
elif selected == "Demo":
    st.title("💻 Demo - Try it Now!")

    resume_file = st.file_uploader("Upload Resume (PDF or TXT)", type=["pdf","txt"], help="Only PDF or TXT files allowed")
    job_desc = st.text_area("Paste Job Description Here", height=150, placeholder="Copy-paste the job description here...")

    if st.button("Analyze 🧠"):
        if not resume_file or not job_desc.strip():
            st.warning("Please upload a resume and paste a job description.")
        else:
            result = analyze_resume(resume_file, job_desc)
            
            st.subheader("Match Score")
            st.progress(result['match_score']/100)
            st.write(f"**{result['match_score']}%** match with the job description.")
            
            st.subheader("Matched Skills ✅")
            for skill in result['matched_skills']:
                st.markdown(f"<span style='color:green;font-weight:bold'>{skill}</span>", unsafe_allow_html=True)

            st.subheader("Missing Skills ❌")
            for skill in result['missing_skills']:
                st.markdown(f"<span style='color:red;font-weight:bold'>{skill}</span>", unsafe_allow_html=True)
            
            pdf_buffer = generate_pdf(result)
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_buffer,
                file_name="resume_skill_report.pdf",
                mime="application/pdf"
            )

# ----------------------------
# Info Page
# ----------------------------
elif selected == "Info":
    st.title("ℹ️ Information")
    with st.container():
        with st.expander("About Resume Skill Matcher"):
            st.write("""
            Resume Skill Matcher helps users analyze how well their resume matches a given job description.
            """)
        with st.expander("How it Works"):
            st.write("""
            1. Upload your resume (PDF/TXT).  
            2. Paste the job description.  
            3. Click Analyze to view matched skills, missing skills, and match percentage.  
            4. Download the PDF report.
            """)

# ----------------------------
# Contact Page
# ----------------------------
elif selected == "Contact":
    st.title("📬 Contact Our Team")
    st.write("Reach out to our team members:")

    team_members = {
        "ABHISHEK KUMAR - Backend Lead": "abhishek.pravat@gmail.com",
        "KRISHNA KUMAR - Frontend Lead": "krishnakumar.s9475@gmail.com",
        "RITHESH H B - UX / Research": "rithuu20077@gmail.com",
        "AKASH K N - Documentation": "akashnagaraju91@gmail.com"
    }

    for name, email in team_members.items():
        st.write(f"- **{name}**: {email}")

    st.write("- GitHub: https://github.com/TeamCatalyst")
