"""Feedback Task — analyzes performance and suggests strategy improvements."""

from crewai import Task
from crewai import Agent


def build_feedback_task(
    agent: Agent,
    niche: str,
    platform: str,
    performance_data: str,
    high_performers: list,
    low_performers: list,
) -> Task:
    hp_summary = "\n".join(
        [f"  - {c.get('title', 'Unknown')} (score: {c.get('score', 'N/A')})" for c in high_performers]
    ) or "  No high-performer history yet."

    lp_summary = "\n".join(
        [f"  - {c.get('title', 'Unknown')} (score: {c.get('score', 'N/A')})" for c in low_performers]
    ) or "  No low-performer history yet."

    perf_section = f"""
CURRENT BATCH PERFORMANCE DATA:
{performance_data or "No live performance data provided. Analyze based on content quality and optimization scores."}

HISTORICAL HIGH PERFORMERS (from memory):
{hp_summary}

HISTORICAL LOW PERFORMERS (from memory):
{lp_summary}
""".strip()

    return Task(
        description=f"""
You are the Performance Analyst & Feedback Coach. Your job is to close the learning loop.

CONTEXT:
- Niche    : {niche}
- Platform : {platform}

{perf_section}

YOUR DELIVERABLES:

1. CONTENT BATCH ASSESSMENT
   - Review the optimized content from the previous agent
   - Score each reel 1–10 on: Hook strength, Value delivery, CTA effectiveness, Virality potential
   - Provide an overall batch grade (A/B/C/D/F) with brief rationale

2. PATTERN ANALYSIS
   - What content TYPES are predicted to perform best in this niche?
   - What hooks are working vs. failing?
   - What emotional triggers are underused?

3. AUDIENCE INSIGHTS
   - Based on the niche "{niche}" and platform "{platform}", what does the audience REALLY want?
   - What content gaps exist that competitors aren't filling?

4. STRATEGY ADJUSTMENT RECOMMENDATIONS (5 specific actions)
   For each action:
   - What to change
   - Why (backed by data or behavioral reasoning)
   - Expected impact

5. NEXT BATCH BRIEF
   - Top 3 content ideas for the NEXT week, based on what you've learned
   - The single most important improvement to make
   - A specific experiment to test (e.g., "Test storytime hooks vs. list hooks for 2 weeks")

6. MEMORY UPDATE NOTES
   [List what should be stored in long-term memory from this run:]
   - Successful hooks to reuse
   - Content formats to avoid
   - Audience preferences observed

Format everything clearly. Be direct and specific — no vague advice.
""",
        expected_output=(
            "A feedback report with: content batch scores, pattern analysis, audience insights, "
            "5 strategy adjustment recommendations, a next-batch brief with 3 content ideas, "
            "and memory update notes listing lessons learned."
        ),
        agent=agent,
    )
