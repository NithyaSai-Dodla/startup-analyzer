# orchestrator_crewai.py

# ----------------------------
# IMPORTS
# ----------------------------
# CrewAI is optional here – we keep it only for structure/logging
try:
    from crewai import Agent
    from crewai.llm import LLM
    CREWAI_AVAILABLE = True
except Exception as e:
    print("⚠️ CrewAI not fully available, running without Agent wrapper.")
    CREWAI_AVAILABLE = False

# Import your agent functions
from market_agent import market_scanner_agent
from trend_agent import trend_agent_smart
from risk_agent import risk_agent
from strategy_agent import strategy_agent
from roadmap_agent import roadmap_agent


# ----------------------------
# OPTIONAL: LLM SETUP (Ollama)
# ----------------------------
# Your pipeline DOES NOT depend on this to run.
# It is only used if you want CrewAI Agent objects.

ollama_llm = None
market_agent = None

if CREWAI_AVAILABLE:
    try:
        ollama_llm = LLM(
            model="ollama/llama3",      # or "ollama/mistral"
            api_key="ollama",           # dummy value, Ollama ignores it
            base_url="http://localhost:11434/v1"
        )

        market_agent = Agent(
            role="Market Analyst",
            goal="Analyze competition and market landscape",
            backstory="Expert in markets and competitive analysis",
            llm=ollama_llm,
            verbose=True
        )

        print("✅ CrewAI + Ollama initialized")

    except Exception as e:
        print("⚠️ CrewAI LLM init failed, continuing without it.")
        print("Reason:", e)
        CREWAI_AVAILABLE = False


# ----------------------------
# TASK WRAPPERS
# ----------------------------
def run_market_task(idea):
    return market_scanner_agent(idea)

def run_trend_task(idea):
    return trend_agent_smart(idea)

def run_risk_task(idea, market_report, trend_report):
    return risk_agent(idea, market_report, trend_report)

def run_strategy_task(idea, market_report, trend_report, risk_report):
    return strategy_agent(idea, market_report, trend_report, risk_report)

def run_roadmap_task(idea, market_report, trend_report, risk_report):
    return roadmap_agent(idea, market_report, trend_report, risk_report)


# ----------------------------
# ORCHESTRATOR
# ----------------------------
def run_with_crewai(idea):
    print("🚀 Running Startup Analyzer Pipeline...")

    # Task 1: Market
    market_report = run_market_task(idea)

    # Task 2: Trend
    trend_report = run_trend_task(idea)

    # Task 3: Risk
    risk_report = run_risk_task(idea, market_report, trend_report)

    # Task 4: Strategy
    strategy_report = run_strategy_task(idea, market_report, trend_report, risk_report)

    # Task 5: Roadmap
    roadmap_report = run_roadmap_task(idea, market_report, trend_report, risk_report)

    return {
        "idea": idea,
        "market_report": market_report,
        "trend_report": trend_report,
        "risk_report": risk_report,
        "strategy_report": strategy_report,
        "roadmap_report": roadmap_report
    }


# ----------------------------
# TEST RUN
# ----------------------------
if __name__ == "__main__":
    idea = "An AI tool that analyzes startup ideas and provides automated market validation and roadmap insights"

    final_output = run_with_crewai(idea)

    print("\n================ FINAL OUTPUT ================\n")
    for k, v in final_output.items():
        print(f"\n--- {k.upper()} ---")
        print(v)
