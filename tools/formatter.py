"""Formatter Tool — cleans and structures agent output."""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import re


class FormatterInput(BaseModel):
    text: str = Field(..., description="Raw text to format.")
    format_type: str = Field(
        default="general",
        description="Format type: 'script', 'caption', 'hashtags', 'calendar', 'general'."
    )


class FormatterTool(BaseTool):
    name: str = "FormatterTool"
    description: str = "Formats raw agent text into clean script/caption/hashtag/calendar output."
    args_schema: Type[BaseModel] = FormatterInput

    def _run(self, text: str, format_type: str = "general") -> str:
        text = text.strip()
        if format_type == "script":
            lines = [l.rstrip() for l in text.splitlines() if l.strip()]
            body = "\n".join(lines)
            if "HOOK" not in body.upper():
                body = "🎬 HOOK:\n" + body
            return f"{'='*50}\n📽️  REEL SCRIPT\n{'='*50}\n\n{body}\n\n{'='*50}"
        elif format_type == "caption":
            cleaned = re.sub(r'\n{3,}', '\n\n', text).strip()
            return f"📝 CAPTION:\n{'─'*40}\n{cleaned}\n{'─'*40}"
        elif format_type == "hashtags":
            tags = re.findall(r'#\w+', text)
            if not tags:
                tags = [f"#{w.lower()}" for w in re.findall(r'\b\w{3,}\b', text)[:15]]
            unique = list(dict.fromkeys(tags))
            groups = [" ".join(unique[i:i+5]) for i in range(0, len(unique), 5)]
            return f"#️⃣  HASHTAGS ({len(unique)}):\n  " + "\n  ".join(groups)
        else:
            return re.sub(r'\n{3,}', '\n\n', text).strip()
