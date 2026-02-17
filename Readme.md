# 🚀 Startup Idea Analyzer (CrewAI + Ollama)

An agentic system that analyzes startup ideas and generates:
- 📊 Market competition insights
- 📈 Trend analysis (Google Trends)
- ⚠️ Risk assessment
- 💡 Strategy recommendations
- 🗺️ Phased execution roadmap

The project uses a **hybrid architecture**:
- Real data where it matters (Market + Trends)
- Local LLM (Ollama) for reasoning, enrichment, and refinement
- CrewAI-style orchestration to run the pipeline

---

## ✨ Features

- 🔎 **Market Agent (API-based)**  
  Uses SerpAPI + TF-IDF similarity to estimate competition and market crowdedness.

- 📈 **Trend Agent (Data-based, no paid API)**  
  Uses `pytrends` to analyze Google Trends and compute a trend score.

- ⚠️ **Risk Agent (Hybrid: Rules + LLM)**  
  Combines deterministic rules with Ollama LLM to enrich and refine risks.

- 💡 **Strategy Agent (Hybrid: Rules + LLM)**  
  Generates core strategies from signals and uses LLM to add missing angles:
  - Partnerships
  - Pricing & monetization
  - Compliance & trust
  - Distribution & GTM
  - Operations & execution

- 🗺️ **Roadmap Agent (Rule-based)**  
  Produces a phased execution plan: Validate → Build → Launch → Scale.

- 🧠 **Local LLM via Ollama**  
  No paid LLM APIs required for reasoning agents.

- 🧩 **CrewAI Orchestrator**  
  Runs all agents in sequence and collects the final report.

---

## 🧱 Tech Stack

- **Language:** Python 3.10+
- **Orchestration:** CrewAI
- **LLM (Local):** Ollama (e.g., llama3, mistral, qwen, etc.)
- **Market Data:** SerpAPI + scikit-learn (TF-IDF, cosine similarity)
- **Trend Data:** pytrends (Google Trends)
- **Data / Utils:** pandas, numpy, requests
- **Environment:** VS Code / any Python IDE

---

