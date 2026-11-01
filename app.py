"""Streamlit UI — Agentra AI Content Creator System."""

import streamlit as st
import time
from datetime import datetime
from dotenv import load_dotenv

# Import the new UI modules
from ui.styles import inject_custom_css
from ui.sidebar import render_sidebar
from ui.components import render_hero_header, render_input_form, render_success_metrics, render_output_tabs

load_dotenv()

st.set_page_config(
    page_title="Agentra — AI Content Creator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 1. Inject Premium Styles
inject_custom_css()

# 2. Render Sidebar
render_sidebar()

# 3. Render Main Area
render_hero_header()

# 4. Render Input Form
submitted, niche, platform, goal, performance_data = render_input_form()

# 5. Handle Execution
if submitted:
    if not niche.strip():
        st.error("Please enter a content niche.")
        st.stop()

    # Progress tracking components
    progress_log = []
    status_placeholder = st.empty()
    progress_bar = st.progress(0)
    step_map = {"memory": 5, "llm": 10, "agents": 20, "tasks": 30,
                "crew": 35, "executing": 40, "done": 100}

    def on_progress(step: str, msg: str):
        progress_log.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
        pct = step_map.get(step, 50)
        progress_bar.progress(pct)
        status_placeholder.markdown(
            f"<div style='color:#c084fc;font-size:0.95rem;font-weight:500'>⚡ {msg}</div>",
            unsafe_allow_html=True,
        )

    try:
        from pipeline.crew_pipeline import run_pipeline

        start_ts = time.time()
        with st.spinner(""):
            results = run_pipeline(
                niche=niche,
                platform=platform,
                goal=goal,
                performance_data=performance_data,
                progress_callback=on_progress,
            )
        elapsed = time.time() - start_ts

        progress_bar.progress(100)
        status_placeholder.empty()

        # Success visual feedback
        render_success_metrics(elapsed, platform, niche)

        # Main Output Tabs
        render_output_tabs(results, niche)

        # Execution Log Expander
        with st.expander("🔍 Detailed Execution Log"):
            st.code("\n".join(progress_log))

    except Exception as e:
        st.error(f"❌ Pipeline error: {e}")
        with st.expander("Full traceback"):
            import traceback
            st.code(traceback.format_exc())

st.markdown("---")
st.markdown("""
<div style='text-align:center;color:#475569;font-size:0.85rem;letter-spacing:0.02em'>
  Agentra · 5-Agent CrewAI Pipeline · Powered by AMD Instinct
</div>
""", unsafe_allow_html=True)
