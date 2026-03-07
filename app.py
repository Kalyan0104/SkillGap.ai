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
        reply=(f"Error: reading PDF: {e}")
        return reply

# PHASE 2: AI ANALYSIS ENGINE (RAG)
def ask_ai_advice(resume_text, context_data):
    """communicates directly with gemini 2.5 Flash for career analysis."""

    try:
        #force cleaning the strings to remove hidden surrogate characters.
        #'ignore' error handler removes characters that cause the 'utf-8' codec error
        clean_resume=str(resume_text).encode("utf-8","ignore").decode("utf-8")
        clean_jd=str(context_data).encode("utf-8","ignore").decode("utf-8")
        """using Gemini 2.5 Flash for fast,accurate analysis."""
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config={"temperature": 0.7}
            )
        prompt = f"""
        You are a Senior Software Engineer and career Mentor. 
        Analyze the candidate's resume against the Job Description (JD) context.
    
        JD CONTEXT: {clean_jd}
        RESUME TEXT: {clean_resume[:3000]}
    
        STRICT INSTRUCTIONS:
        1. Identify the most important missing skills.
        2.Explain why each skill matters for this role.
        3. Provide a learning roadmap.
        3. Keep the tone professional and encouraging.

        FORMAT:
        ### 🚩 Critical Skill Gaps
        - [Skill Name]: Why it matters.

        ### 💡 Mentor's Action Plan
        1. Short-term learning step
        2. practical Project Idea
        """
        response=model.generate_content(prompt)
        return  response.text
    except Exception as e:
        st.error(f"AI Error:{str(e)}")
        return "AI Advice generation failed."

def extract_jd_skills(jd_text):
    """Extract skills from JD using Gemini"""
    try:
        model=genai.generativeModel("gemini-2.5-flash")

        prompt=f"""
        Extract exactly 10-12 technical skills/tools from this Job Description.

        return ONLY a comma separated list.

        Example:
        Python,AWS,Docker,React 
        JD:
        {jd_text[:2000]}
        """
        reponse=model.generate_content(prompt)

        skills_list=[
            s.strip()
            for s in response.text.replace("\n","").split(",")
            if s.strip()

        ]
        return skills_list
    except:
        return["Python","React","Node.js","SQL","AWS","Git"]
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
    jd_method = st.radio("How would you like to provide  JD ?", ("Paste Text","Upload PDF"),horizontal=True)
    
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
    if resume_file and final_jd_content:
        with st.spinner("Senior Mentor is reviewing your profile... Please wait...."):
            # --- EXECUTION: PHASE 1 Extraction ---
            resume_content = get_pdf_text(resume_file)
            #----Execution:phase AI Analysis
            advice = ask_ai_advice(resume_content, final_jd_content)
            #----Exceution:phase Simple Keyqord Metric
            skills_to_check = extract_jd_skills(final_jd_content)
            skills_to_check= list(set(skills_to_check))
            found_skills = [s for s in skills_to_check if s.lower() in resume_content.lower()]
            missing_skills = [s for s in skills_to_check if s not in found_skills]
            found_skills.sort()
            missing_skills.sort()
            match_p = int((len(found_skills) / len(skills_to_check)) * 100) if skills_to_check else 0
            
            #Displaying Metrics
            m_col1,m_col2,m_col3 = st.columns(3)
            with m_col1:
                st.metric("Match Score", f"{match_p}%")
            with m_col2:
                st.metric("Skills Found", len(found_skills))
            with m_col3:
                st.metric("Gaps Identified", len(missing_skills))

            st.progress(match_p / 100)
            
            st.markdown("### ✅ Skills detected in your Resume:")
            st.write(", ".join(found_skills)if found_skills else "No matching skills  detected.")

            st.markdown("### ⚠ Missing Skills:")
            st.write(", ".join(missing_skills)if missing_skills else "No skills are missing ")
            st.markdown("---")    
            
            #FinalAnalysis Output.
            st.success(" Analysis Done !")
            st.markdown("### 🚀 AI Mentor Advice")
            st.write(advice)
            
    else:
        st.warning("Please upload both Resume and at least one Job Description(JD).")

st.markdown("---")
st.caption("Powered by Gemini 2.5 Flash| Created by SKillGap.ai Team")