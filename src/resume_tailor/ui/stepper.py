import streamlit as st
from resume_tailor.config import STEP_LABELS

def render_stepper(current_step: int):
    stepper_md = " → ".join([
        f"<span style='color: {'#4F8BF9' if i == current_step else '#888'}'>{label}</span>"
        for i, label in enumerate(STEP_LABELS)
    ])
    st.markdown(f"""
    <div style='font-size:1.1em; margin-bottom: 1.5em;'>{stepper_md}</div>
    """, unsafe_allow_html=True)
