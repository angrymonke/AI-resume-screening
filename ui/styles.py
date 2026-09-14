"""Theme-aware CSS for Rolevia's recruiter dashboard."""


def inject_styles(dark: bool) -> None:
    import streamlit as st

    colors = {
        "bg": "#0B1020" if dark else "#F7F8FC", "card": "#111827" if dark else "#FFFFFF",
        "elevated": "#172033" if dark else "#FFFFFF", "text": "#F9FAFB" if dark else "#111827",
        "muted": "#9CA3AF" if dark else "#6B7280", "border": "#263247" if dark else "#E5E7EB",
        "primary": "#818CF8" if dark else "#4F46E5", "primary_hover": "#A5B4FC" if dark else "#4338CA",
        "success": "#22C55E" if dark else "#16A34A", "warning": "#F59E0B" if dark else "#D97706",
        "error": "#F87171" if dark else "#DC2626",
    }
    st.markdown(f"""
    <style>
      :root {{ color-scheme: {'dark' if dark else 'light'}; }}
      html, body, [data-testid="stAppViewContainer"] {{ background:{colors['bg']}; color:{colors['text']}; }}
      [data-testid="stHeader"] {{ background:transparent; }}
      [data-testid="stSidebar"] {{ background:{colors['card']}; border-right:1px solid {colors['border']}; }}
      [data-testid="stSidebar"] * {{ color:{colors['text']}; }}
      .block-container {{ max-width:1280px; padding:2rem 2.5rem 4rem; }}
      h1,h2,h3,p,span,label {{ color:{colors['text']}; }}
      .brand {{ font-size:1.35rem; font-weight:800; letter-spacing:-.045em; color:{colors['text']}; }}
      .brand-mark {{ color:{colors['primary']}; margin-right:6px; }}
      .eyebrow {{ font-size:.73rem; font-weight:750; color:{colors['primary']}; text-transform:uppercase; letter-spacing:.09em; margin-bottom:8px; }}
      .page-title {{ font-size:2.25rem; line-height:1.1; font-weight:750; letter-spacing:-.055em; margin:0 0 10px; }}
      .subtle {{ color:{colors['muted']}; font-size:.95rem; line-height:1.55; }}
      .surface {{ background:{colors['card']}; border:1px solid {colors['border']}; border-radius:16px; padding:24px; box-shadow:0 5px 18px rgba(15,23,42,.045); margin-bottom:18px; }}
      .surface:hover,.ranking-card:hover {{ transform:translateY(-2px); border-color:{colors['primary']}; transition:all .18s ease; }}
      .section-title {{ font-size:1.08rem; font-weight:700; letter-spacing:-.025em; margin:0 0 5px; }}
      .kpi {{ background:{colors['card']}; border:1px solid {colors['border']}; border-radius:14px; padding:18px; min-height:105px; }}
      .kpi-label {{ color:{colors['muted']}; font-size:.78rem; font-weight:650; }}
      .kpi-value {{ color:{colors['text']}; font-size:1.75rem; font-weight:780; letter-spacing:-.06em; margin-top:7px; }}
      .ranking-card {{ background:{colors['card']}; border:1px solid {colors['border']}; border-radius:15px; padding:20px; margin:10px 0; transition:all .18s ease; }}
      .rank {{ color:{colors['muted']}; font-size:.78rem; font-weight:700; }}
      .score {{ color:{colors['primary']}; font-size:1.7rem; font-weight:800; letter-spacing:-.06em; text-align:right; }}
      .candidate {{ font-weight:700; margin:10px 0 12px; overflow-wrap:anywhere; }}
      .pill {{ display:inline-block; padding:5px 9px; border-radius:999px; background:{colors['elevated']}; color:{colors['primary']}; font-size:.75rem; font-weight:700; }}
      .score-track {{ height:7px; background:{colors['border']}; border-radius:99px; overflow:hidden; margin:12px 0; }}
      .score-fill {{ height:100%; background:{colors['primary']}; border-radius:99px; }}
      .workflow {{ border-left:2px solid {colors['primary']}; padding:0 0 0 18px; margin:20px 0; }}
      .workflow-item {{ padding:0 0 20px; }}
      .workflow-num {{ color:{colors['primary']}; font-size:.75rem; font-weight:800; }}
      div[data-testid="stTextArea"] textarea, div[data-testid="stFileUploader"] section {{ background:{colors['elevated']} !important; color:{colors['text']} !important; border-color:{colors['border']} !important; border-radius:12px !important; }}
      div[data-testid="stTextArea"] textarea:focus {{ border-color:{colors['primary']} !important; box-shadow:0 0 0 3px {colors['primary']}33 !important; }}
      .stButton>button {{ background:{colors['primary']}; color:white; border:0; border-radius:10px; min-height:44px; font-weight:700; width:100%; }}
      .stButton>button:hover {{ background:{colors['primary_hover']}; color:{'#111827' if dark else 'white'}; }}
      .stButton>button:disabled {{ opacity:.42; }}
      div[data-testid="stDataFrame"] {{ border:1px solid {colors['border']}; border-radius:12px; overflow:hidden; }}
      [data-testid="stAlert"] {{ border-radius:12px; }}
      @media(max-width:700px) {{ .block-container {{ padding:1.2rem 1rem 3rem; }} .page-title {{ font-size:1.8rem; }} }}
    </style>
    """, unsafe_allow_html=True)
