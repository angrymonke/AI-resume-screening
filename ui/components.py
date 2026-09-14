"""Reusable presentation components for Rolevia."""

import html

import streamlit as st


def header(section: str) -> None:
    left, right = st.columns([5, 1])
    with left:
        st.markdown(f'<div class="brand"><span class="brand-mark">◈</span>Rolevia</div><div class="subtle">{html.escape(section)}</div>', unsafe_allow_html=True)
    with right:
        dark = st.toggle("☾ Dark", value=st.session_state.get("dark_mode", False), key="theme_toggle")
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
