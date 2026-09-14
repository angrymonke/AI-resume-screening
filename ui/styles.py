"""Theme-aware CSS for Rolevia's recruiter dashboard."""


def inject_styles(dark: bool, active_page: str) -> None:
    import streamlit as st

    colors = {
        "bg": "#0B1020" if dark else "#F7F8FC", "card": "#111827" if dark else "#FFFFFF",
        "elevated": "#172033" if dark else "#FFFFFF", "text": "#F9FAFB" if dark else "#111827",
        "muted": "#9CA3AF" if dark else "#6B7280", "border": "#263247" if dark else "#E5E7EB",
        "primary": "#818CF8" if dark else "#4F46E5", "primary_hover": "#A5B4FC" if dark else "#4338CA",
        "success": "#22C55E" if dark else "#16A34A", "warning": "#F59E0B" if dark else "#D97706",
        "error": "#F87171" if dark else "#DC2626",
    }
    nav_keys = {
        "New Screening": "nav_new_screening",
        "Results": "nav_results",
        "How It Works": "nav_how_it_works",
        "About": "nav_about",
    }
    active_nav = nav_keys.get(active_page, "nav_new_screening")
    st.markdown(f"""
    <style>
      :root {{ color-scheme: {'dark' if dark else 'light'}; }}
      html, body, [data-testid="stAppViewContainer"] {{ background:{colors['bg']}; color:{colors['text']}; }}
      [data-testid="stHeader"] {{ background:transparent; }}
      [data-testid="stSidebar"] {{ background:{colors['card']}; border-right:1px solid {colors['border']}; }}
      [data-testid="stSidebar"] {{ color:{colors['text']}; }}
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
      [data-testid="stFileUploader"] button {{ background:{colors['primary']} !important; color:#fff !important; border:0 !important; border-radius:9px !important; font-weight:700 !important; }}
      [data-testid="stFileUploader"] button:hover {{ background:{colors['primary_hover']} !important; color:#fff !important; }}
      .stButton > button {{ background:{colors['elevated']} !important; color:{colors['text']} !important; border:1px solid {colors['border']} !important; border-radius:10px !important; min-height:42px; font-weight:650 !important; width:100%; }}
      .stButton > button:hover {{ background:{colors['border']} !important; color:{colors['text']} !important; border-color:{colors['primary']} !important; }}
      .st-key-analyze button, .st-key-start_screening button {{ background:{colors['primary']} !important; color:#fff !important; border:0 !important; border-radius:10px !important; min-height:44px; font-weight:700 !important; width:100%; }}
      .st-key-analyze button:hover, .st-key-start_screening button:hover {{ background:{colors['primary_hover']} !important; color:#fff !important; }}
      .st-key-analyze button:disabled {{ opacity:.42; }}
      [class*="st-key-view_"] button {{ background:{colors['primary']} !important; color:#fff !important; border:0 !important; min-height:38px; font-size:.82rem; }}
      [class*="st-key-view_"] button:hover {{ background:{colors['primary_hover']} !important; color:#fff !important; }}
      .st-key-nav_new_screening button, .st-key-nav_results button, .st-key-nav_how_it_works button, .st-key-nav_about button {{ background:transparent !important; color:{colors['muted']} !important; border:1px solid transparent !important; border-radius:9px !important; min-height:40px; font-weight:650 !important; justify-content:flex-start !important; padding-left:12px !important; }}
      .st-key-nav_new_screening button:hover, .st-key-nav_results button:hover, .st-key-nav_how_it_works button:hover, .st-key-nav_about button:hover {{ background:{colors['elevated']} !important; color:{colors['text']} !important; border-color:{colors['border']} !important; }}
      .st-key-{active_nav} button {{ background:{colors['primary']} !important; color:#fff !important; border-color:{colors['primary']} !important; }}
      .st-key-theme_toggle {{ background:{colors['elevated']} !important; border:1px solid {colors['border']} !important; border-radius:10px !important; padding:4px 10px 3px !important; min-width:104px; box-shadow:0 3px 10px rgba(15,23,42,.08); }}
      .st-key-theme_toggle [data-testid="stWidgetLabel"] {{ margin-bottom:0 !important; }}
      .st-key-theme_toggle [data-testid="stWidgetLabel"] p {{ color:{colors['text']} !important; font-weight:750 !important; white-space:nowrap; font-size:.84rem !important; }}
      .st-key-theme_toggle [role="switch"] {{ accent-color:{colors['primary']} !important; }}
      .results-table-wrap {{ overflow-x:auto; border:1px solid {colors['border']}; border-radius:14px; background:{colors['card']}; box-shadow:0 5px 18px rgba(15,23,42,.045); }}
      .results-table {{ border-collapse:collapse; width:100%; min-width:720px; color:{colors['text']}; font-size:.88rem; }}
      .results-table th {{ background:{colors['elevated']}; color:{colors['muted']}; font-size:.72rem; text-transform:uppercase; letter-spacing:.06em; font-weight:750; text-align:left; padding:14px 16px; border-bottom:1px solid {colors['border']}; white-space:nowrap; }}
      .results-table td {{ padding:15px 16px; border-bottom:1px solid {colors['border']}; vertical-align:middle; }}
      .results-table tbody tr:last-child td {{ border-bottom:0; }}
      .results-table tbody tr:hover {{ background:{colors['elevated']}; }}
      .table-rank {{ color:{colors['muted']}; font-weight:750; }}
      .table-candidate {{ font-weight:700; overflow-wrap:anywhere; }}
      .table-score {{ color:{colors['primary']}; font-size:1rem; }}
      .table-pill {{ display:inline-block; border:1px solid {colors['border']}; background:{colors['elevated']}; color:{colors['primary']}; border-radius:999px; padding:5px 10px; font-size:.74rem; font-weight:700; white-space:nowrap; }}
      .chart-shell {{ border:1px solid {colors['border']}; border-radius:14px; background:{colors['card']}; padding:12px 14px 4px; box-shadow:0 5px 18px rgba(15,23,42,.045); }}
      .analysis-grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:12px; margin-top:18px; }}
      .analysis-block {{ background:{colors['elevated']}; border:1px solid {colors['border']}; border-radius:12px; padding:14px 16px; }}
      .analysis-label {{ color:{colors['muted']}; font-size:.72rem; font-weight:750; text-transform:uppercase; letter-spacing:.06em; margin-bottom:6px; }}
      .analysis-value {{ color:{colors['primary']}; font-size:1.5rem; font-weight:800; letter-spacing:-.04em; }}
      .analysis-columns {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:20px; margin-top:20px; }}
      .keyword-list {{ display:flex; flex-wrap:wrap; gap:7px; margin-top:9px; }}
      .keyword-chip {{ display:inline-block; border-radius:999px; padding:5px 9px; font-size:.74rem; font-weight:700; }}
      .keyword-match {{ background:{colors['primary']}22; color:{colors['primary']}; border:1px solid {colors['primary']}55; }}
      .keyword-missing {{ background:{colors['elevated']}; color:{colors['muted']}; border:1px solid {colors['border']}; }}
      .resume-text {{ background:{colors['elevated']}; color:{colors['text']} !important; border:1px solid {colors['border']}; border-radius:12px; padding:18px; min-height:220px; max-height:380px; overflow:auto; white-space:pre-wrap; word-break:break-word; font-family:ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace; font-size:.84rem; line-height:1.65; margin:10px 0 0; }}
      /* Streamlit's chart toolbar must follow the active theme too. */
      /* Hide the floating Streamlit element toolbar: it otherwise renders as an opaque black pill over charts. */
      [data-testid="stElementToolbar"] {{ display:none !important; }}
      [data-testid="stElementToolbar"] > div {{ background:{colors['card']} !important; color:{colors['muted']} !important; border:1px solid {colors['border']} !important; border-radius:9px !important; box-shadow:0 4px 12px rgba(15,23,42,.12) !important; }}
      [data-testid="stElementToolbar"] button, [data-testid="stElementToolbar"] svg {{ color:{colors['text']} !important; fill:{colors['text']} !important; }}
      [data-testid="stElementToolbar"] button:hover {{ background:{colors['elevated']} !important; color:{colors['primary']} !important; }}
      .vega-embed .vega-actions {{ background:{colors['card']} !important; border:1px solid {colors['border']} !important; border-radius:9px !important; padding:4px !important; }}
      .vega-embed .vega-actions a {{ color:{colors['text']} !important; background:transparent !important; }}
      .vega-embed .vega-actions a:hover {{ color:{colors['primary']} !important; background:{colors['elevated']} !important; }}
      [data-testid="stAlert"] {{ border-radius:12px; }}
      @media(max-width:700px) {{ .block-container {{ padding:1.2rem 1rem 3rem; }} .page-title {{ font-size:1.8rem; }} .analysis-grid,.analysis-columns {{ grid-template-columns:1fr; }} }}
    </style>
    """, unsafe_allow_html=True)
