import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai

# ==========================================
# CONFIGURATION & API SETUP
# ==========================================

api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)


# ==========================================
# PHASE 4: UI CONFIGURATION & STYLING
# ==========================================
st.set_page_config(page_title="SkillGap.ai v1.1",page_icon="🎯", layout="wide")

#custom css for professional dashboard look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #2E7D32;
        color: white;
        font-weight: bold;
        transition:0.3s;
    }
    .stButton>button:hover{
        background-colour: #1B5e20;
        border: 1px solid white;
    }
    </style>
    """, unsafe_allow_html=True)   


# ==========================================
# BACKEND LOGIC (Gemini Powered)
# ==========================================

# PHASE 1: PDF TEXT EXTRACTION

def get_pdf_text(uploaded_file):
    """Extracts all text from a pdf file."""
    text = ""
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        return f"Error: reading PDF: {e}"

# PHASE 2: AI ANALYSIS ENGINE (RAG)
def ask_ai_advice(resume_text, context_data):
    """communicates directly with gemin i1.5 Flash for career analysis."""

    try:
        """using Gemini 1.5 Flash for fast,accurate analysis."""
        model =genai.Generativemodel("gemini-1.5-flash",
            generation_configuration={"temperature":0.7} 
        )    
        prompt = f"""
        You are a Senior Software Engineer and Mentor. 
        Analyze the student's resume against the Job Description (JD) context.
    
        JD CONTEXT: {context_data}
        RESUME TEXT: {resume_text[:2000]}
    
        STRICT INSTRUCTIONS:
        1. Identify exact missing skills from JD.
        2. Provide a 'Roadmap' style tip for the most critical missing skill.
        3. Keep the tone professional and encouraging.

        FORMAT:
        ### 🚩 Critical Skill Gaps
        - [Skill Name]: Why it matters.

        ### 💡 Mentor's Action Plan
        1. **Short-term:** [Tool/Course]
        2. **Project Idea:** [Small Project]
        """
        response=llm.invoke(prompt)
        return  response.content
    except Exception as e:
        st.error(f"LLM Error:{str(e)}")
        return "AI Advice generation failed."


# ==========================================
# FRONTEND UI (Phase 4)
# ==========================================
st.sidebar.title("🚀 SkillGap.ai ")
st.sidebar.info("Upload your resume and the target Job Description to see where you stand and how to bridge the gap..")
st.title("🤖 SkillGap.ai: Your Personal AI Career Mentor")

#Two-column layout for file uploads
up_col1, up_col2 = st.columns(2)
with up_col1:
    st.subheader("📄 Step 1 : Your Resume")
    resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf",help="please upload your latest resume in PDF formate.")


with up_col2:
    st.subheader("📂 Step 2: Job Descriptions")
    #choice:pdf or text
    jd_method = st.radio("How would you like to provide  JD ?", ("Paste Text","Upload PDF"),horizonatl=True)
    
    final_jd_content=""

    if jd_method == "Paste Text":
        final_jd_content = st.text_area(
            "Paste the JD requirements here:",
            height=200,
            placeholder="Requirements: Python,AWS,Docker,etc..."
        )
    
    else:
        jd_pdf_files=st.file_uploader("Upload JD PDF's",type="pdf",accept_multiple_files=True)
        if jd_pdf_files:
            for f in jd_pdf_files:
                final_jd_content += get_pdf_text(f)

st.markdown("---")

# ==========================================
# EXECUTION & OUTPUT
# ==========================================
if st.button("🚀 Analyze Skills & Generate Roadmap "):
    if resume_file and jd_files:
        with st.spinner("Senior Mentor is reviewing your profile... Please wait...."):
            # --- EXECUTION: PHASE 1 Extraction ---
            resume_content = get_pdf_text(resume_file)
            #----Execution:phase AI Analysis
            advice = ask_ai_advice(resume_content, context)
            #----Exceution:phase Simple Keyqord Metric
            skills_to_check = ["Python", "Django", "SQL", "Git", "Docker", "API", "Testing","Machine Learning","Kubernetes"]
            found_skills = [s for s in skills_to_check if s.lower() in resume_content.lower()]
            match_p = int((len(found_skills) / len(skills_to_check)) * 100)
            
            #Displaying Metrics
            m_col1,m_col2,m_col3 = st.columns(3)
            with m_col1:
                st.metric("Match Score", f"{match_p}%")
            with m_col2:
                st.metric("Skills Found", len(found_skills))
            with m_col3:
                st.metric("Gaps Identified", len(skills_to_check) - len(found_skills))

            st.progress(match_p / 100)
            
            st.markdown("### ✅ Skills detected in your Resume:")
            st.write(", ".join(found_skills)if found_skills else "No matching skills from the checklist detected.")
            st.markdown("---")    
            
            #FinalAnalysis Output.
            st.success("Analysis Done !")
            st.markdown("### 🌟 AI Mentor Advice")
            st.write(advice)
            
    else:
        st.warning("Please upload both Resume and at least one Job Description(JD).")

st.markdown("---")
st.caption("Powered by Gemini 1.5 Flash| Created by SKillGap.ai Team")