import json
from llm import call_llm  # your Ollama wrapper

# ---------------------------------
# STRATEGY AGENT (Rules + LLM Enhancer)
# ---------------------------------

def strategy_agent(idea_text, market_report=None, trend_report=None, risk_report=None):

    strategies = []

    print("\n==============================")
    print("💡 STRATEGY REPORT")
    print("==============================")

    crowdedness = 0
    trend_score = 0

    if market_report:
        crowdedness = market_report.get("crowdedness_score_0_to_10", 0)

    if trend_report:
        trend_score = trend_report.get("trend_score_0_to_10", 0)

    # ---------------------------------
    # 1️⃣ Competition-Based Strategy
    # ---------------------------------
    if crowdedness >= 7:
        strategies.append("Focus on niche segment instead of broad market")
        strategies.append("Build strong differentiation through unique features")
    elif crowdedness >= 4:
        strategies.append("Position clearly against top competitors")
        strategies.append("Emphasize superior UX and execution")
    else:
        strategies.append("Move fast to capture early market share")
        strategies.append("Educate market to increase demand awareness")

    # ---------------------------------
    # 2️⃣ Trend-Based Strategy
    # ---------------------------------
    if trend_score >= 7:
        strategies.append("Leverage growth momentum with aggressive marketing")
        strategies.append("Raise funding early to scale quickly")
    elif trend_score >= 4:
        strategies.append("Adopt steady growth strategy with focused GTM")
    else:
        strategies.append("Validate demand deeply before heavy investment")

    # ---------------------------------
    # 3️⃣ Risk-Based Strategy
    # ---------------------------------
    if risk_report:
        risks = risk_report.get("risks", [])
        for r in risks:
            if "AI" in r:
                strategies.append("Invest heavily in model accuracy and reliability")
            if "competition" in r.lower():
                strategies.append("Build brand authority and thought leadership")
            if "budget" in r.lower():
                strategies.append("Offer freemium or low-cost entry tier")

    # ---------------------------------
    # 4️⃣ Idea-Based Strategy
    # ---------------------------------
    idea_lower = idea_text.lower()

    if "ai" in idea_lower:
        strategies.append("Position as AI-powered but human-supervised tool")

    if "startup" in idea_lower:
        strategies.append("Partner with incubators and startup communities")

    if "market" in idea_lower:
        strategies.append("Provide data-backed insights as core value proposition")

    # ---------------------------------
    # 5️⃣ LLM ENHANCEMENT: Add Missing Angles
    # ---------------------------------
    prompt = f"""
You are a startup strategy expert.

Idea: {idea_text}
Market report: {market_report}
Trend report: {trend_report}
Risk report: {risk_report}

Current strategies:
{strategies}

Task:
- Add missing strategic angles such as:
  - Partnerships
  - Pricing & monetization
  - Compliance / trust / credibility
  - Distribution channels
  - Operations / execution
- Refine wording
- Remove duplicates
- Keep it practical and concise

Return ONLY JSON:
{{
  "strategies": [
    "strategy 1",
    "strategy 2",
    "strategy 3"
  ]
}}
"""

    llm_output = call_llm(prompt)

    try:
        llm_data = json.loads(llm_output)
        llm_strategies = llm_data.get("strategies", [])
    except:
        print("⚠️ LLM did not return valid JSON, using rule-based strategies only.")
        llm_strategies = []

    # ---------------------------------
    # 6️⃣ Merge + Deduplicate
    # ---------------------------------
    final_strategies = list(set(strategies + llm_strategies))

    # ---------------------------------
    # 7️⃣ Print Output
    # ---------------------------------
    for i, strategy in enumerate(final_strategies, 1):
        print(f"{i}. {strategy}")

    return {
        "idea": idea_text,
        "strategy_count": len(final_strategies),
        "strategies": final_strategies
    }
