# AI Resume Tailor

AI Resume Tailor is a Streamlit web app that helps you upload your resume, automatically parses and builds a professional profile, searches for relevant job postings, and tailors your resume for each selected job using AI. Download your tailored resumes as DOCX files, optimized for ATS and job-specific requirements.

## Features
- Upload your resume in PDF format
- Automatic resume parsing and profile building
- AI-powered job search and job selection
- Resume tailoring for each job using CrewAI agents
- Download tailored resumes as DOCX
- Modern, user-friendly Streamlit interface

## Demo
Deploy this app instantly on [Streamlit Community Cloud](https://streamlit.io/cloud) or run locally (see below).

## Setup & Installation

### 1. Requirements
- Python 3.10, 3.11, or 3.12
- [Streamlit Community Cloud](https://streamlit.io/cloud) (for deployment)

### 2. Local Installation
Clone the repository:
```bash
git clone https://github.com/yourusername/ai-resume-tailor.git
cd ai-resume-tailor
```
Install dependencies:
```bash
pip install -r src/resume_tailor/requirements.txt
```

### 3. Running Locally
```bash
streamlit run src/resume_tailor/app.py
```

### 4. Deploying to Streamlit Community Cloud
- Push your code to a public GitHub repository.
- On [Streamlit Cloud](https://streamlit.io/cloud), click "New app" and select your repo and `src/resume_tailor/app.py` as the entry point.
- Add your OpenAI API key as a secret or enter it in the sidebar when prompted.

## Usage
1. Upload your resume (PDF).
2. The app parses your resume and builds your profile.
3. The app searches for job matches based on your profile.
4. Select jobs and paste the final redirected job URL for each.
5. Click "Tailor My Resume" to generate tailored resumes.
6. Download your tailored resumes as DOCX files.

## Environment Variables
- `OPENAI_API_KEY`: Required for AI-powered features. Enter in the sidebar or set as an environment variable.
- `SERPER_API_KEY`, `ADZUNA_APP_ID`, `ADZUNA_APP_KEY`: Required for job search features.

For local deployment, rename `.example.env` to `.env` and add your own API keys for SERPER and Adzuna:

```
SERPER_API_KEY=<YOUR_SERPER_API_KEY>
ADZUNA_APP_ID=<YOUR_ADZUNA_APP_ID>
ADZUNA_APP_KEY=<YOUR_ADZUNA_APP_KEY>
```

You can obtain these keys from:
- [SerpApi](https://serpapi.com/)
- [Adzuna Developer Portal](https://developer.adzuna.com/)

## Tech Stack
- Streamlit
- Python
- CrewAI & crewai_tools
- OpenAI API
- PyMuPDF (fitz)
- pypandoc
- pydantic
- requests

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## Support
- For questions or issues, open an issue on this repo.
- For CrewAI documentation, visit [crewai.com](https://crewai.com).

---
**AI Resume Tailor** — Effortlessly tailor your resume for every job.
