import streamlit as st
import tempfile
import os
import json
import asyncio
from tools.pdf_extractor import (
    extract_text_and_style,
    extract_links_with_text_first_page
)
from resume_tailor.components.profile_builder import build_user_profile
from resume_tailor.components.job_search import search_jobs_adzuna
from resume_tailor.components.markdown_builder import insert_links_into_markdown
from resume_tailor.components.docx_builder import save_docx_with_styles
from resume_tailor.ui.sidebar import render_sidebar
from resume_tailor.ui.stepper import render_stepper

# --- CrewAI imports ---
from resume_tailor.crews.crewai_logic import run_crew_for_job

# Define required constants directly here:
OPENAI_KEY_MISSING_INFO = "⚠️ Please enter your OpenAI API key in the sidebar to get started"
HOW_TO_COPY_URL_INFO = (
    "ℹ️ For some job boards, you may need to click the job link, let it redirect, and then copy the final URL from your browser's address bar. Paste that URL below."
)
REDIRECT_INFO = """
<details>
<summary><b>How to get the redirected job URL?</b></summary>
<ol>
    <li>Click the job title link below.</li>
    <li>Wait for the page to fully load (you may be redirected).</li>
    <li>Copy the URL from your browser's address bar.</li>
    <li>Paste it into the URL field below.</li>
</ol>
</details>
"""
HOW_TO_COPY_URL_HELP = "Click the job link below, let it redirect, then copy the final URL from your browser's address bar and paste it here."
STEP_LABELS = [
    "1. **Upload Resume**",
    "2. **Build Profile**",
    "3. **Select Jobs**",
    "4. **Tailor & Download**"
]

# --- Determine current step ---
if "parsed_resume" not in st.session_state:
    current_step = 0
elif "profile" not in st.session_state:
    current_step = 1
elif "jobs" not in st.session_state:
    current_step = 2
elif "tailored_results" not in st.session_state:
    current_step = 3
else:
    current_step = 4

# --- Streamlit App UI ---
st.set_page_config(page_title="AI Resume Tailoring", layout="wide")
st.title("📄 AI-Powered Resume Tailoring")
render_stepper(current_step)

# Logo
st.logo(
    "https://cdn.prod.website-files.com/66cf2bfc3ed15b02da0ca770/66d07240057721394308addd_Logo%20(1).svg",
    link="https://www.crewai.com/",
    size="large"
)

# --- Sidebar ---
sidebar_state = render_sidebar()
selected_model = sidebar_state["model"]
openai_api_key = sidebar_state["openai_api_key"]
num_jobs = sidebar_state["num_jobs"]
if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key
else:
    st.warning(OPENAI_KEY_MISSING_INFO)
    st.stop()

# --- File Upload and Parsing ---
try:
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF)",
        type="pdf",
        disabled="resume_path" in st.session_state
    )
except Exception as e:
    st.error(f"File uploader failed to initialize: {e}")
    st.stop()

if uploaded_file and "resume_path" not in st.session_state:
    try:
        if uploaded_file.type != "application/pdf":
            st.error("❌ Only PDF files are supported. Please upload your resume as a PDF.")
            st.stop()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            st.session_state["resume_path"] = tmp.name
        st.success("PDF uploaded successfully!")
    except Exception as e:
        st.error(f"Failed to save uploaded file: {e}")
        st.stop()

if "resume_path" in st.session_state:
    try:
        # Parse resume only once
        if "parsed_resume" not in st.session_state:
            with st.spinner("Parsing resume..."):
                try:
                    parsed = extract_text_and_style(st.session_state["resume_path"])
                except Exception as e:
                    st.error(f"Failed to parse PDF: {e}")
                    st.stop()
                st.session_state["parsed_resume"] = parsed
                st.session_state["resume_styles"] = parsed["styles"]
                # Extract links from first page
                try:
                    links = extract_links_with_text_first_page(st.session_state["resume_path"])
                except Exception as e:
                    st.error(f"Failed to extract links from PDF: {e}")
                    st.stop()
                st.session_state["resume_links"] = links
                st.success("Resume parsed successfully!")
        parsed = st.session_state["parsed_resume"]
        resume_text = parsed["text"]
        resume_styles = st.session_state["resume_styles"]
    except Exception as e:
        st.error(f"Unexpected error during resume parsing: {e}")
        st.stop()

    with st.expander("📝 View Resume Text"):
        st.text(resume_text)

    # --- Profile Building ---
    if "profile" not in st.session_state:
        with st.spinner("Building user profile..."):
            try:
                profile = build_user_profile(resume_text)
                if not profile:
                    raise ValueError("Profile is empty.")
                st.session_state["profile"] = profile
                st.success("User profile built successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to build user profile: {e}")
                st.stop()
    profile = st.session_state["profile"]

    with st.expander("📝 View Profile"):
        st.text(profile)

    # --- Job Search ---
    if "jobs" not in st.session_state:
        try:
            profile_dict = json.loads(profile)
            jobs = search_jobs_adzuna(profile_dict, num_results=num_jobs)
            if not jobs:
                raise ValueError("No jobs found. Try adjusting your profile or search criteria.")
            st.session_state["jobs"] = jobs
        except Exception as e:
            st.error(f"Job search failed: {e}")
            st.stop()
    jobs = st.session_state["jobs"]

    # --- Job Selection UI ---
    if "job_selections" not in st.session_state:
        st.session_state["job_selections"] = {}

    with st.expander("🔍 Job Matches", expanded=True):
        st.subheader("📝 Select Jobs from the List")
        st.info(HOW_TO_COPY_URL_INFO)
        st.markdown(REDIRECT_INFO, unsafe_allow_html=True)
        st.markdown("&nbsp;", unsafe_allow_html=True)
        if "job_final_urls" not in st.session_state:
            st.session_state["job_final_urls"] = {}
        for i, job in enumerate(jobs):
            adref = job["adref"]
            selected = st.session_state["job_selections"].get(adref, False)
            checked = st.checkbox(
                "Select",
                value=selected,
                key=f"select_{adref}"
            )
            st.session_state["job_selections"][adref] = checked
            job["selected"] = checked

            # URL text input for the final URL
            final_url = st.session_state["job_final_urls"].get(adref, job.get("final_url", ""))
            url_input = st.text_input(
                "URL (paste the actual redirected job URL)",
                value=final_url,
                key=f"final_url_{adref}",
                help=HOW_TO_COPY_URL_HELP
            )
            st.session_state["job_final_urls"][adref] = url_input
            job["final_url"] = url_input if url_input else job["link"]

            st.markdown(f"**[{job['title']}]({job['link']})**  \n{job['company']}")

            if i != len(jobs) - 1:
                st.markdown("---")

    if "tailor_button_clicked" not in st.session_state:
        st.session_state["tailor_button_clicked"] = False

    # --- Tailor My Resume Button ---
    if st.button("Tailor My Resume", disabled=st.session_state["tailor_button_clicked"]):
        # Only consider jobs where both selected and URL is provided
        selected_jobs = []
        missing_url_jobs = []
        for job in jobs:
            adref = job["adref"]
            is_selected = job.get("selected")
            url = st.session_state["job_final_urls"].get(adref, "").strip()
            if is_selected:
                if url:
                    job["final_url"] = url
                    selected_jobs.append(job)
                else:
                    missing_url_jobs.append(job)
        if not selected_jobs:
            st.warning("Please select at least one job and provide a URL for each selected job.")
        elif missing_url_jobs:
            job_titles = ', '.join([f'{job["title"]} at {job["company"]}' for job in missing_url_jobs])
            st.warning(f"Please provide a URL for the following selected job(s): {job_titles}")
        else:
            st.session_state["tailor_button_clicked"] = True
            async def run_all_crews():
                tasks = [run_crew_for_job(job, resume_text, selected_model) for job in selected_jobs]
                try:
                    results = await asyncio.gather(*tasks)
                except Exception as e:
                    st.error(f"Failed to tailor resumes: {e}")
                    return []
                return results
            
            with st.spinner("Tailoring resumes for selected jobs. This may take a while..."):
                tailored_results = asyncio.run(run_all_crews())
                if not tailored_results:
                    raise ValueError("No tailored resumes generated.")
                st.session_state["tailored_results"] = tailored_results

    # --- Display tailored resumes if available ---
    if "tailored_results" in st.session_state:
        st.header("🎯 Tailored Resumes")
        for idx, (job, tailored_resume) in enumerate(st.session_state["tailored_results"]):
            with st.container():
                st.subheader(f"{job['title']} at {job['company']}")
                edited_resume = st.text_area(
                    "Edit your tailored resume below before saving as DOCX:",
                    value=tailored_resume,
                    key=f"edit_resume_{idx}",
                    height=400
                )
                if st.button(f"Save as DOCX for {job['title']} at {job['company']}", key=f"save_docx_{idx}"):
                    links = st.session_state.get("resume_links", [])
                    try:
                        resume_with_links = insert_links_into_markdown(edited_resume, links)
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_docx:
                            try:
                                save_docx_with_styles(resume_with_links, tmp_docx.name)
                            except Exception as e:
                                st.error(f"Failed to generate DOCX: {e}")
                                st.stop()
                            st.success(f"DOCX saved for {job['title']} at {job['company']}.")
                            st.download_button(
                                label="Download DOCX",
                                data=open(tmp_docx.name, "rb").read(),
                                file_name=f"Tailored_{job['title'].replace(' ', '_')}.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                    except Exception as e:
                        st.error(f"Failed to prepare resume for DOCX: {e}")
