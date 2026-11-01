"""LLM Factory — returns the configured LLM (AMD vLLM primary, Groq fallback)."""

import os
import requests
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()


def get_llm():
    """
    Tries to connect to AMD vLLM first. If it's a placeholder or unreachable,
    automatically falls back to Groq API using a fast model with higher limits.
    """
    amd_url = os.getenv("AMD_BASE_URL", "http://YOUR_AMD_INSTANCE_IP:8000/v1")
    
    # 1. Check if AMD is configured and reachable
    if "YOUR_AMD_INSTANCE_IP" not in amd_url:
        try:
            # Quick health check to vLLM models endpoint
            r = requests.get(f"{amd_url}/models", timeout=2)
            if r.status_code == 200:
                print("✅ Connected to AMD vLLM Backend.")
                return _build_amd_llm(amd_url)
        except requests.RequestException:
            print("⚠️ AMD endpoint unreachable. Falling back to Groq...")
            pass
    else:
        print("⚠️ AMD IP not configured. Falling back to Groq...")

    # 2. Fallback to Groq
    return _build_groq_llm()


def _build_amd_llm(base_url):
    """AMD Developer Cloud — vLLM OpenAI-compatible endpoint."""
    model    = os.getenv("AMD_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")
    api_key  = os.getenv("AMD_API_KEY", "EMPTY")

    return LLM(
        model=f"openai/{model}",
        api_key=api_key,
        base_url=base_url,
        temperature=0.7,
        max_tokens=1024,
        timeout=120,
    )


def _build_groq_llm():
    """Groq cloud inference — fallback for local development."""
    api_key = os.getenv("GROQ_API_KEY", "")
    
    # Use Mixtral. It has a high rate limit on the free tier and is 
    # much more reliable at tool execution than the 8B models.
    model = "mixtral-8x7b-32768"

    if not api_key:
        raise ValueError(
            "❌ No AMD endpoint available AND no GROQ_API_KEY provided in .env!"
        )

    print(f"✅ Using Groq Fallback Backend ({model}).")
    return LLM(
        model=f"groq/{model}",
        api_key=api_key,
        temperature=0.7,
        max_tokens=1024,
    )
