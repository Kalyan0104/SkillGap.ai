 # **🚀SkillGap.ai | AI-Powered Resume Analyst**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Google_Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white" />
</p>

An AI-Integrated Python application that analyzes the gap between a candidate's resume and a job description using LLM-powered reasoning.

🔗 **[Live Demo](https://skillgap-ai.streamlit.app/)**

## **🌟Features**

- **Dynamic Skill Extraction:** Automatically identifies 10-12 core technical skills from any JD using Gemini AI.

- **Resume Parsing:** Extracts and cleans text from PDF resumes with high accuracy.

- **Mentor-Style Advice:** Provides actionable project ideas and learning rescources based on identified gaps.

- **Match Score Calculation:** Quantifiable metric to show resume compatibility with the job role.

- **Data Sanitization:** Robust UTF-8 cleaning to handle hidden characters and prevent API crashes.

- **Interactive UI:** Clean and responsive dashboard built for job seekers.



## **🛠️Tech Stack**



### **Frontend & Backend**

- Python 3.x

- streamlit(Web Framework)

- PyPDF(Text Extraction)



### **AI Services**

- Google Gemini 2.5 Flash(LLM)

- Prompt Engineering for Mentor-style feedback



## **🚀 Quick Start**



**1.Clone the Repository**

  ```Bash

  git clone [https://github.com/Kalyan0104/SkillGap.ai](https://github.com/Kalyan0104/SkillGap.ai)

  cd SkillGap.ai

```

**2.Setup Virtual Environment**

  ```

Bash

```

```

  python -m venv venv

  # On Windows:

  venv\Scripts\activate

  #On Mac/Linux:

  source venv/bin/activate

```

**3.Install Dependencies**

```

Bash

```

  ```

 pip install -r requirements.txt 

 ```  

**4.Configure Secrets**

  ```

    Create .streamlit/secrets.toml:

  ```

  ```

     lni,TOML

       GOOGLE_API_KEY = "your_api_key_here"

  ```

**4.Start the Application****

  ```

  Bash

```

```

streamlit run app.py

```

## **🧠 Logic & Architecture**

### **Data Processing Pipeline**



1.**Extraction:** PyPDF reads raw text from the uploaded resume.



2.**Sanitization:** Custom logic removes UTF-8 surrogates to ensure LLM compatibility.



3.**Contextual Analysis:** Gemini 2.5 Flash extracts skills from the JD.



4.**Matching Engine:** Cross-references extracted skills with santitized resume text.



## **📂Project Structure**

```

Plaintext

```

```text

│─.streamlit/

│    └ secrets.toml    #API Key Configuration(Local Only)

│─app.py               #Main Streamlit Application Logic

│─ requirements.txt    #List of Python dependencies

│─.gitignore           # Files to be ignored by Git

└ README.md            #Project Documentation



```

## **Future Enchancements**

- [] Transition to React Frontend with FastAPI Backend.

- [] Multi-Job description comparison feature.

- [] Autonated PDF report generation for thr mentor advice.

## 🛠️ Key Technical Challenges & Solutions
* **Data Integrity:** Handled "UTF-8 Surrogate" errors during PDF parsing by implementing a custom sanitization layer, ensuring smooth LLM processing.
* **Prompt Engineering:** Optimized Gemini 1.5 Flash prompts to ensure the AI provides structured, mentor-style feedback rather than generic responses.

## 🌱 Learning Outcomes
* **AI Integration:** Mastered the process of connecting Python backends to Google Gemini API.
* **Full-Stack Thinking:** Learned to build end-to-end tools using Streamlit that solve real-world career problems.
* **Documentation:** Improved skills in technical writing and project organization.

### **Author**

## **Kummari Kalyan**

AI-Integrated Python Full Stack Developer.
