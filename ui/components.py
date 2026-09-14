"""Reusable presentation components for Rolevia."""

import html

import streamlit as st


def header(section: str) -> None:
    left, right = st.columns([5, 1])
    with left:
        st.markdown(f'<div class="brand"><span class="brand-mark">◈</span>Rolevia</div><div class="subtle">{html.escape(section)}</div>', unsafe_allow_html=True)
    with right:
        is_dark = st.session_state.get("dark_mode", False)
        theme_label = "Dark" if is_dark else "Light"
        dark = st.toggle(theme_label, value=is_dark, key="theme_toggle")
        if dark != st.session_state.get("dark_mode", False):
            st.session_state.dark_mode = dark
            st.rerun()


def page_intro(eyebrow: str, title: str, description: str) -> None:
    st.markdown(f'<div class="eyebrow">{html.escape(eyebrow)}</div><h1 class="page-title">{html.escape(title)}</h1><div class="subtle">{html.escape(description)}</div>', unsafe_allow_html=True)


def kpi(label: str, value: str) -> None:
    st.markdown(f'<div class="kpi"><div class="kpi-label">{html.escape(label)}</div><div class="kpi-value">{html.escape(value)}</div></div>', unsafe_allow_html=True)


def ranking_card(item: dict) -> None:
    filename = html.escape(item["filename"])
    st.markdown(f'''<div class="ranking-card"><div style="display:flex;justify-content:space-between;align-items:start"><div class="rank">RANK #{item['rank']}</div><div class="score">{item['match_score']:.1f}%</div></div><div class="candidate">📄 {filename}</div><div class="score-track"><div class="score-fill" style="width:{item['match_score']}%"></div></div><span class="pill">{html.escape(item['match_category'])}</span></div>''', unsafe_allow_html=True)


def ranking_table(results: list[dict]) -> None:
    """Render a compact theme-aware ranking table."""
    rows = []
    for item in results:
        rows.append(
            f"<tr><td><span class='table-rank'>#{item['rank']}</span></td>"
            f"<td><span class='table-candidate'>{html.escape(item['filename'])}</span></td>"
            f"<td><strong class='table-score'>{item['match_score']:.1f}%</strong></td>"
            f"<td>{item['cosine_similarity']:.4f}</td>"
            f"<td><span class='table-pill'>{html.escape(item['match_category'])}</span></td></tr>"
        )
    st.markdown(
        "<div class='results-table-wrap'><table class='results-table'><thead><tr>"
        "<th>Rank</th><th>Candidate</th><th>Match score</th><th>Cosine similarity</th><th>Category</th>"
        "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>",
        unsafe_allow_html=True,
    )


def candidate_analysis(item: dict) -> None:
    """Show the selected candidate's calculation details and extracted text."""
    st.markdown('<div class="surface" style="margin-top:20px">', unsafe_allow_html=True)
    st.markdown(f"<div class='section-title'>Candidate Analysis</div><div class='subtle'>Showing details for <strong>{html.escape(item['filename'])}</strong></div>", unsafe_allow_html=True)
    a, b, c = st.columns(3)
    with a:
        kpi("Match Score", f"{item['match_score']:.1f}%")
    with b:
        kpi("Cosine Similarity", f"{item['cosine_similarity']:.4f}")
    with c:
        kpi("Category", item['match_category'])
    coverage = item.get("keyword_coverage", 0.0)
    matched = item.get("matched_keywords", [])
    missing = item.get("missing_keywords", [])
    st.markdown(
        f"<div class='analysis-grid'><div class='analysis-block'><div class='analysis-label'>Keyword coverage</div><div class='analysis-value'>{coverage:.1f}%</div><div class='subtle'>Relevant terms found in the resume</div></div>"
        f"<div class='analysis-block'><div class='analysis-label'>Matched terms</div><div class='analysis-value'>{len(matched)}</div><div class='subtle'>Of {len(matched) + len(missing)} job-description terms reviewed</div></div></div>",
        unsafe_allow_html=True,
    )
    matched_html = "".join(f"<span class='keyword-chip keyword-match'>{html.escape(word)}</span>" for word in matched) or "<span class='subtle'>No strong keyword overlap detected.</span>"
    missing_html = "".join(f"<span class='keyword-chip keyword-missing'>{html.escape(word)}</span>" for word in missing) or "<span class='subtle'>No major keyword gaps detected.</span>"
    st.markdown(
        f"<div class='analysis-columns'><div><div class='analysis-label'>Detected strengths</div><div class='keyword-list'>{matched_html}</div></div><div><div class='analysis-label'>Potential gaps to review</div><div class='keyword-list'>{missing_html}</div></div></div>",
        unsafe_allow_html=True,
    )
    st.markdown("<br><div class='subtle'>Match score represents the cosine similarity between the TF-IDF representation of the job description and this resume.</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title' style='margin-top:20px'>Extracted Resume Text</div>", unsafe_allow_html=True)
    st.markdown(f"<pre class='resume-text'>{html.escape(item['extracted_text'])}</pre>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
