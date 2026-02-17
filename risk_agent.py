import json
from llm import call_llm   # your Ollama wrapper

# ---------------------------------
# DYNAMIC + LLM-ENHANCED RISK AGENT
# ---------------------------------

def risk_agent(idea_text, market_report=None, trend_report=None):

    risks = []

    print("\n==============================")
    print("⚠️ RISK ANALYSIS REPORT")
    print("==============================")

    # ---------------------------------
    # 1️⃣ Competition Risk (Dynamic)
    # ---------------------------------
    if market_report:
        crowdedness = market_report.get("crowdedness_score_0_to_10", 0)

        if crowdedness >= 8:
            risks.append("Extremely crowded market — strong moat required")
        elif crowdedness >= 6:
            risks.append("High competition — clear differentiation needed")
        elif crowdedness >= 3:
            risks.append("Moderate competition — positioning matters")
        else:
            risks.append("Low competition — validate actual demand carefully")

    # ---------------------------------
    # 2️⃣ Trend Risk (Dynamic)
    # ---------------------------------
    if trend_report:
        trend_score = trend_report.get("trend_score_0_to_10", 0)
        keywords = trend_report.get("strong_keywords", [])

        if trend_score >= 7:
            risks.append("High growth market — risk of rapid new entrants")
        elif trend_score >= 4:
            risks.append("Moderate growth — sustainable but competitive")
        elif trend_score >= 2:
            risks.append("Slow growth — may require strong GTM strategy")
        else:
            risks.append("Low demand momentum — validate user pain deeply")

        if not keywords:
            risks.append("Weak keyword signals — unclear search demand")

    # ---------------------------------
    # 3️⃣ Technical / Execution Risk
    # ---------------------------------
    idea_lower = idea_text.lower()

    if "ai" in idea_lower:
        risks.append("AI reliability and model accuracy risk")

    if "automation" in idea_lower:
        risks.append("Automation errors may reduce user trust")

    # ---------------------------------
    # 4️⃣ Business Model Risk
    # ---------------------------------
    risks.append("Revenue model must align with customer willingness to pay")

    # ---------------------------------
    # 5️⃣ Early Customer Risk
    # ---------------------------------
    if "startup" in idea_lower:
        risks.append("Early-stage founders may have budget constraints")

    # ---------------------------------
    # 6️⃣ LLM ENHANCEMENT LAYER (Ollama)
    # ---------------------------------
    prompt = f"""
You are a startup risk analyst.

Idea:
{idea_text}

Market report:
{market_report}

Trend report:
{trend_report}

Current identified risks:
{risks}

Task:
- Add any missing important risks
- Refine wording
- Remove duplicates
- Keep it concise and realistic

IMPORTANT:
Return ONLY valid JSON in this exact format. No explanation. No markdown. No text outside JSON.

{{
  "risks": [
    "risk 1",
    "risk 2",
    "risk 3"
  ]
}}
"""

    llm_output = call_llm(prompt)

    # 🔍 DEBUG: Show raw LLM output
    print("\n--- RAW LLM OUTPUT ---")
    print(llm_output)
    print("----------------------\n")

    llm_risks = []

    if llm_output and llm_output.strip():
        try:
            llm_data = json.loads(llm_output)
            if isinstance(llm_data, dict) and "risks" in llm_data:
                llm_risks = llm_data.get("risks", [])
            else:
                print("⚠️ LLM returned JSON but not in expected format.")
        except Exception as e:
            print("⚠️ LLM did not return valid JSON, using rule-based risks only.")
            print("⚠️ JSON parse error:", e)
    else:
        print("⚠️ LLM returned empty output, using rule-based risks only.")

    # ---------------------------------
    # 7️⃣ Merge + Deduplicate
    # ---------------------------------
    final_risks = list(dict.fromkeys(risks + llm_risks))  # preserves order, removes duplicates

    # ---------------------------------
    # 8️⃣ Print Output
    # ---------------------------------
    for i, risk in enumerate(final_risks, 1):
        print(f"{i}. {risk}")

    return {
        "idea": idea_text,
        "risk_count": len(final_risks),
        "risks": final_risks
    }
