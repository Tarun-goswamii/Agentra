"""Content Scheduler Tool — generates a weekly posting calendar."""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from datetime import datetime, timedelta

PLATFORM_CFG = {
    "Instagram": {"ppw": 5, "times": ["8 AM", "12 PM", "6 PM"], "formats": ["Reel", "Carousel", "Story"]},
    "TikTok":    {"ppw": 7, "times": ["7 AM", "3 PM", "9 PM"],  "formats": ["Short video", "Duet"]},
    "YouTube":   {"ppw": 3, "times": ["2 PM", "6 PM"],          "formats": ["Short", "Long-form"]},
    "LinkedIn":  {"ppw": 3, "times": ["8 AM", "12 PM"],         "formats": ["Article", "Carousel"]},
    "Twitter":   {"ppw": 7, "times": ["9 AM", "3 PM", "7 PM"],  "formats": ["Thread", "Video"]},
}
CONTENT_TYPES = [
    "Educational / Tutorial", "Motivational / Story", "Tips & Tricks",
    "Behind-the-Scenes", "Myth-busting", "Q&A / Engagement", "Resource List",
]


class SchedulerInput(BaseModel):
    niche: str = Field(..., description="Content niche")
    platform: str = Field(default="Instagram", description="Target platform")


class ContentSchedulerTool(BaseTool):
    name: str = "ContentSchedulerTool"
    description: str = "Generates a 7-day weekly content posting calendar with times and content types."
    args_schema: Type[BaseModel] = SchedulerInput

    def _run(self, niche: str, platform: str = "Instagram") -> str:
        cfg = PLATFORM_CFG.get(platform, PLATFORM_CFG["Instagram"])
        ppw, times, formats = cfg["ppw"], cfg["times"], cfg["formats"]

        today = datetime.now()
        days_ahead = (7 - today.weekday()) % 7 or 7
        week_start = today + timedelta(days=days_ahead)

        step = 7 / ppw
        post_days = sorted(set(int(i * step) for i in range(ppw)))
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        lines = [
            "📅 WEEKLY CONTENT CALENDAR",
            f"Niche: {niche} | Platform: {platform}",
            f"Week of: {week_start.strftime('%B %d, %Y')}",
            "=" * 55,
        ]
        ct_idx = 0
        for d in range(7):
            day = week_start + timedelta(days=d)
            if d in post_days:
                t   = times[ct_idx % len(times)]
                fmt = formats[ct_idx % len(formats)]
                ctype = CONTENT_TYPES[ct_idx % len(CONTENT_TYPES)]
                lines.append(
                    f"\n📌 {day_names[d]}, {day.strftime('%b %d')} — {t}\n"
                    f"   Format : {fmt}\n   Type   : {ctype}"
                )
                ct_idx += 1
            else:
                lines.append(f"\n⬜ {day_names[d]}, {day.strftime('%b %d')} — Engagement / Rest day")

        lines.append(f"\n{'='*55}\nTotal posts: {ppw}/week | Best times: {' | '.join(times)}")
        return "\n".join(lines)
