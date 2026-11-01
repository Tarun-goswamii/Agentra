"""Strategy Task — defines the content strategy and weekly calendar."""

from crewai import Task
from crewai import Agent


def build_strategy_task(agent: Agent, niche: str, platform: str, goal: str, memory_context: str) -> Task:
    return Task(
        description=f"""
You are the Content Strategist. Your job is to build a complete content strategy.

INPUTS:
- Niche       : {niche}
- Platform    : {platform}
- Growth Goal : {goal}
- Past Context: {memory_context or "No past history — this is a fresh start."}

YOUR DELIVERABLES:
1. TARGET AUDIENCE PROFILE
   - Demographics (age, interests, pain points)
   - What they want to learn/see
   - Their frustrations with existing content

2. CONTENT PILLARS (3–4 pillars)
   - Name each pillar
   - Brief description + why it resonates

3. POSTING STRATEGY
   - Posts per week and best times
   - Content mix (ratio of education/entertainment/promotion)
   - Engagement tactics (polls, CTAs, collabs)

4. WEEKLY CONTENT CALENDAR
   - Use the ContentSchedulerTool to generate a 7-day calendar for {platform}
   - Include: date, time, content type, format, priority

5. GROWTH MILESTONES
   - 30-day, 60-day, 90-day targets
   - Key metrics to track (reach, saves, follower growth rate)

Be specific, actionable, and platform-native. Avoid generic advice.
""",
        expected_output=(
            "A comprehensive content strategy document with: target audience profile, "
            "3–4 content pillars, posting strategy, a 7-day weekly calendar, and "
            "30/60/90-day growth milestones. Formatted clearly with headers."
        ),
        agent=agent,
    )
