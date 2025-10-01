import os
import json
import streamlit as st
from dotenv import load_dotenv
from file_tools.file_loader import detect_and_extract
from crew import run_pipeline
from utils import txt_to_docx_bytes
import plotly.graph_objects as go
import plotly.express as px
import re

# Load environment variables
load_dotenv()

# --------------------------------------------
# Helper functions
# --------------------------------------------
def safe_parse_json(text: str):
    """
    Robustly parse JSON from a string, handling single quotes and trailing commas.
    """
    try:
        text = text.replace("'", '"')
        text = re.sub(r",\s*([}\]])", r"\1", text)
        return json.loads(text)
    except Exception:
        return None

def generate_donut_chart(score, title="Overall ATS Score"):
    """
    Creates a donut chart for the overall ATS score.
    """
    fig = go.Figure(data=[go.Pie(
        values=[score, 100 - score],
        labels=["Match", "Remaining"],
        hole=0.6,
        marker_colors=["#2E86AB", "#E8E8E8"],
        textinfo='label+percent'
    )])
    fig.update_layout(
        title_text=f"{title}: {score}%",
        annotations=[dict(text=f"{score}%", x=0.5, y=0.5, font_size=24, showarrow=False)],
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        height=350
    )
    return fig

def generate_radar_chart(breakdown: dict, title="Section Breakdown"):
    """
    Creates a radar chart from a section-wise breakdown.
    """
    categories = list(breakdown.keys())
    values = list(breakdown.values())
    categories += categories[:1]
    values += values[:1]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        line_color="#2E86AB",
        name="Section Scores"
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, max(values)+1])),
        showlegend=False,
        title=title,
        height=400,
        margin=dict(t=50, b=20, l=20, r=20)
    )
    return fig

def display_quick_wins(quick_wins: list):
    st.subheader("💡 Quick Wins")
    for i, tip in enumerate(quick_wins, 1):
        st.markdown(f"**{i}.** {tip}")

def display_missing_keywords(keywords: list):
    st.subheader("🔑 Missing Keywords")
    st.markdown(", ".join([f"`{kw}`" for kw in keywords]))

# --------------------------------------------
# Page Config
# --------------------------------------------
st.set_page_config(
    page_title="ATS Resume Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------
# Sidebar Navigation
# --------------------------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2922/2922510.png", width=120)
st.sidebar.markdown(
    """
    <div style="
        text-align: center; 
        padding: 10px; 
        border-radius: 10px; 
        background: linear-gradient(90deg, #2E86AB, #5DADE2);
        color: white;
        font-family: 'Arial', sans-serif;
    ">
        <h2 style="margin: 5px;">Shivam Kumar</h2>
        <p style="margin: 0; font-size: 14px;">ATS Resume Analyzer</p>
    </div>
    """,
    unsafe_allow_html=True
)

page = st.sidebar.radio("Navigation", ["Upload Resume", "JD Matching", "Analytics", "About"])

# --------------------------------------------
# --------------------------------------------
# Upload Resume Page (Professional SaaS Style)
# --------------------------------------------
if page == "Upload Resume":
    st.markdown("<h1 style='text-align:center; color:#2E86AB;'>📄 Upload Your Resume</h1>", unsafe_allow_html=True)
    st.markdown(
        """
        <p style='text-align:center; color:#555; font-size:16px;'>
        Upload your resume in <b>PDF or DOCX</b> format.<br>
        Extract key sections like <b>Skills, Experience, Education</b> and get a comprehensive ATS score.
        </p>
        """,
        unsafe_allow_html=True
    )

    # ---------------- Inputs Card ----------------
    with st.container():
        st.markdown(
            "<div style='padding:15px; border-radius:10px; background-color:#f9f9f9; box-shadow: 0px 3px 8px rgba(0,0,0,0.05);'>"
            "<h3 style='color:#2E86AB;'>Upload & Job Details</h3></div>",
            unsafe_allow_html=True
        )
        col1, col2 = st.columns([2, 1])
        with col1:
            resume_file = st.file_uploader(
                "Upload Resume", 
                type=["pdf", "docx"], 
                label_visibility="visible"
            )
        with col2:
            job_title = st.text_input("🎯 Target Job Title", placeholder="e.g., Data Scientist")
            job_desc = st.text_area("📑 Job Description", placeholder="Paste Job Description here...", height=200)

        run_btn = st.button("🚀 Analyze Resume", use_container_width=True, 
                            help="Click to parse and evaluate your resume against the job description")

    # ---------------- Run Analysis ----------------
    if run_btn:
        if resume_file is None or not job_title or not job_desc.strip():
            st.warning("⚠️ Please upload a resume and provide a job title + job description.")
        else:
            with st.spinner("🤖 Parsing resume and evaluating..."):
                # ---- PLACEHOLDER: Replace with actual parsing & scoring ----
                try:
                    raw_text = resume_file.read().decode("utf-8", errors="ignore")  # dummy
                except Exception:
                    raw_text = "Dummy text"

                # Simulated evaluation JSON
                evaluation = {
                    "overall_score": 78,
                    "breakdown": {
                        "keywords": 4,
                        "structure": 3,
                        "metrics": 4,
                        "verbs": 3,
                        "format": 4
                    },
                    "quick_wins": [
                        "Add more action verbs in experience section.",
                        "Include specific metrics to quantify achievements.",
                        "Ensure consistent formatting throughout."
                    ],
                    "missing_keywords": ["Python", "Machine Learning", "NLP"]
                }

            # ---------------- Success Notification ----------------
            st.success("✅ Resume analyzed successfully!", icon="✅")

            # ---------------- Metrics Cards ----------------
            st.markdown("<h3 style='color:#2E86AB;'>Summary Metrics</h3>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Overall ATS Score", value=f"{evaluation['overall_score']} / 100")
            with col2:
                st.metric(label="Keywords Matched", value=f"{evaluation['breakdown']['keywords']} / 5")
            with col3:
                st.metric(label="Missing Keywords", value=f"{len(evaluation['missing_keywords'])}")

            # ---------------- Progress Bar ----------------
            st.markdown("<h4 style='color:#2E86AB;'>Match Progress</h4>", unsafe_allow_html=True)
            st.progress(evaluation["overall_score"]/100)

            # ---------------- Donut Chart ----------------
            st.markdown("<h4 style='color:#2E86AB;'>Visual ATS Score</h4>", unsafe_allow_html=True)
            st.plotly_chart(generate_donut_chart(evaluation["overall_score"]), use_container_width=True)

            # ---------------- Quick Wins ----------------
            st.markdown("<h4 style='color:#2E86AB;'>💡 Quick Wins & Recommendations</h4>", unsafe_allow_html=True)
            for i, tip in enumerate(evaluation["quick_wins"], 1):
                st.markdown(f"<div style='padding:10px; border-left: 4px solid #2E86AB; background:#f7f9fc; margin-bottom:8px;'>{i}. {tip}</div>", unsafe_allow_html=True)

            # ---------------- Missing Keywords ----------------
            st.markdown("<h4 style='color:#2E86AB;'>🔑 Missing Keywords</h4>", unsafe_allow_html=True)
            st.markdown(
                "<div style='display:flex; flex-wrap:wrap; gap:8px;'>"
                + "".join([f"<span style='padding:5px 10px; background:#d0e7ff; border-radius:5px;'>{kw}</span>" for kw in evaluation["missing_keywords"]])
                + "</div>",
                unsafe_allow_html=True
            )

# JD Matching Page
# --------------------------------------------
elif page == "JD Matching":
    st.title("📑 Job Description Matching")
    st.markdown("Compare your resume against job description and visualize keyword matches, missing skills, and recommendations.")

    # ---- PLACEHOLDER: Replace with actual parsing & scoring ----
    sample_keywords = ["Python", "Machine Learning", "Data Analysis", "NLP", "SQL"]
    frequencies = [5, 4, 3, 2, 1]
    df_keywords = {"Keyword": sample_keywords, "Frequency": frequencies}

    fig_bar = px.bar(df_keywords, x="Keyword", y="Frequency", color="Frequency",
                     text="Frequency", color_continuous_scale="Blues")
    fig_bar.update_layout(title="Keyword Frequency in Resume", height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

# --------------------------------------------
# Analytics Page
# --------------------------------------------
elif page == "Analytics":
    st.title("📊 Resume Analytics Dashboard")
    st.markdown("Visualize your resume performance and ATS score breakdown.")

    # ---- PLACEHOLDER: Replace with actual evaluation JSON ----
    parsed = {
        "overall_score": 78,
        "breakdown": {
            "keywords": 4,
            "structure": 3,
            "metrics": 4,
            "verbs": 3,
            "format": 4
        },
        "quick_wins": [
            "Add more action verbs in experience section.",
            "Include metrics in achievements.",
            "Ensure consistent formatting."
        ],
        "missing_keywords": ["Python", "Machine Learning", "NLP"]
    }

    st.plotly_chart(generate_donut_chart(parsed["overall_score"]), use_container_width=True)
    st.plotly_chart(generate_radar_chart(parsed["breakdown"]), use_container_width=True)
    display_quick_wins(parsed["quick_wins"])
    display_missing_keywords(parsed["missing_keywords"])

# --------------------------------------------
# About Page
# --------------------------------------------
else:
    st.title("ℹ️ About This App")
    st.markdown(
        """
        This **ATS Resume Analyzer** is built by **Shivam Kumar** using **Streamlit, Plotly, and OpenAI**.  
        Features:
        - Parse PDF/DOCX resumes
        - Evaluate against job descriptions
        - Generate ATS-style scoring
        - Interactive charts and dashboard
        - Quick wins and missing keyword suggestions

        **Future Enhancements:**
        - Multi-resume batch analysis
        - Downloadable ATS reports
        - Keyword heatmaps and radar charts
        """
    )

# --------------------------------------------
# Footer
# --------------------------------------------
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:gray; font-size:0.9em;'>"
    "Built with ❤️ by <b>Shivam Kumar</b> | Powered by CrewAI & OpenAI"
    "</div>",
    unsafe_allow_html=True
)
