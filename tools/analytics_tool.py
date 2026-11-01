"""Analytics Tool — scores content performance and returns recommendations."""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import json


class AnalyticsInput(BaseModel):
    metrics_json: str = Field(
        ..., description="JSON string with: views, likes, comments, shares, saves, followers_gained, content_type."
    )


class AnalyticsTool(BaseTool):
    name: str = "AnalyticsTool"
    description: str = "Scores content performance 0-10 and returns engagement insights + recommendations."
    args_schema: Type[BaseModel] = AnalyticsInput

    def _run(self, metrics_json: str) -> str:
        try:
            m = json.loads(metrics_json)
        except json.JSONDecodeError:
            return "❌ Invalid JSON. Provide metrics as a valid JSON string."

        views = m.get("views", 0)
        if views == 0:
            return "❌ 'views' must be > 0."

        likes    = m.get("likes", 0)
        comments = m.get("comments", 0)
        shares   = m.get("shares", 0)
        saves    = m.get("saves", 0)
        fol      = m.get("followers_gained", 0)
        ctype    = m.get("content_type", "Unknown")

        like_r  = likes / views * 100
        cmt_r   = comments / views * 100
        shr_r   = shares / views * 100
        save_r  = saves / views * 100
        fol_r   = fol / views * 100
        eng     = (likes + comments*2 + shares*3 + saves*3) / views * 100

        score = min(10.0, round(
            (eng/15)*4 + (save_r/5)*3 + (fol_r/2)*2 + (shr_r/3)*1, 1
        ))

        tips = []
        if like_r < 3:   tips.append("⚠️  Hook/thumbnail needs work — like rate is low.")
        if save_r > 3:   tips.append("✅ High save rate — content provides strong value.")
        if shr_r > 1:    tips.append("✅ Above-average shares — content is highly shareable.")
        if cmt_r < 0.5:  tips.append("⚠️  Add a CTA asking viewers to comment.")
        if fol_r > 1:    tips.append("✅ Excellent follower conversion rate.")
        if not tips:     tips.append("📊 Performance within normal range. Keep iterating.")

        return (
            f"📊 PERFORMANCE REPORT | {ctype}\n{'='*50}\n"
            f"Views: {views:,} | Like: {like_r:.1f}% | Comment: {cmt_r:.1f}%\n"
            f"Share: {shr_r:.1f}% | Save: {save_r:.1f}% | Follower gain: {fol_r:.2f}%\n"
            f"Engagement rate: {eng:.2f}%\n\n"
            f"🏆 SCORE: {score}/10 {'⭐'*int(score)}\n\n"
            f"INSIGHTS:\n" + "\n".join(f"  {t}" for t in tips)
        )
