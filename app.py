"""Rolevia — traditional NLP resume similarity screening."""

import streamlit as st
import altair as alt
import pandas as pd

from nlp_utils import rank_resumes
from resume_parser import extract_resume_text
from ui.components import candidate_analysis, header, kpi, page_intro, ranking_card, ranking_table
from ui.styles import inject_styles

st.set_page_config(page_title="Rolevia | Resume Screening", page_icon="◈", layout="wide", initial_sidebar_state="expanded")
for key, value in {"dark_mode": False, "page": "New Screening", "results": [], "job_description": ""}.items():
    st.session_state.setdefault(key, value)
inject_styles(st.session_state.dark_mode, st.session_state.page)

with st.sidebar:
    st.markdown('<div class="brand"><span class="brand-mark">◈</span>Rolevia</div><div class="subtle" style="margin-bottom:22px">AI Resume Screening</div>', unsafe_allow_html=True)
    nav_items = [("New Screening", "+", "nav_new_screening"), ("Results", "▦", "nav_results"), ("How It Works", "◎", "nav_how_it_works"), ("About", "i", "nav_about")]
    for label, icon, key in nav_items:
        if st.button(f"{icon}  {label}", key=key):
            st.session_state.page = label
            st.rerun()
    st.markdown('<div style="position:fixed;bottom:24px" class="subtle">AI Resume Screening<br>v1.0</div>', unsafe_allow_html=True)

page = st.session_state.page
header(page)

if page == "New Screening":
    page_intro("New screening", "Find the best candidates faster.", "Match resumes against job requirements using NLP-based similarity analysis.")
    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="surface"><div class="section-title">Job Description</div><div class="subtle">Paste the job requirements you want to screen candidates against.</div></div>', unsafe_allow_html=True)
    job_description = st.text_area("Job description", value=st.session_state.job_description, height=210, placeholder="Example: Looking for a Python developer with data analysis, SQL, machine learning, and communication skills.", label_visibility="collapsed")
    st.session_state.job_description = job_description
    st.markdown('<div class="surface"><div class="section-title">Upload Resumes</div><div class="subtle">Upload multiple PDF resumes to compare candidates against the job description.</div></div>', unsafe_allow_html=True)
    uploads = st.file_uploader("Drop PDF resumes here", type=["pdf"], accept_multiple_files=True, help="PDF files only. Each file is processed independently.")
    if uploads:
        st.caption("Selected files: " + "  •  ".join(f"✓ {f.name}" for f in uploads))
    if st.button("Analyze & Rank Resumes", disabled=not (job_description.strip() and uploads), key="analyze"):
        extracted = []
        with st.status("Analyzing candidates", expanded=True) as status:
            st.write("✓ Extracting resume text")
            for file in uploads:
                extracted.append(extract_resume_text(file))
            st.write("✓ Processing job description")
            st.write("● Calculating TF-IDF cosine similarity")
            results = rank_resumes(job_description, extracted)
            st.write("✓ Ranking candidates")
            status.update(label="Analysis complete", state="complete")
        failed = [x for x in extracted if x["status"] != "Ready"]
        if failed:
            st.warning("Some files could not be analyzed: " + ", ".join(f"{x['filename']} ({x['status']})" for x in failed))
        if not results:
            st.error("No resumes with extractable text could be matched. Try text-based PDF resumes.")
        else:
            st.session_state.results = results
            st.session_state.page = "Results"
            st.rerun()

elif page == "Results":
    results = st.session_state.results
    page_intro("Screening results", "Candidates, ranked clearly.", "Candidates are ranked by textual similarity to the job description—not candidate quality or hiring probability.")
    if not results:
        st.markdown('<div class="surface" style="margin-top:24px"><div class="section-title">No screening results yet</div><div class="subtle">Run a screening to see ranked candidates here.</div></div>', unsafe_allow_html=True)
        if st.button("Start New Screening", key="start_screening"):
            st.session_state.page = "New Screening"; st.rerun()
    else:
        average = sum(x["match_score"] for x in results) / len(results)
        strong = sum(x["match_score"] >= 80 for x in results)
        cols = st.columns(4)
        for column, label, value in zip(cols, ["Candidates Screened", "Top Match", "Average Match", "Strong Matches"], [str(len(results)), f"{results[0]['match_score']:.1f}%", f"{average:.1f}%", str(strong)]):
            with column: kpi(label, value)
        st.markdown('<div style="height:20px"></div><div class="section-title">Candidate Ranking</div><div class="subtle">Inspect each result for the source text and similarity details.</div>', unsafe_allow_html=True)
        for item in results:
            left, right = st.columns([5, 1])
            with left: ranking_card(item)
            with right:
                st.markdown('<div style="height:42px"></div>', unsafe_allow_html=True)
                if st.button("View Analysis →", key=f"view_{item['rank']}"):
                    st.session_state.selected_candidate = item["rank"]
                    st.rerun()
            if st.session_state.get("selected_candidate") == item["rank"]:
                candidate_analysis(item)
        st.markdown('<div style="height:18px"></div><div class="section-title">Ranking Table</div><div class="subtle">A quick comparison of every screened candidate.</div>', unsafe_allow_html=True)
        ranking_table(results)
        st.markdown('<div style="height:18px"></div><div class="section-title">Match Score Comparison</div><div class="subtle">Higher bars indicate stronger textual similarity to the job description.</div>', unsafe_allow_html=True)
        chart_data = pd.DataFrame({"Candidate": [item["filename"] for item in results], "Match score": [item["match_score"] for item in results]})
        chart_color = "#A5B4FC" if st.session_state.dark_mode else "#4F46E5"
        axis_color = "#CBD5E1" if st.session_state.dark_mode else "#475569"
        chart = alt.Chart(chart_data).mark_bar(cornerRadiusTopRight=6, cornerRadiusBottomRight=6, color=chart_color).encode(
            x=alt.X("Match score:Q", scale=alt.Scale(domain=[0, 100]), title="Match score (%)", axis=alt.Axis(labelColor=axis_color, titleColor=axis_color, gridColor="#334155" if st.session_state.dark_mode else "#E2E8F0")),
            y=alt.Y("Candidate:N", sort="-x", title=None, axis=alt.Axis(labelColor=axis_color, labelLimit=230)),
            tooltip=[alt.Tooltip("Candidate:N", title="Candidate"), alt.Tooltip("Match score:Q", title="Match score", format=".1f")],
        ).properties(height=max(180, 46 * len(results)), padding={"left": 6, "right": 12, "top": 8, "bottom": 8}).configure_view(stroke=None).configure(background="transparent")
        st.markdown('<div class="chart-shell">', unsafe_allow_html=True)
        st.altair_chart(chart, width="stretch", key="match_score_chart")
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "How It Works":
    page_intro("Methodology", "Simple NLP. Clear ranking.", "Rolevia uses one shared TF-IDF vocabulary to compare every resume fairly against the same job description.")
    steps = [("01", "Add a job description", "Describe the requirements, responsibilities, and relevant skills."), ("02", "Upload resumes", "Choose one or more text-based PDF resumes."), ("03", "Extract & normalize text", "Rolevia reads every PDF page and removes punctuation and whitespace noise."), ("04", "Build TF-IDF vectors", "Job and resume text are represented in one shared vector space."), ("05", "Compare and rank", "Cosine similarity becomes a display score and a descending candidate ranking.")]
    st.markdown('<div class="surface"><div class="workflow">' + ''.join(f'<div class="workflow-item"><div class="workflow-num">{n}</div><div class="section-title">{t}</div><div class="subtle">{d}</div></div>' for n,t,d in steps) + '</div></div>', unsafe_allow_html=True)
    st.info("Job Description + Resumes → Text Extraction → NLP Processing → TF-IDF → Cosine Similarity → Match Score → Ranking")

else:
    page_intro("About Rolevia", "Assistive resume screening, explained.", "Rolevia is an academic project demonstrating traditional NLP-based document similarity in a recruiter-focused interface.")
    st.markdown('<div class="surface"><div class="section-title">Technology</div><div class="subtle">Python · Streamlit · PyMuPDF · Pandas · Scikit-learn · TF-IDF · Cosine Similarity</div><br><div class="section-title">Responsible use</div><div class="subtle">This tool provides similarity-based ranking and should be used as an assistive screening tool rather than an automated hiring decision-maker.</div></div>', unsafe_allow_html=True)
