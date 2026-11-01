"""Research Task — identifies trends, hooks, and content ideas."""

from crewai import Task
from crewai import Agent


def build_research_task(agent: Agent, niche: str, platform: str, strategy_output: str = "") -> Task:
    return Task(
        description=f"""
You are the Trend Researcher. Your job is to find the best content opportunities RIGHT NOW.

INPUTS:
- Niche           : {niche}
- Platform        : {platform}
- Strategy Context: Use the content pillars and goals from the strategy (previous task output).

YOUR DELIVERABLES:
1. TREND REPORT
   - Use TrendFetcherTool with niche="{niche}" and platform="{platform}"
   - Summarize the top 5 trending topics in this niche

2. VIRAL HOOK ANALYSIS
   - List 5 proven hook formulas that work for this niche
   - For each hook: explain WHY it works psychologically
   - Example: "Nobody talks about [X]..." triggers curiosity gap

3. CONTENT IDEAS (5 ideas)
   For each idea provide:
   - Title/concept
   - Why it's trending NOW
   - Target emotion (curiosity, FOMO, inspiration, surprise)
   - Suggested format (tutorial, storytime, list, myth-bust)
   - Estimated virality potential (High/Medium/Low) with reason

4. COMPETITOR CONTENT GAPS
   - What are other creators in this niche NOT covering?
   - 2–3 underserved angles the creator can own

5. HASHTAG INTELLIGENCE
   - 10 niche-specific hashtags
   - 5 broad hashtags for reach
   - 3 emerging hashtags (trending but not yet saturated)

Return all findings in a structured, easy-to-read format.
""",
        expected_output=(
            "A trend research report with: trend summary, 5 viral hook formulas with psychology explanations, "
            "5 specific content ideas with virality ratings, competitor content gaps, and a hashtag strategy "
            "split into niche/broad/emerging categories."
        ),
        agent=agent,
    )
