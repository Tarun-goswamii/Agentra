"""Strategist Agent — niche strategy + weekly content calendar."""

from crewai import Agent
from tools.content_scheduler import ContentSchedulerTool
from tools.formatter import FormatterTool


def build_strategist(llm) -> Agent:
    return Agent(
        role="Content Strategist",
        goal=(
            "Define a laser-focused content strategy for the given niche and platform. "
            "Identify the target audience, content pillars, posting frequency, and overarching goal. "
            "Produce a structured weekly content calendar that maximizes growth."
        ),
        backstory=(
            "You are a seasoned social media strategist with 10+ years growing accounts "
            "from zero to hundreds of thousands of followers across Instagram, TikTok, and YouTube. "
            "You understand audience psychology, platform algorithms, and viral content principles. "
            "You are data-driven, creative, and obsessed with measurable results. "
            "Your strategies have helped 50+ creators reach monetization milestones."
        ),
        tools=[ContentSchedulerTool(), FormatterTool()],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3,
    )
