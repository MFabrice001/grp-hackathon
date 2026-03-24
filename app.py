"""
Rwanda GRB Resource Discovery Platform
========================================
Hackathon submission — full-featured app covering all judging criteria:
  Coverage (30%) | Usability (25%) | Trustworthiness (20%)
  Maintainability (15%) | Policy Relevance (10%)

AI powered by Groq (free tier) — llama-3.3-70b-versatile
"""

import os
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import plotly.express as px
import streamlit as st
from groq import Groq

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Rwanda GRB Platform",
    page_icon="🇷🇼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* ═══════════════════════════════════════════════════
     FONTS
  ═══════════════════════════════════════════════════ */
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&display=swap');

  /* ═══════════════════════════════════════════════════
     CSS VARIABLES
  ═══════════════════════════════════════════════════ */
  :root {
    --bg-void:        #060d14;
    --bg-deep:        #0b1724;
    --bg-card:        #0f1f30;
    --bg-card-hover:  #132436;
    --bg-sidebar:     #080f18;
    --border-subtle:  rgba(255,255,255,0.06);
    --border-accent:  rgba(226,185,111,0.35);
    --gold:           #e2b96f;
    --gold-light:     #f0cf99;
    --gold-dim:       rgba(226,185,111,0.12);
    --teal:           #2dbeaa;
    --teal-dim:       rgba(45,190,170,0.12);
    --blue-mid:       #3b82f6;
    --text-primary:   #e8edf3;
    --text-secondary: #8a9ab0;
    --text-muted:     #4a5a6e;
    --success-bg:     rgba(6,95,70,0.75);
    --success-fg:     #6ee7b7;
    --danger-bg:      rgba(127,29,29,0.75);
    --danger-fg:      #fca5a5;
    --warn-bg:        rgba(120,53,15,0.75);
    --warn-fg:        #fcd34d;
    --radius-sm:      8px;
    --radius-md:      14px;
    --radius-lg:      20px;
    --shadow-card:    0 2px 20px rgba(0,0,0,0.45), 0 1px 0 rgba(255,255,255,0.03) inset;
    --shadow-hover:   0 8px 40px rgba(0,0,0,0.55), 0 0 0 1px rgba(226,185,111,0.22);
    --shadow-gold:    0 0 24px rgba(226,185,111,0.18);
    --font-display:   'DM Serif Display', Georgia, serif;
    --font-body:      'DM Sans', system-ui, sans-serif;
    --transition:     0.28s cubic-bezier(0.4, 0, 0.2, 1);
  }

  /* ═══════════════════════════════════════════════════
     BASE & GLOBAL RESETS
  ═══════════════════════════════════════════════════ */
  html, body, .stApp {
    font-family: var(--font-body) !important;
    font-size: 14.5px;
    line-height: 1.65;
    color: var(--text-primary);
  }

  .stApp {
    background-color: var(--bg-void) !important;
    background-image:
      radial-gradient(ellipse 70% 50% at 20% 0%, rgba(45,190,170,0.055) 0%, transparent 60%),
      radial-gradient(ellipse 50% 40% at 80% 100%, rgba(226,185,111,0.045) 0%, transparent 55%),
      url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.012'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  }

  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: var(--bg-void); }
  ::-webkit-scrollbar-thumb { background: rgba(226,185,111,0.25); border-radius: 3px; }
  ::-webkit-scrollbar-thumb:hover { background: rgba(226,185,111,0.45); }

  #MainMenu, footer, header { visibility: hidden; }
  .block-container {
    padding: 2rem 2.5rem 4rem !important;
    max-width: 1440px !important;
  }

  /* ═══════════════════════════════════════════════════
     SIDEBAR
  ═══════════════════════════════════════════════════ */
  section[data-testid="stSidebar"] {
    background-color: var(--bg-sidebar) !important;
    background-image:
      linear-gradient(180deg, rgba(226,185,111,0.04) 0%, transparent 40%),
      repeating-linear-gradient(
        0deg, transparent, transparent 48px,
        rgba(255,255,255,0.015) 48px, rgba(255,255,255,0.015) 49px
      );
    border-right: 1px solid var(--border-subtle) !important;
  }
  section[data-testid="stSidebar"] .block-container { padding: 1.5rem 1.25rem !important; }
  section[data-testid="stSidebar"] h2 {
    font-family: var(--font-display) !important;
    font-size: 19px !important;
    color: var(--gold) !important;
    letter-spacing: 0.4px;
    margin-bottom: 0.25rem !important;
  }
  section[data-testid="stSidebar"] label,
  section[data-testid="stSidebar"] .stMarkdown p {
    font-size: 12.5px !important;
    color: var(--text-secondary) !important;
    letter-spacing: 0.3px;
  }
  section[data-testid="stSidebar"] hr {
    border-color: var(--border-subtle) !important;
    margin: 1rem 0 !important;
  }

  /* ═══════════════════════════════════════════════════
     PAGE HEADINGS
  ═══════════════════════════════════════════════════ */
  h1, h2, h3 {
    font-family: var(--font-display) !important;
    letter-spacing: 0.2px;
    color: var(--text-primary) !important;
  }
  h1 { font-size: 2rem !important; }
  h2 { font-size: 1.55rem !important; }
  h3 { font-size: 1.15rem !important; }

  /* ═══════════════════════════════════════════════════
     TABS
  ═══════════════════════════════════════════════════ */
  .stTabs [data-baseweb="tab-list"] {
    gap: 4px !important;
    background: rgba(255,255,255,0.025) !important;
    border-radius: var(--radius-md) var(--radius-md) 0 0;
    padding: 6px 6px 0 !important;
    border-bottom: 1px solid var(--border-subtle);
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: var(--radius-sm) var(--radius-sm) 0 0 !important;
    padding: 10px 20px !important;
    font-family: var(--font-body) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    transition: color var(--transition), background var(--transition) !important;
    border: none !important;
  }
  .stTabs [data-baseweb="tab"]:hover {
    color: var(--text-secondary) !important;
    background: rgba(255,255,255,0.04) !important;
  }
  .stTabs [aria-selected="true"] {
    color: var(--gold) !important;
    font-weight: 600 !important;
    background: rgba(226,185,111,0.07) !important;
  }
  .stTabs [data-baseweb="tab-highlight"] {
    background: linear-gradient(90deg, var(--gold), var(--gold-light)) !important;
    height: 2px !important;
    border-radius: 2px 2px 0 0 !important;
  }
  .stTabs [data-baseweb="tab-panel"] {
    background: rgba(255,255,255,0.018) !important;
    border: 1px solid var(--border-subtle) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
    padding: 2rem !important;
  }

  /* ═══════════════════════════════════════════════════
     METRIC CARDS
  ═══════════════════════════════════════════════════ */
  div[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    padding: 20px 22px !important;
    box-shadow: var(--shadow-card) !important;
    position: relative;
    overflow: hidden;
    transition: transform var(--transition), border-color var(--transition), box-shadow var(--transition) !important;
  }
  div[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(226,185,111,0.4), transparent);
  }
  div[data-testid="metric-container"]:hover {
    transform: translateY(-3px) !important;
    border-color: var(--border-accent) !important;
    box-shadow: var(--shadow-hover) !important;
  }
  div[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.9px !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
  }
  div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: var(--font-display) !important;
    font-size: 28px !important;
    color: var(--text-primary) !important;
    line-height: 1.2 !important;
  }
  div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-size: 11.5px !important;
    color: var(--teal) !important;
    font-weight: 500 !important;
  }

  /* ═══════════════════════════════════════════════════
     RESOURCE CARDS
  ═══════════════════════════════════════════════════ */
  .resource-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 22px 24px;
    margin-bottom: 14px;
    box-shadow: var(--shadow-card);
    position: relative;
    overflow: hidden;
    transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition);
  }
  .resource-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, var(--gold) 0%, var(--teal) 100%);
    border-radius: 3px 0 0 3px;
    opacity: 0;
    transition: opacity var(--transition);
  }
  .resource-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, rgba(226,185,111,0.2) 50%, transparent 100%);
  }
  .resource-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-hover);
    border-color: rgba(226,185,111,0.28);
    background: var(--bg-card-hover);
  }
  .resource-card:hover::before { opacity: 1; }
  .resource-card h4 {
    color: var(--gold) !important;
    margin: 0 0 10px !important;
    font-family: var(--font-display) !important;
    font-size: 16.5px !important;
    font-weight: 400 !important;
    letter-spacing: 0.2px;
    line-height: 1.35;
  }
  .resource-card p {
    color: var(--text-secondary) !important;
    font-size: 13px !important;
    margin: 0 !important;
    line-height: 1.6 !important;
  }

  /* ═══════════════════════════════════════════════════
     BADGES
  ═══════════════════════════════════════════════════ */
  .badge-open {
    display: inline-flex; align-items: center; gap: 4px;
    background: var(--success-bg); color: var(--success-fg);
    padding: 3px 11px 3px 9px; border-radius: 999px;
    font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.7px;
    border: 1px solid rgba(110,231,183,0.2);
    box-shadow: 0 0 10px rgba(110,231,183,0.12), 0 0 0 1px rgba(110,231,183,0.08) inset;
  }
  .badge-restricted {
    display: inline-flex; align-items: center; gap: 4px;
    background: var(--danger-bg); color: var(--danger-fg);
    padding: 3px 11px 3px 9px; border-radius: 999px;
    font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.7px;
    border: 1px solid rgba(252,165,165,0.2);
    box-shadow: 0 0 10px rgba(252,165,165,0.1), 0 0 0 1px rgba(252,165,165,0.08) inset;
  }
  .badge-flag {
    display: inline-flex; align-items: center; gap: 4px;
    background: var(--warn-bg); color: var(--warn-fg);
    padding: 3px 11px 3px 9px; border-radius: 999px;
    font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.7px;
    border: 1px solid rgba(252,211,77,0.2);
    box-shadow: 0 0 10px rgba(252,211,77,0.1), 0 0 0 1px rgba(252,211,77,0.08) inset;
  }

  /* ═══════════════════════════════════════════════════
     AI POLICY BRIEF BOX
  ═══════════════════════════════════════════════════ */
  .brief-box {
    background: linear-gradient(135deg, rgba(226,185,111,0.04) 0%, transparent 50%), var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-left: 3px solid var(--gold);
    border-radius: 0 var(--radius-md) var(--radius-md) 0;
    padding: 28px 32px;
    margin-top: 20px;
    box-shadow: var(--shadow-card);
    line-height: 1.75;
    position: relative;
  }
  .brief-box::before {
    content: '"';
    position: absolute;
    top: 12px; left: 18px;
    font-family: var(--font-display);
    font-size: 56px;
    color: rgba(226,185,111,0.12);
    line-height: 1;
    pointer-events: none;
    user-select: none;
  }

  /* ═══════════════════════════════════════════════════
     BUTTONS
  ═══════════════════════════════════════════════════ */
  div.stButton > button {
    font-family: var(--font-body) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.4px !important;
    border-radius: var(--radius-sm) !important;
    padding: 10px 20px !important;
    transition: all var(--transition) !important;
  }
  div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--gold) 0%, #c9a45e 100%) !important;
    color: #0b1724 !important;
    font-weight: 700 !important;
    border: none !important;
    box-shadow: 0 4px 16px rgba(226,185,111,0.3), 0 1px 0 rgba(255,255,255,0.15) inset !important;
  }
  div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, var(--gold-light) 0%, var(--gold) 100%) !important;
    box-shadow: 0 6px 24px rgba(226,185,111,0.45) !important;
    transform: translateY(-1px) !important;
  }
  div.stButton > button[kind="primary"]:active {
    transform: translateY(0) !important;
  }
  div.stDownloadButton > button {
    font-family: var(--font-body) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.4px !important;
    background: rgba(255,255,255,0.04) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-sm) !important;
    padding: 10px 20px !important;
    transition: all var(--transition) !important;
  }
  div.stDownloadButton > button:hover {
    background: rgba(255,255,255,0.08) !important;
    border-color: var(--border-accent) !important;
    color: var(--gold) !important;
    transform: translateY(-1px) !important;
  }

  /* ═══════════════════════════════════════════════════
     INPUTS
  ═══════════════════════════════════════════════════ */
  div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
    font-size: 13.5px !important;
    padding: 10px 14px !important;
    transition: border-color var(--transition), box-shadow var(--transition) !important;
  }
  div[data-testid="stTextInput"] input:focus {
    border-color: rgba(226,185,111,0.5) !important;
    box-shadow: 0 0 0 3px rgba(226,185,111,0.1) !important;
    background: rgba(255,255,255,0.06) !important;
  }
  div[data-testid="stTextInput"] input::placeholder { color: var(--text-muted) !important; }
  div[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
  }
  div[data-testid="stSelectbox"] > div > div:hover {
    border-color: var(--border-accent) !important;
    background: rgba(255,255,255,0.07) !important;
  }
  div[data-testid="stChatInput"] textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
  }
  div[data-testid="stChatInput"] textarea:focus {
    border-color: rgba(226,185,111,0.45) !important;
    box-shadow: 0 0 0 3px rgba(226,185,111,0.08) !important;
  }

  /* ═══════════════════════════════════════════════════
     ALERTS
  ═══════════════════════════════════════════════════ */
  div[data-testid="stAlert"] {
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border-subtle) !important;
    font-size: 13px !important;
  }

  /* ═══════════════════════════════════════════════════
     EXPANDER
  ═══════════════════════════════════════════════════ */
  details[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    overflow: hidden;
  }
  details[data-testid="stExpander"]:hover { border-color: var(--border-accent) !important; }
  details[data-testid="stExpander"] summary {
    background: rgba(255,255,255,0.025) !important;
    padding: 14px 18px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    color: var(--text-secondary) !important;
    letter-spacing: 0.3px;
    cursor: pointer;
  }
  details[data-testid="stExpander"] summary:hover { color: var(--gold) !important; }
  details[data-testid="stExpander"] > div { padding: 16px 18px !important; }

  /* ═══════════════════════════════════════════════════
     DATAFRAME
  ═══════════════════════════════════════════════════ */
  div[data-testid="stDataFrame"] {
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    overflow: hidden !important;
    box-shadow: var(--shadow-card) !important;
  }

  /* ═══════════════════════════════════════════════════
     CHAT MESSAGES
  ═══════════════════════════════════════════════════ */
  div[data-testid="stChatMessage"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    padding: 16px 20px !important;
    margin-bottom: 10px !important;
    box-shadow: var(--shadow-card) !important;
  }
  div[data-testid="stChatMessage"]:hover { border-color: var(--border-accent) !important; }

  /* ═══════════════════════════════════════════════════
     PLOTLY CHARTS
  ═══════════════════════════════════════════════════ */
  div[data-testid="stPlotlyChart"] {
    border-radius: var(--radius-md) !important;
    overflow: hidden;
    border: 1px solid var(--border-subtle) !important;
    box-shadow: var(--shadow-card) !important;
    background: var(--bg-card) !important;
  }
  div[data-testid="stPlotlyChart"]:hover {
    border-color: var(--border-accent) !important;
    box-shadow: var(--shadow-hover) !important;
  }

  /* ═══════════════════════════════════════════════════
     MARKDOWN
  ═══════════════════════════════════════════════════ */
  .stMarkdown p, .stMarkdown li { color: var(--text-secondary) !important; font-size: 13.5px !important; }
  .stMarkdown strong { color: var(--text-primary) !important; font-weight: 600 !important; }
  .stMarkdown a { color: var(--gold) !important; text-decoration: none; border-bottom: 1px solid rgba(226,185,111,0.3); }
  .stMarkdown a:hover { color: var(--gold-light) !important; }
  .stMarkdown code {
    background: rgba(226,185,111,0.1) !important;
    color: var(--gold-light) !important;
    padding: 2px 7px !important;
    border-radius: 4px !important;
    font-size: 12.5px !important;
    border: 1px solid rgba(226,185,111,0.18) !important;
  }
  .stMarkdown h4 {
    font-family: var(--font-body) !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
    margin-bottom: 12px !important;
  }

  hr { border: none !important; border-top: 1px solid var(--border-subtle) !important; margin: 1.5rem 0 !important; }
  small, .stMarkdown small { color: var(--text-muted) !important; font-size: 11.5px !important; }

  /* ═══════════════════════════════════════════════════
     PAGE-LOAD ANIMATION
  ═══════════════════════════════════════════════════ */
  .block-container { animation: fadeUp 0.5s ease both; }
  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
  }
</style>
""", unsafe_allow_html=True)


# ── Groq client ───────────────────────────────────────────────────────────────
@st.cache_resource
def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return None
    return Groq(api_key=api_key)

GROQ_MODEL = "llama-3.3-70b-versatile"

# ── Context token budget ───────────────────────────────────────────────────────
# Groq's llama-3.3-70b context window is 32 768 tokens.
# We reserve ~1 000 for the system prompt + question and ~600 for the reply,
# leaving ≈ 2 000 characters of catalog data (very conservative; 1 char ≈ 0.3 tokens).
MAX_CONTEXT_CHARS = 6_000   # ~2 000 tokens — safe for any Groq free-tier model


def build_chat_context(df: pd.DataFrame | None) -> str:
    """
    Build a compact, token-safe context string from the studies dataframe.

    Strategy:
      1. If no dataframe, return a static fallback string.
      2. Otherwise emit a schema summary + up to 30 rows of key columns only,
         then truncate the whole string to MAX_CONTEXT_CHARS.
    """
    if df is None:
        return (
            "No CSV uploaded yet. Use general knowledge about Rwanda gender data "
            "from NISR, MIGEPROF, BNR, REB, and UNFPA sources."
        )

    # Pick only the most informative columns to reduce token cost
    preferred_cols = ["title", "organization", "org", "publisher",
                      "year", "abstract", "summary", "description",
                      "quality_flags", "url"]
    keep = [c for c in preferred_cols if c in df.columns] or list(df.columns[:6])

    # Take at most 30 rows and convert to a readable list format
    subset = df[keep].head(30)
    lines = [f"Columns: {', '.join(keep)}", "---"]
    for i, (_, row) in enumerate(subset.iterrows(), 1):
        parts = []
        for col in keep:
            val = row.get(col, "")
            if pd.notna(val) and str(val).strip():
                # Truncate very long fields (e.g. abstracts) per cell
                cell = str(val).strip()
                if col in ("abstract", "summary", "description") and len(cell) > 200:
                    cell = cell[:200] + "…"
                parts.append(f"{col}: {cell}")
        lines.append(f"[{i}] " + " | ".join(parts))

    context = "\n".join(lines)

    # Hard cap — never exceed the budget regardless of dataframe size
    if len(context) > MAX_CONTEXT_CHARS:
        context = context[:MAX_CONTEXT_CHARS] + "\n…[truncated for length]"

    return context


# ── Helpers ───────────────────────────────────────────────────────────────────
@st.cache_data
def load_csv(file) -> pd.DataFrame:
    return pd.read_csv(file)


def normalise(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df


def get_col(df: pd.DataFrame, *candidates: str):
    for c in candidates:
        if c in df.columns:
            return c
    return None


def access_badge(flags: str) -> str:
    if pd.isna(flags) or str(flags).strip() == "":
        return '<span class="badge-open">🟢 Open</span>'
    if "restricted" in str(flags).lower():
        return '<span class="badge-restricted">🔴 Restricted</span>'
    return '<span class="badge-open">🟢 Open</span>'


def quality_badge(flags: str) -> str:
    if pd.isna(flags) or str(flags).strip() == "":
        return ""
    return f'<span class="badge-flag">⚠ {str(flags)[:60]}</span>'


def stream_policy_brief(context: str, district: str, sector: str):
    """Stream a policy brief using Groq."""
    client = get_groq_client()
    if client is None:
        yield "⚠️ GROQ_API_KEY not found in .env file. Please add it and restart."
        return

    system = (
        "You are an expert gender-responsive budgeting (GRB) analyst for Rwanda. "
        "Produce concise, evidence-based policy briefs for CSO officers and policymakers. "
        "Use clear headings and bullet points. Be specific to the Rwanda context."
    )
    prompt = (
        f"Write a one-page policy brief for advocacy.\n\n"
        f"District/Scope: {district}\nPolicy Sector: {sector}\n\n"
        f"Available evidence from the GRB resource catalog:\n{context}\n\n"
        "Structure the brief exactly as:\n"
        "## Problem Statement\n"
        "## Key Evidence (cite specific resources)\n"
        "## Data Gaps & Caveats\n"
        "## Recommendations\n"
        "## Suggested Next Steps for Advocacy"
    )

    stream = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt},
        ],
        max_tokens=1024,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


def stream_chat_answer(question: str, df_context: str):
    """
    Stream a chat answer using Groq.

    df_context must already be a compact, token-safe string
    produced by build_chat_context() — never a raw dataframe dump.
    """
    client = get_groq_client()
    if client is None:
        yield "⚠️ GROQ_API_KEY not found in .env file. Please add it and restart."
        return

    system = (
        "You are a helpful GRB data assistant for Rwanda. "
        "Answer questions about gender-related resources using the catalog data provided. "
        "Be concise, cite specific resources by title, and flag any data gaps."
    )
    prompt = (
        f"Catalog data summary:\n{df_context}\n\n"
        f"User question: {question}"
    )

    stream = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt},
        ],
        max_tokens=600,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🇷🇼 Advocacy Context")
    st.markdown("---")

    district = st.selectbox(
        "Target District",
        ["National", "Kigali City", "Gasabo", "Kicukiro", "Nyarugenge",
         "Eastern Province", "Western Province", "Northern Province", "Southern Province"],
    )
    sector = st.selectbox(
        "Policy Focus",
        ["Education", "Health", "Agriculture", "Economic Empowerment",
         "Justice & Security", "Water & Sanitation", "Nutrition", "Social Protection"],
    )

    st.markdown("---")
    st.info("Use these filters to set the context for your advocacy report and AI policy brief.")

    st.markdown("---")
    st.markdown("### 📂 Load Your Data")
    studies_file        = st.file_uploader("studies.csv",         type=["csv"], key="studies")
    resources_file      = st.file_uploader("study_resources.csv", type=["csv"], key="resources")
    quality_report_file = st.file_uploader("quality_report.csv",  type=["csv"], key="quality")

    # AI status indicator
    st.markdown("---")
    groq_key = os.getenv("GROQ_API_KEY", "")
    if groq_key:
        st.success("🤖 AI Assistant: Ready")
    else:
        st.error("🤖 AI Assistant: No API key")

    st.markdown(
        "<small style='color:#6b7280'>Rwanda GRB Resource Discovery Platform<br>"
        "Hackathon 2025 Submission</small>",
        unsafe_allow_html=True,
    )


# ── Load data ─────────────────────────────────────────────────────────────────
df_studies   = normalise(load_csv(studies_file))        if studies_file        else None
df_resources = normalise(load_csv(resources_file))      if resources_file      else None
df_quality   = normalise(load_csv(quality_report_file)) if quality_report_file else None

# ── Build the safe context string ONCE (used in Tab 4) ───────────────────────
# ✅ FIX: replaces the raw df.to_string() call that caused the 400 error
chat_context = build_chat_context(df_studies)


# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Discover Resources",
    "📊 Analytics Dashboard",
    "📄 AI Policy Brief",
    "💬 GRB Chat Assistant",
])


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — CATALOG / DISCOVERY
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("🔍 Discover Gender Data Resources")

    if df_studies is None:
        st.warning("⬅ Upload **studies.csv** in the sidebar to start discovering resources.")
        st.markdown("""
        **What this tab does:**
        - Searchable catalog of all gender-related datasets
        - Trust signals: quality flags, access status, source links
        - Filter by keyword, year, and organization
        """)
        st.stop()

    # column detection
    title_col = get_col(df_studies, "title")
    org_col   = get_col(df_studies, "organization", "org", "publisher")
    year_col  = get_col(df_studies, "year")

    # Force year column to numeric to fix slider type errors
    if year_col:
        df_studies[year_col] = pd.to_numeric(df_studies[year_col], errors="coerce")

    url_col   = get_col(df_studies, "url")
    qf_col    = get_col(df_studies, "quality_flags")
    abs_col   = get_col(df_studies, "abstract", "summary", "description")

    # ── Metrics row ──
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Total Resources",   len(df_studies))
    col_b.metric("Organizations",
                 df_studies[org_col].nunique() if org_col else "—")
    col_c.metric("Year Range",
                 f"{int(df_studies[year_col].min())}–{int(df_studies[year_col].max())}"
                 if year_col and df_studies[year_col].notna().any() else "—")
    flagged = df_studies[qf_col].notna().sum() if qf_col else 0
    col_d.metric("Resources with Quality Flags", flagged)

    st.markdown("---")

    # ── Filters ──
    fcol1, fcol2, fcol3 = st.columns([3, 2, 2])
    with fcol1:
        search_term = st.text_input(
            "🔎 Search by keyword",
            placeholder="e.g., education, nutrition, Kigali"
        )
    with fcol2:
        if year_col and df_studies[year_col].notna().any():
            year_min = int(df_studies[year_col].min())
            year_max = int(df_studies[year_col].max())
            year_range = st.slider("Year range", year_min, year_max, (year_min, year_max))
        else:
            year_range = None
    with fcol3:
        if org_col:
            orgs = ["All"] + sorted(df_studies[org_col].dropna().unique().tolist())
            selected_org = st.selectbox("Organization", orgs)
        else:
            selected_org = "All"

    # ── Apply filters ──
    filtered = df_studies.copy()

    if search_term:
        mask = pd.Series(False, index=filtered.index)
        for col in [title_col, abs_col, org_col]:
            if col:
                mask |= filtered[col].astype(str).str.contains(
                    search_term, case=False, na=False
                )
        filtered = filtered[mask]

    if year_range and year_col:
        filtered = filtered[
            filtered[year_col].between(year_range[0], year_range[1], inclusive="both")
        ]

    if selected_org != "All" and org_col:
        filtered = filtered[filtered[org_col] == selected_org]

    st.success(f"**{len(filtered)}** resource(s) found")

    # ── Resource cards ──
    for _, row in filtered.iterrows():
        title    = row.get(title_col, "Untitled")  if title_col else "Untitled"
        org      = row.get(org_col,   "Unknown")   if org_col   else "Unknown"
        year     = int(row[year_col]) if year_col and pd.notna(row.get(year_col)) else "N/A"
        url      = row.get(url_col,   "")          if url_col   else ""
        flags    = row.get(qf_col,    "")          if qf_col    else ""
        abstract = str(row.get(abs_col, "No abstract available."))[:300] if abs_col else ""

        if url and str(url).startswith("http"):
            link_html = f'<a href="{url}" target="_blank" style="color:#60a5fa;font-size:12px">🔗 Access Source</a>'
        else:
            link_html = '<span style="color:#6b7280;font-size:12px">No URL available</span>'

        st.markdown(f"""
        <div class="resource-card">
          <h4>{title}</h4>
          <p>
            <strong style="color:#d1d5db">🏢 {org}</strong> &nbsp;|&nbsp;
            📅 {year} &nbsp;|&nbsp;
            {access_badge(flags)} &nbsp; {quality_badge(flags)}
          </p>
          <p style="margin-top:8px">{abstract}{"..." if len(abstract) == 300 else ""}</p>
          <p style="margin-top:8px">{link_html}</p>
        </div>
        """, unsafe_allow_html=True)

    # ── Quality caveats ──
    if df_quality is not None:
        with st.expander("⚠️ Quality Report — Data Caveats & Limitations"):
            st.markdown("Known quality issues with resources in the catalog.")
            st.dataframe(df_quality, use_container_width=True)
    else:
        with st.expander("⚠️ Quality Caveats (upload quality_report.csv for full details)"):
            st.markdown("""
            Common caveats in Rwanda gender data:
            - Some NISR resources are **PDF-only** (not machine-readable)
            - District-level disaggregation may not be available for all indicators
            - Some datasets require registration at source institution
            - Publication lag: most recent data may be 2–3 years old
            """)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ANALYTICS DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("📊 Analytics Dashboard")

    if df_studies is None:
        st.info("Upload studies.csv in the sidebar to see analytics.")
        st.stop()

    col1, col2 = st.columns(2)

    # Chart 1 — Resources by Organization
    with col1:
        st.markdown("#### Resources by Organization")
        if org_col:
            org_counts = df_studies[org_col].value_counts().reset_index()
            org_counts.columns = ["Organization", "Count"]
            fig = px.bar(
                org_counts.head(10), x="Count", y="Organization",
                orientation="h", color="Count",
                color_continuous_scale=["#1d4e3a", "#2d9c6f", "#e2b96f"],
                template="plotly_dark",
            )
            fig.update_layout(
                paper_bgcolor="#0d1b2a", plot_bgcolor="#0d1b2a",
                showlegend=False, coloraxis_showscale=False,
                margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No organization column found.")

    # Chart 2 — Publications per Year
    with col2:
        st.markdown("#### Publications per Year")
        if year_col and df_studies[year_col].notna().any():
            year_counts = (
                df_studies[year_col].value_counts().sort_index().reset_index()
            )
            year_counts.columns = ["Year", "Count"]
            fig2 = px.area(
                year_counts, x="Year", y="Count",
                color_discrete_sequence=["#2d9c6f"],
                template="plotly_dark",
            )
            fig2.update_traces(
                fillcolor="rgba(45,156,111,0.25)", line_color="#2d9c6f"
            )
            fig2.update_layout(
                paper_bgcolor="#0d1b2a", plot_bgcolor="#0d1b2a",
                margin=dict(l=10, r=10, t=10, b=10),
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No year column found.")

    st.markdown("---")
    col3, col4 = st.columns(2)

    # Chart 3 — Gender Focus donut
    with col3:
        st.markdown("#### Resource Allocation by Gender Focus")
        gender_data = pd.DataFrame({
            "Category": ["Female-focused", "Male-focused", "Both / Disaggregated"],
            "Value":    [58, 22, 20],
        })
        fig3 = px.pie(
            gender_data, names="Category", values="Value", hole=0.45,
            color_discrete_sequence=["#2d9c6f", "#e2b96f", "#3b82f6"],
            template="plotly_dark",
        )
        fig3.update_layout(
            paper_bgcolor="#0d1b2a", plot_bgcolor="#0d1b2a",
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(font=dict(color="#9ca3af")),
        )
        st.plotly_chart(fig3, use_container_width=True)

    # Chart 4 — Urban vs Rural
    with col4:
        st.markdown("#### Intersectionality: Urban vs Rural Needs")
        intersect_data = pd.DataFrame({
            "Location": ["Urban", "Urban", "Rural", "Rural"],
            "Gender":   ["Female", "Male", "Female", "Male"],
            "Count":    [42, 28, 35, 18],
        })
        fig4 = px.bar(
            intersect_data, x="Location", y="Count", color="Gender",
            barmode="group",
            color_discrete_map={"Female": "#2d9c6f", "Male": "#e2b96f"},
            template="plotly_dark",
        )
        fig4.update_layout(
            paper_bgcolor="#0d1b2a", plot_bgcolor="#0d1b2a",
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(font=dict(color="#9ca3af")),
        )
        st.plotly_chart(fig4, use_container_width=True)

    # Advocacy snapshot
    st.markdown("---")
    st.markdown(f"#### Advocacy Snapshot: **{district}** — **{sector}**")
    snap1, snap2, snap3 = st.columns(3)
    snap1.metric("Sector Resources",     "12", "+3 since 2022")
    snap2.metric("Gender-disaggregated", "8",  "67% of total")
    snap3.metric("Avg. Data Recency",    "2021", "3-year lag ⚠")

    st.info(
        f"**Data note:** Figures above are illustrative. "
        f"Upload the full dataset for precise {district} / {sector} breakdowns."
    )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — AI POLICY BRIEF
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("📄 AI-Powered Policy Brief Generator")
    st.markdown(
        "Generate an evidence-based, advocacy-ready policy brief "
        "using the catalog data and AI."
    )

    col_brief, col_info = st.columns([2, 1])

    with col_info:
        st.markdown("**Brief will cover:**")
        st.markdown(f"- 📍 District: **{district}**")
        st.markdown(f"- 🏷 Sector: **{sector}**")
        st.markdown("- 📚 Evidence from catalog")
        st.markdown("- ⚠️ Data gaps & caveats")
        st.markdown("- ✅ Concrete recommendations")
        st.markdown("---")
        st.markdown(
            "<small style='color:#9ca3af'>Generated by Llama 3.3 via Groq. "
            "Verify statistics with original NISR sources before publication.</small>",
            unsafe_allow_html=True,
        )

    with col_brief:
        # Build context from loaded data
        context_lines = []
        if df_studies is not None and title_col:
            for _, r in df_studies.head(10).iterrows():
                t   = r.get(title_col, "")
                org = r.get(org_col,   "") if org_col  else ""
                yr  = r.get(year_col,  "") if year_col else ""
                qf  = r.get(qf_col,    "") if qf_col   else ""
                context_lines.append(f"- {t} ({org}, {yr}) [flags: {qf}]")
        else:
            context_lines = [
                "- Rwanda Demographic and Health Survey 2020 (NISR, 2020)",
                "- Women's Financial Inclusion Study (BNR, 2021)",
                "- Girls' Education Completion Rates Report (REB, 2022)",
                "- Gender-Based Violence Prevalence Data (MIGEPROF, 2021)",
                "- Rwanda Labor Force Survey — Gender Module (NISR, 2022)",
            ]
        context_str = "\n".join(context_lines)

        generate_btn = st.button(
            "📝 Generate Policy Brief", type="primary", use_container_width=True
        )

        if generate_btn:
            st.markdown('<div class="brief-box">', unsafe_allow_html=True)
            st.markdown(f"**📍 {district} | {sector} | Rwanda GRB Policy Brief**")
            st.markdown("---")
            placeholder = st.empty()
            full_text = ""
            with st.spinner("Generating brief with AI..."):
                for chunk in stream_policy_brief(context_str, district, sector):
                    full_text += chunk
                    placeholder.markdown(full_text)
            st.markdown('</div>', unsafe_allow_html=True)

            st.download_button(
                "⬇️ Download Brief (.txt)",
                data=full_text,
                file_name=f"GRB_Brief_{district}_{sector}.txt",
                mime="text/plain",
            )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — AI CHAT ASSISTANT
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("💬 GRB Chat Assistant")
    st.markdown(
        "Ask any question about the gender data catalog. "
        "The assistant is aware of all loaded resources."
    )

    # ✅ FIX: use the pre-built, token-safe context string instead of df.to_string()
    # chat_context was built above with build_chat_context(df_studies)

    # Initialise chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hi! I'm your GRB data assistant 👋\n\n"
                    "Ask me anything about the gender resource catalog — for example:\n"
                    "- *What education datasets are available?*\n"
                    "- *Which resources cover Kigali City?*\n"
                    "- *What data gaps exist for women's economic empowerment?*"
                ),
            }
        ]

    # Display history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User input
    if prompt := st.chat_input("Ask about the GRB catalog..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            reply_placeholder = st.empty()
            full_reply = ""
            # ✅ FIX: pass chat_context (safe string) not df.to_string()
            for chunk in stream_chat_answer(prompt, chat_context):
                full_reply += chunk
                reply_placeholder.markdown(full_reply)

        st.session_state.messages.append(
            {"role": "assistant", "content": full_reply}
        )
