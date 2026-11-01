# 🚀 Agentra: AI Content Creator System

**Agentra** is an autonomous, multi-agent content creation pipeline designed to act as your personal AI content team. Powered by **CrewAI** and featuring a sleek **Streamlit** user interface, Agentra handles the entire content lifecycle from strategy and research to scripting, optimization, and feedback.

The system is optimized to run on the **AMD Developer Cloud** (via vLLM on ROCm) for high-performance local inference, with a seamless fallback to the **Groq Cloud API** for instant generation.

---

## ✨ Features

- **🤖 5-Agent Collaborative Pipeline**: Mimics a real-world content marketing team.
- **🧠 Persistent Memory System**: Tracks past performance, learns from high-performing posts, and logs your specific content niches.
- **🎨 Premium UI/UX**: A responsive, glassmorphic Streamlit interface with live progress tracking and organized output tabs.
- **⚙️ Custom Tools**: Equipped with mock APIs for Trend Fetching, Content Scheduling, and Analytics scoring.
- **☁️ Auto-Fallback Architecture**: Connects directly to an OpenAI-compatible AMD server, but instantly fails over to Groq's high-speed Mixture-of-Experts models if the local server is offline.

---

## 🏗️ The Agent Team

1. **🎯 Strategist**: Analyzes your niche and target audience to build a complete content strategy and a 7-day posting calendar.
2. **🔍 Researcher**: Identifies viral hooks, trending formats, and content gaps using the `TrendFetcherTool`.
3. **✍️ Creator**: Generates 3 full-length short-form video scripts (Reels/TikToks) complete with screen directions and optimized captions.
4. **⚡ Optimizer**: Acts as the editor. Tightens the pacing, punches up the hooks, and ensures strong Calls to Action (CTAs).
5. **📊 Feedback**: Analyzes past performance data (using the `AnalyticsTool`) and updates the long-term memory to improve future generations.

---

## 🚀 Setup & Installation

### 1. Clone & Install Dependencies
Ensure you have Python 3.10+ installed.

```bash
git clone https://github.com/yourusername/agentra.git
cd agentra
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy the `.env.example` file to `.env`:

```bash
cp .env.example .env
```

Open `.env` and configure your API keys and endpoints:
- Set `LLM_BACKEND=amd` to use your AMD instance, or `LLM_BACKEND=groq` to use Groq.
- If using Groq, provide your free API key: `GROQ_API_KEY=gsk_your_key_here`.
- If using AMD Cloud, update the `AMD_BASE_URL` with your instance's IP address.

*(See the `amd_setup/AMD_SETUP_GUIDE.md` for full instructions on provisioning your AMD Instinct GPU server with ROCm and vLLM).*

### 3. Run the Application
Launch the Agentra Streamlit UI:

```bash
streamlit run app.py
```
The application will automatically open in your browser at `http://localhost:8501`.

---

## 📂 Project Structure

```text
agentra/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env                    # Environment configuration
├── agents/                 # CrewAI Agent definitions
├── tasks/                  # CrewAI Task definitions
├── tools/                  # Custom tools (TrendFetcher, Scheduler, etc.)
├── pipeline/               # Crew execution and orchestration logic
├── memory/                 # JSON-based persistent memory system
├── ui/                     # UI modules (styles, sidebar, components)
└── amd_setup/              # Scripts for deploying vLLM on AMD Cloud
```

---

## 🛠️ Tech Stack
- **Orchestration**: [CrewAI](https://www.crewai.com/)
- **Frontend UI**: [Streamlit](https://streamlit.io/)
- **LLM Infrastructure**: LangChain, LiteLLM
- **Inference Engines**: AMD ROCm / vLLM, Groq API
