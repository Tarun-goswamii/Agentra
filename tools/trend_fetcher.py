"""Trend Fetcher Tool — returns trending topics, hooks, and hashtags for a niche."""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from datetime import datetime
import random

TREND_DATABASE: dict = {
    "coding for beginners": {
        "trending_topics": [
            "Python in 60 seconds", "Top 5 beginner mistakes", "Day in the life of a dev",
            "Build your first app in 10 minutes", "Why 90% quit coding (and how not to)",
            "Free resources that replaced my $3000 bootcamp", "VS Code tips no one tells beginners",
        ],
        "viral_hooks": [
            "I learned to code in 30 days — here's what actually worked",
            "Stop doing THIS if you're a beginner coder",
            "The ONE thing that made coding click for me",
            "Nobody talks about this part of learning to code",
        ],
        "trending_hashtags": [
            "#coding", "#learntocode", "#python", "#webdev", "#codingforbeginners",
            "#developerlife", "#programming", "#codingtips", "#techcareer", "#100daysofcode",
        ],
        "content_formats": ["tutorial", "myth-busting", "day-in-life", "resource-list"],
    },
    "fitness": {
        "trending_topics": [
            "5-minute morning routine", "Gym mistakes beginners make",
            "No-equipment workouts", "What I eat in a day",
        ],
        "viral_hooks": [
            "I worked out every day for 30 days — here's what happened",
            "You don't need a gym to get fit",
        ],
        "trending_hashtags": ["#fitness", "#gym", "#workout", "#fitnessmotivation", "#healthylifestyle"],
        "content_formats": ["transformation", "routine", "myth-busting"],
    },
    "personal finance": {
        "trending_topics": [
            "How I saved $10k on a $40k salary", "Money habits in your 20s",
            "Stop wasting money on these 5 things",
        ],
        "viral_hooks": [
            "I was broke at 22. Here's exactly what I changed.",
            "The money advice no one gives you in school",
        ],
        "trending_hashtags": ["#personalfinance", "#moneytips", "#investing", "#savingmoney"],
        "content_formats": ["story", "list", "myth-busting"],
    },
}

_DEFAULT = {
    "trending_topics": ["Top 5 things about your niche", "A day in the life", "Myth vs. fact",
                        "Tools I use every day", "My honest review"],
    "viral_hooks": ["Nobody talks about this...", "I tried this for 30 days",
                    "Stop making this mistake", "This changed everything for me"],
    "trending_hashtags": ["#viral", "#trending", "#tips", "#howto", "#fyp"],
    "content_formats": ["tutorial", "story", "list"],
}


class TrendFetcherInput(BaseModel):
    niche: str = Field(..., description="Content niche to fetch trends for")
    platform: str = Field(default="Instagram", description="Target platform")
    num_topics: int = Field(default=5, description="Number of topics to return")


class TrendFetcherTool(BaseTool):
    name: str = "TrendFetcherTool"
    description: str = "Fetches trending topics, viral hooks, and hashtags for a given niche."
    args_schema: Type[BaseModel] = TrendFetcherInput

    def _run(self, niche: str, platform: str = "Instagram", num_topics: int = 5) -> str:
        trends = TREND_DATABASE.get(niche.lower().strip(), _DEFAULT)
        topics  = random.sample(trends["trending_topics"], min(num_topics, len(trends["trending_topics"])))
        hooks   = random.sample(trends["viral_hooks"], min(3, len(trends["viral_hooks"])))
        hashtags = trends["trending_hashtags"][:10]

        return (
            f"📈 TREND REPORT — {niche.title()} | {platform} | {datetime.now().strftime('%B %Y')}\n"
            f"{'='*55}\n\n"
            f"🔥 TRENDING TOPICS:\n" +
            "\n".join(f"  {i+1}. {t}" for i, t in enumerate(topics)) +
            f"\n\n🎣 VIRAL HOOKS:\n" +
            "\n".join(f'  • "{h}"' for h in hooks) +
            f"\n\n#️⃣ TOP HASHTAGS:\n  {' '.join(hashtags)}\n\n"
            f"📋 BEST FORMATS: {', '.join(trends['content_formats'])}\n\n"
            f"💡 TIP: Reels 15–30s perform 2× better. Front-load value in first 2 seconds."
        )
