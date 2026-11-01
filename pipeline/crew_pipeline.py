"""
CrewAI Pipeline — assembles and runs the 5-agent content creation crew.

Pipeline:
  User Input
    → Strategist  (strategy + weekly calendar)
    → Researcher  (trends + content ideas)
    → Creator     (3 reel scripts + captions + hashtags)
    → Optimizer   (engagement optimization)
    → Feedback    (performance analysis + strategy updates)
    → Memory      (store results for future runs)
"""

from crewai import Crew, Process

from agents import (
    build_strategist,
    build_researcher,
    build_creator,
    build_optimizer,
    build_feedback_agent,
)
from tasks import (
    build_strategy_task,
    build_research_task,
    build_creation_task,
    build_optimization_task,
    build_feedback_task,
)
from memory import (
    get_niche_context,
    save_niche_preferences,
    log_content,
    get_high_performers,
    get_low_performers,
)
from utils.llm_factory import get_llm


def run_pipeline(
    niche: str,
    platform: str,
    goal: str,
    performance_data: str = "",
    progress_callback=None,
) -> dict:
    """
    Run the full 5-agent content creation pipeline.

    Args:
        niche            : Content niche (e.g. "Coding for beginners")
        platform         : Target platform (e.g. "Instagram")
        goal             : Growth goal (e.g. "Grow to 5k followers")
        performance_data : Optional JSON string with past post metrics
        progress_callback: Optional callable(step_name: str, msg: str) for UI updates

    Returns:
        dict with keys: strategy, research, content, optimized, feedback
    """

    def _progress(step: str, msg: str):
        if progress_callback:
            progress_callback(step, msg)

    # ── 1. Load memory context ────────────────────────────────────────────────
    _progress("memory", f"🧠 Loading memory for niche: {niche}")
    memory_ctx = get_niche_context(niche)
    high_perf  = get_high_performers(niche, limit=5)
    low_perf   = get_low_performers(niche, limit=5)

    memory_summary_text = ""
    if memory_ctx:
        memory_summary_text = (
            f"Platform preferences: {memory_ctx.get('platform', 'N/A')}\n"
            f"Past goal: {memory_ctx.get('goal', 'N/A')}\n"
            f"Last used: {memory_ctx.get('last_used', 'N/A')}"
        )

    # ── 2. Build LLM ─────────────────────────────────────────────────────────
    _progress("llm", "⚙️  Connecting to AMD vLLM endpoint...")
    llm = get_llm()

    # ── 3. Build agents ───────────────────────────────────────────────────────
    _progress("agents", "🤖 Assembling agent team...")
    strategist   = build_strategist(llm)
    researcher   = build_researcher(llm)
    creator      = build_creator(llm)
    optimizer    = build_optimizer(llm)
    feedback_bot = build_feedback_agent(llm)

    # ── 4. Build tasks ────────────────────────────────────────────────────────
    _progress("tasks", "📋 Defining task pipeline...")
    task_strategy  = build_strategy_task(strategist, niche, platform, goal, memory_summary_text)
    task_research  = build_research_task(researcher, niche, platform)
    task_creation  = build_creation_task(creator, niche, platform)
    task_optimize  = build_optimization_task(optimizer, platform)
    task_feedback  = build_feedback_task(
        feedback_bot, niche, platform, performance_data, high_perf, low_perf
    )

    # ── 5. Assemble Crew ──────────────────────────────────────────────────────
    _progress("crew", "🚀 Starting CrewAI sequential pipeline...")
    crew = Crew(
        agents=[strategist, researcher, creator, optimizer, feedback_bot],
        tasks=[task_strategy, task_research, task_creation, task_optimize, task_feedback],
        process=Process.sequential,  # Each agent hands off to the next
        verbose=True,
        max_rpm=15,  # Throttles execution to avoid hitting Groq free tier API limits
    )

    # ── 6. Execute ────────────────────────────────────────────────────────────
    _progress("executing", "⚡ Running agents on AMD GPU (this may take 1–3 minutes)...")
    result = crew.kickoff()

    # ── 7. Parse task outputs ────────────────────────────────────────────────
    outputs = {
        "strategy":  _safe_output(task_strategy),
        "research":  _safe_output(task_research),
        "content":   _safe_output(task_creation),
        "optimized": _safe_output(task_optimize),
        "feedback":  _safe_output(task_feedback),
        "final":     str(result),
    }

    # ── 8. Save to memory ────────────────────────────────────────────────────
    _progress("memory", "💾 Saving results to memory...")
    save_niche_preferences(niche, {"platform": platform, "goal": goal})
    log_content(
        niche=niche,
        platform=platform,
        content={
            "strategy":  outputs["strategy"][:500],
            "research":  outputs["research"][:500],
            "scripts":   outputs["content"][:1000],
            "optimized": outputs["optimized"][:1000],
            "feedback":  outputs["feedback"][:500],
        },
    )

    _progress("done", "✅ Pipeline complete!")
    return outputs


def _safe_output(task) -> str:
    """Safely extract task output string."""
    try:
        if hasattr(task, "output") and task.output:
            if hasattr(task.output, "raw"):
                return str(task.output.raw)
            return str(task.output)
        return "No output generated."
    except Exception as e:
        return f"Error extracting output: {e}"
