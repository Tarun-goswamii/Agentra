"""Main Content Components for Agentra UI."""

import streamlit as st
import json
from datetime import datetime

def render_hero_header():
    st.markdown("<div class='hero-title'>🚀 Agentra</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='hero-sub'>Agentic AI Content Creator · Multi-Agent Pipeline · Powered by AMD Instinct</div>",
        unsafe_allow_html=True,
    )
    st.markdown("""
    <div class='pipeline-flow'>
      🎯 STRATEGY &nbsp;→&nbsp; 🔍 RESEARCH &nbsp;→&nbsp; ✍️ CREATION &nbsp;→&nbsp; ⚡ OPTIMIZATION &nbsp;→&nbsp; 📊 FEEDBACK
    </div>
    """, unsafe_allow_html=True)

def render_input_form():
    with st.form("pipeline_form"):
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            niche = st.text_input(
                "🎯 Content Niche",
                value="Coding for beginners",
                placeholder="e.g. Fitness, Personal Finance...",
            )
        with col2:
            platform = st.selectbox(
                "📱 Platform",
                ["Instagram", "TikTok", "YouTube", "LinkedIn", "Twitter"],
            )
        with col3:
            goal = st.text_input(
                "🏆 Growth Goal",
                value="Grow to 5k followers in 90 days",
                placeholder="e.g. Get 10k views per reel",
            )

        with st.expander("📊 Add Past Performance Data (optional)", expanded=False):
            perf_cols = st.columns(4)
            views      = perf_cols[0].number_input("Views", min_value=0, value=0)
            likes      = perf_cols[1].number_input("Likes", min_value=0, value=0)
            comments   = perf_cols[2].number_input("Comments", min_value=0, value=0)
            saves      = perf_cols[3].number_input("Saves", min_value=0, value=0)
            shares     = perf_cols[0].number_input("Shares", min_value=0, value=0)
            fol_gained = perf_cols[1].number_input("Followers Gained", min_value=0, value=0)
            content_type_sel = perf_cols[2].text_input("Content Type", value="Tutorial Reel")
            hook_text_inp    = perf_cols[3].text_input("Hook Used", value="")

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀 Launch Agentra Pipeline", use_container_width=True)

    performance_data = ""
    if submitted and views > 0:
        performance_data = json.dumps({
            "views": views, "likes": likes, "comments": comments,
            "saves": saves, "shares": shares,
            "followers_gained": fol_gained,
            "content_type": content_type_sel,
            "hook_text": hook_text_inp,
            "profile_visits": int(views * 0.05),
        })

    return submitted, niche, platform, goal, performance_data

def render_success_metrics(elapsed_time, platform, niche):
    st.markdown(f"""
    <div class='success-banner'>
      <span>✅ Pipeline Complete — {elapsed_time:.0f}s · {platform} · {niche}</span>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4, m5 = st.columns(5)
    labels = ["🎯 Strategy", "🔍 Research", "✍️ 3 Reels", "⚡ Optimized", "📊 Feedback"]
    for col, label in zip([m1, m2, m3, m4, m5], labels):
        col.markdown(
            f"<div class='metric-box'><div class='metric-value'>✓</div>"
            f"<div class='metric-label'>{label}</div></div>",
            unsafe_allow_html=True,
        )
    st.markdown("<br>", unsafe_allow_html=True)

def render_output_tabs(results, niche):
    tab_labels = ["🎯 Strategy", "🔍 Research", "✍️ Content", "⚡ Optimized", "📊 Feedback", "📋 All"]
    tabs = st.tabs(tab_labels)

    output_map = [
        ("strategy",  "🎯 Content Strategy & Weekly Calendar"),
        ("research",  "🔍 Trend Research & Content Ideas"),
        ("content",   "✍️ Generated Reels (Script + Caption + Hashtags)"),
        ("optimized", "⚡ Optimized Content (Engagement-Ready)"),
        ("feedback",  "📊 Performance Feedback & Next Steps"),
    ]

    for tab, (key, title) in zip(tabs[:5], output_map):
        with tab:
            st.markdown(f"### {title}")
            content_text = results.get(key, "No output.")
            st.markdown(
                f"<div class='agent-card'><div class='agent-body'>{content_text}</div></div>",
                unsafe_allow_html=True,
            )
            st.download_button(
                label=f"⬇️ Download {title.split()[1]}",
                data=content_text,
                file_name=f"{key}_{niche.replace(' ','_')}.txt",
                mime="text/plain",
                key=f"dl_{key}",
            )

    with tabs[5]:
        st.markdown("### 📋 Full Pipeline Output")
        all_output = "\n\n" + "="*60 + "\n\n".join(
            [f"{'='*60}\n{t}\n{'='*60}\n{results.get(k,'')}"
             for k, t in [
                 ("strategy","STRATEGY"), ("research","RESEARCH"),
                 ("content","CONTENT"), ("optimized","OPTIMIZED"),
                 ("feedback","FEEDBACK"),
             ]]
        )
        st.text_area("Full Output", all_output, height=600, label_visibility="collapsed")
        st.download_button(
            "⬇️ Download Full Report",
            data=all_output,
            file_name=f"agentra_full_report_{niche.replace(' ','_')}_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
            key="dl_all",
        )
