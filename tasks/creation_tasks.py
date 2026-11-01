"""Creation Task — generates 3 complete reels (script + caption + hashtags)."""

from crewai import Task
from crewai import Agent


def build_creation_task(agent: Agent, niche: str, platform: str) -> Task:
    return Task(
        description=f"""
You are the Content Creator. Use the strategy and research from previous agents to create content.

INPUTS:
- Niche    : {niche}
- Platform : {platform}
- Context  : Use the content ideas, hooks, and strategy from previous task outputs.

YOUR DELIVERABLES:
Generate exactly 3 complete reels. Use the top 3 content ideas from the research.

For EACH reel (label them REEL 1, REEL 2, REEL 3), provide:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REEL [N]: [Title]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 CONCEPT:
[1-sentence description of the reel idea]

🎬 HOOK (first 2 seconds):
[The exact opening line that stops scrolling — max 10 words]

📽️ FULL SCRIPT (15–30 seconds when read aloud):
[Beat 1]: [Opening — expand on the hook, 2–3 sentences]
[Beat 2]: [Main content — core value/insight, 3–5 sentences]
[Beat 3]: [CTA/Closing — what to do next, 1–2 sentences]

📊 VISUAL DIRECTION:
[Brief notes on what to show on screen at each beat]

📝 CAPTION (for {platform}):
[3–5 lines. First line must be hook-worthy. Include a question or CTA at the end.]

#️⃣ HASHTAGS:
[15–20 hashtags, mix of niche, broad, and emerging]

🎯 TARGET EMOTION: [Curiosity / Inspiration / FOMO / Surprise / Relatability]
📈 BEST TIME TO POST: [Based on {platform} algorithm behavior]

Make each reel feel human, conversational, and authentic — not robotic or generic.
""",
        expected_output=(
            "Three complete reels, each with: concept, hook, full script with beats, "
            "visual direction notes, caption, 15-20 hashtags, target emotion, and best posting time. "
            "Clearly labeled REEL 1, REEL 2, REEL 3."
        ),
        agent=agent,
    )
