import streamlit as st
import tempfile
import pypandoc
from resume_tailor.tools.pdf_extractor import extract_text_and_style, extract_links_with_text_first_page

def handle_file_upload():
    """
    Handles the upload of a PDF resume file via Streamlit's file uploader.
    Stores the file path in st.session_state["resume_path"].
    """
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF)",
        type="pdf",
        disabled="resume_path" in st.session_state
    )
    if uploaded_file and "resume_path" not in st.session_state:
        if uploaded_file.type != "application/pdf":
            st.error("❌ Only PDF files are supported. Please upload your resume as a PDF.")
            st.stop()
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                st.session_state["resume_path"] = tmp.name
            st.success("PDF uploaded successfully!")
        except Exception as e:
            st.error(f"Failed to save uploaded file: {e}")
            st.stop()

def parse_resume():
    """
    Parses the uploaded PDF resume and stores the extracted text, styles, and links in session state.
    Only runs if 'resume_path' is present and 'parsed_resume' is not already set.
    """
    if "resume_path" in st.session_state and "parsed_resume" not in st.session_state:
        with st.spinner("Parsing resume..."):
            try:
                parsed = extract_text_and_style(st.session_state["resume_path"])
                st.session_state["parsed_resume"] = parsed
                st.session_state["resume_styles"] = parsed["styles"]
            except Exception as e:
                st.error(f"Failed to parse PDF: {e}")
                st.stop()
            # Extract links from first page
            try:
                links = extract_links_with_text_first_page(st.session_state["resume_path"])
                st.session_state["resume_links"] = links
            except Exception as e:
                st.error(f"Failed to extract links from PDF: {e}")
                st.stop()
            st.success("Resume parsed successfully!")

def save_docx_with_styles(markdown_text, output_path):
    """
    Converts markdown text to a DOCX file using pypandoc and saves it to output_path.
    """
    pypandoc.convert_text(
        markdown_text,
        'docx',
        format='md',
        outputfile=output_path
    )