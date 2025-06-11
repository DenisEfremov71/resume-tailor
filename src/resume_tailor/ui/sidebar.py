import streamlit as st
import os

def render_sidebar():
    with st.sidebar:
        # 1. Free/Paid selection
        with st.expander("🧑‍💼 Account Type", expanded=True):
            account_type = st.radio(
                "Select your OpenAI account type:",
                ["Free", "Paid"],
                index=0,
                key="account_type_radio",
                disabled=True
            )

        # 2. Model selection (dynamic)
        free_models = ["gpt-3.5-turbo", "gpt-3.5-turbo-0125"]
        paid_models = ["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo", "gpt-3.5-turbo-0125"]
        model_options = free_models if account_type == "Free" else paid_models
        with st.expander("🤖 Model Selection", expanded=True):
            model = st.selectbox(
                "Select ChatGPT model:",
                model_options,
                index=0,
                key="model_selectbox"
            )

        # 3. API key input
        with st.expander("🔑 OpenAI API Key", expanded=True):
            openai_api_key = st.text_input(
                "Paste your OpenAI API key:",
                type="password",
                key="openai_api_key_input"
            )
            if openai_api_key:
                os.environ["OPENAI_API_KEY"] = openai_api_key

        # 4. About section
        with st.expander("ℹ️ About", expanded=False):
            st.markdown(
                """
                **AI-Powered Resume Tailoring**
                
                1. Upload your resume PDF.
                2. The app will parse your resume and build your profile.
                3. The app will automatically search for job matches based on your profile's title.
                4. Select the jobs you want to tailor your resume to.
                5. Click "Tailor My Resume" button.
                6. Download tailored resumes as DOCX files.
                
                **Sidebar Features:**
                - Select your OpenAI account type (Free or Paid). This affects available models and the number of job postings you can search for.
                - Choose your preferred ChatGPT model.
                - Paste your OpenAI API key to enable AI features.
                - For Free accounts, 3 job postings will be searched. For Paid accounts, 10 job postings will be searched.
                """
            )

    num_jobs = 3 if account_type == "Free" else 10
    return {
        "model": model,
        "openai_api_key": openai_api_key,
        "num_jobs": num_jobs
    } 