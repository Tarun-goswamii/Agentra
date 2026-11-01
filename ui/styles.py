"""CSS Styles for Agentra UI."""

import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
    /* Import modern Google Font (Outfit) */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    /* Global Typography */
    * { 
        font-family: 'Outfit', sans-serif; 
    }

    /* Main App Background (Premium Gradient) */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #020617 100%);
        min-height: 100vh;
    }

    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Text Colors */
    [data-testid="stSidebar"] * { color: #f8fafc !important; }
    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3 { color: #f8fafc; }
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] li { color: #cbd5e1; }

    /* Hero Headers */
    .hero-title {
        font-size: 4rem; 
        font-weight: 800;
        background: linear-gradient(135deg, #c084fc, #3b82f6, #06b6d4);
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        text-align: center; 
        margin-bottom: 0.2rem;
        letter-spacing: -0.02em;
    }
    .hero-sub {
        text-align: center; 
        color: #94a3b8; 
        font-size: 1.1rem; 
        font-weight: 300;
        margin-bottom: 2.5rem;
        letter-spacing: 0.02em;
    }

    /* Agent Cards / General Cards */
    .agent-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px; 
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.2rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .agent-card:hover { 
        border-color: rgba(192, 132, 252, 0.5); 
        transform: translateY(-4px); 
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1);
        background: rgba(255, 255, 255, 0.06);
    }
    .agent-header { font-weight: 700; font-size: 1.1rem; color: #d8b4fe; margin-bottom: 0.5rem; }
    .agent-body { color: #cbd5e1; font-size: 0.95rem; line-height: 1.7; white-space: pre-wrap; }

    /* Pipeline Status Flow */
    .pipeline-flow {
        text-align: center; 
        margin-bottom: 2.5rem; 
        color: #64748b; 
        font-size: 0.95rem; 
        font-weight: 500;
        letter-spacing: 0.08em;
    }

    /* Metrics */
    .metric-box {
        background: rgba(59, 130, 246, 0.1); 
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 14px; 
        padding: 1.2rem; 
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-box:hover {
        background: rgba(59, 130, 246, 0.15);
        transform: scale(1.02);
    }
    .metric-value { font-size: 2rem; font-weight: 800; color: #bfdbfe; }
    .metric-label { font-size: 0.85rem; font-weight: 500; color: #94a3b8; margin-top: 0.3rem; }

    /* Status Badges */
    .status-badge {
        display: inline-block; padding: 0.25rem 0.8rem;
        border-radius: 999px; font-size: 0.8rem; font-weight: 600;
    }
    .badge-amd  { background: rgba(234, 88, 12, 0.2); color: #fdba74; border: 1px solid rgba(234, 88, 12, 0.4); }
    .badge-ok   { background: rgba(22, 163, 74, 0.2); color: #86efac; border: 1px solid rgba(22, 163, 74, 0.4); }
    .badge-warn { background: rgba(202, 138, 4, 0.2); color: #fde047; border: 1px solid rgba(202, 138, 4, 0.4); }

    /* Buttons (Larger, more premium) */
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6, #3b82f6);
        color: white; 
        border: none; 
        border-radius: 14px;
        padding: 0.8rem 2.5rem; 
        font-weight: 700; 
        font-size: 1.1rem;
        width: 100%; 
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #a78bfa, #60a5fa);
        transform: translateY(-3px); 
        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.4);
    }
    .stButton > button:active {
        transform: translateY(1px);
    }

    /* Inputs (Larger options) */
    .stTextInput input, .stTextArea textarea, .stSelectbox select, .stNumberInput input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #f8fafc !important; 
        border-radius: 12px !important;
        padding: 0.8rem 1rem !important;
        font-size: 1.05rem !important;
        transition: border-color 0.3s ease;
    }
    .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus, .stNumberInput input:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2) !important;
    }

    /* Form specific styles */
    [data-testid="stForm"] {
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.02);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8; 
        font-weight: 600;
        font-size: 1.05rem;
        padding: 1rem 1.5rem;
    }
    .stTabs [aria-selected="true"] { 
        color: #c084fc !important; 
    }
    
    /* Success Banner */
    .success-banner {
        background: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 14px;
        padding: 1.2rem 1.5rem;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .success-banner span {
        color: #86efac;
        font-weight: 700;
        font-size: 1.15rem;
    }
    </style>
    """, unsafe_allow_html=True)
