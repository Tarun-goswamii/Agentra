"""Sidebar Module for Agentra."""

import streamlit as st
import os

def render_sidebar():
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        st.markdown("---")

        # Connection / Backend Status
        amd_url   = os.getenv("AMD_BASE_URL", "http://localhost:8000/v1")
        amd_model = os.getenv("AMD_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")
        backend   = os.getenv("LLM_BACKEND", "amd").upper()

        st.markdown(f"""
        <div class='agent-card'>
          <div class='agent-header'>🔥 Inference Backend</div>
          <div class='agent-body'>
            Active : <span class='status-badge badge-amd'>{backend}</span><br>
            Endpoint: <code style='font-size:0.8rem;color:#fdba74'>{amd_url}</code><br>
            Model   : <code style='font-size:0.8rem;color:#fdba74'>{amd_model.split('/')[-1]}</code>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔌 Test Connection", key="test_conn"):
            with st.spinner("Testing..."):
                try:
                    import requests
                    r = requests.get(f"{amd_url}/models", timeout=5)
                    if r.status_code == 200:
                        st.success("✅ AMD vLLM connected!")
                    else:
                        st.warning(f"⚠️ Status {r.status_code}")
                except Exception as e:
                    st.error(f"❌ Cannot reach AMD endpoint.\nRun vLLM server first or fallback to Groq.\n\n{e}")

        st.markdown("---")
        st.markdown("### 🤖 Agent Pipeline")
        agents_info = [
            ("🎯", "Strategist",  "Content strategy + calendar"),
            ("🔍", "Researcher",  "Trends + viral hooks"),
            ("✍️", "Creator",     "Scripts + captions"),
            ("⚡", "Optimizer",   "Engagement rewrites"),
            ("📊", "Feedback",    "Performance analysis"),
        ]
        
        for icon, name, desc in agents_info:
            st.markdown(f"""
            <div class='agent-card' style='padding:0.8rem 1.2rem; margin-bottom:0.8rem'>
              <div style='font-weight:700; font-size:1.05rem; color:#d8b4fe'>{icon} {name}</div>
              <div style='font-size:0.85rem; color:#94a3b8; margin-top:0.2rem'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Memory stats
        try:
            from memory import memory_summary
            mem = memory_summary()
            st.markdown("### 🧠 Agentra Memory")
            c1, c2 = st.columns(2)
            c1.metric("Content", mem["total_content"])
            c2.metric("Niches", len(mem["niches_tracked"]))
            c1.metric("✅ Top", mem["high_performers"])
            c2.metric("❌ Low", mem["low_performers"])
            if mem["niches_tracked"]:
                st.caption(f"Tracked: {', '.join(mem['niches_tracked'])}")
        except Exception:
            pass

        if st.button("🗑️ Clear Memory", key="clear_mem"):
            from memory import clear_memory
            clear_memory()
            st.success("Memory cleared!")
