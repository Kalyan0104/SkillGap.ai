import streamlit as st
from pypdf import PdfReader
import os
from dotenv import load_dotenv #to handle local key
from langchain_google_genai import GoogleGenerativeAI,GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

load_dotenv()

api_key=os.getenv("GOOGLE_API_KEY")
# ==========================================
# PHASE 4: UI CONFIGURATION & STYLING
# ==========================================
st.set_page_config(page_title="SkillGap.ai v1.0",page_icon="🎯", layout="wide")

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
    }
    </style>
    """, unsafe_allow_html=True)   


# ==========================================
# BACKEND LOGIC (Gemini Powered)
# ==========================================

# PHASE 1: PDF TEXT EXTRACTION

def get_pdf_text(uploaded_file):
    text = ""
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        return f"Error: {e}"

# PHASE 2: DOCUMENT CHUNKING & VECTOR STORAGE

def get_text_chunks(text):
    """Splits the long text into smaller chunks for efficient processing."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_text(text)

def create_vector_store(chunks):
    """Creates an in-memory vector database using ChromaDB and ollama Embeddings."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-001",google_api_key=api_key)
    return Chroma.from_texts(texts=chunks, embedding=embeddings)

# PHASE 3: AI ANALYSIS ENGINE (RAG)
def ask_ai_advice(resume_text, context_data):
    """Generates mentorship advice based on the resume and JD context."""
    llm =GoogleGenerativeAI(model="gemini-1.5-flash",google_api_key=api_key)
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
    return llm.invoke(prompt)


# ==========================================
# FRONTEND UI (Phase 4)
# ==========================================
st.sidebar.title("🚀 SkillGap.ai ")
st.sidebar.info("Analyze your Resume against JDs using RAG technology.")
st.title("🤖 SkillGap.ai: Your Personal AI Career Mentor")

#Two-column layout for file uploads
up_col1, up_col2 = st.columns(2)
with up_col1:
    st.subheader("📄 Step 1 : Your Resume")
    resume_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

with up_col2:
    st.subheader("📂 Step 2: Job Descriptions")
    jd_files = st.file_uploader("Upload JD PDFs", type="pdf", accept_multiple_files=True)

st.markdown("---")

# Execution Button
if st.button("🚀 Analyze Skills & Generate Roadmap "):
    if resume_file and jd_files:
        with st.spinner("Senior Mentor is reviewing your profile... Please wait...."):
            # --- EXECUTION: PHASE 1 ---
            resume_content = get_pdf_text(resume_file)
            
            # --- EXECUTION: PHASE 2 ---
            all_jd_text = ""
            for f in jd_files:
                all_jd_text += get_pdf_text(f)
            
            chunks = get_text_chunks(all_jd_text)
            vector_db = create_vector_store(chunks)
            
            # --- EXECUTION:PHASE 3 ---
            # Retrieve relevant content using similarity search
            context = "\n".join([doc.page_content for doc in vector_db.similarity_search(resume_content, k=2)])
         
            #Metric calculation Logic 
            skills_to_check = ["Python", "Django", "SQL", "Git", "Docker", "API", "Testing","Machine Learning","Kubernetes"]
            found = [s for s in skills_to_check if s.lower() in resume_content.lower()]
            match_p = int((len(found) / len(skills_to_check)) * 100)
            
            #Displaying Metrics
            col1,col2,col3 = st.columns(3)
            with col1:
                st.metric("Match Score", f"{match_p}%")
            with col2:
                st.metric("Skills Found", len(found))
            with col3:
                st.metric("Gaps Identified", len(skills_to_check) - len(found))

            st.progress(match_p / 100)
            
            st.markdown("### ✅ Skills detected in your Resume:")
            st.write(", ".join(found)if found else "No matching skills from the checklist detected.")
            st.markdown("---")    
            
            #FinalAnalysis Output.
            advice = ask_ai_advice(resume_content, context)
            st.success("Analysis Done mowa!")
            st.markdown("### 🌟 AI Mentor Advice")
            st.write(advice)
            
    else:
        st.warning("Please upload both Resume and at least one Job Description(JD).")