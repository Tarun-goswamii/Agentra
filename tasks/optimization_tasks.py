"""Optimization Task — rewrites content for maximum engagement."""

from crewai import Task
from crewai import Agent


def build_optimization_task(agent: Agent, platform: str) -> Task:
    return Task(
        description=f"""
You are the Engagement Optimizer. Take the 3 reels from the Content Creator and make them exceptional.

PLATFORM: {platform}

For EACH of the 3 reels, apply the following optimization framework:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPTIMIZED REEL [N]: [Title]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 OPTIMIZATION CHANGES:
[List every specific change made and why — be precise]

🎬 OPTIMIZED HOOK:
[Rewritten hook — more scroll-stopping, pattern-interrupt, or curiosity-driving]
Reason: [Why this version is better]

📽️ OPTIMIZED SCRIPT:
[Full rewritten script — tighter pacing, clearer value, stronger CTA]
Key changes: [Brief notes on what changed]

📝 OPTIMIZED CAPTION:
[Rewritten caption — better line breaks, stronger opening, emotional hook, clear CTA]

#️⃣ OPTIMIZED HASHTAGS:
[Refined hashtag set — removed low-ROI tags, added high-reach tags]

💪 STRONG CTA ADDED:
[The specific call-to-action and why it will drive comments/saves/shares]

📊 PREDICTED ENGAGEMENT SCORE: [X/10]
Reasoning: [Brief justification based on hook strength, CTA, value delivery]

OPTIMIZATION PRINCIPLES TO APPLY:
- Pattern interrupt: Does the first frame stop the scroll?
- Clarity: Is the value proposition clear in 3 seconds?
- Pacing: Is every sentence necessary? Cut fluff ruthlessly.
- CTA: Is there ONE clear action the viewer should take?
- Captions: Do they have line breaks for mobile readability?
- Hashtag hygiene: Mix of 500K–5M posts (niche) + 10M+ (broad)

After all 3 optimized reels, provide:
OVERALL CONTENT BATCH SCORE: [X/10]
TOP 3 STRENGTHS of this content batch
TOP 3 AREAS TO IMPROVE for next batch
""",
        expected_output=(
            "Three fully optimized reels with rewritten hooks, scripts, captions, and hashtags. "
            "Each with a predicted engagement score and specific optimization notes. "
            "Followed by an overall batch score and 3 strengths + 3 improvement areas."
        ),
        agent=agent,
    )
