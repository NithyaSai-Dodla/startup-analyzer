# ---------------------------------
# ROADMAP AGENT (Phased Execution Plan)
# ---------------------------------

def roadmap_agent(idea_text, market_report=None, trend_report=None, risk_report=None):

    print("\n==============================")
    print("🗺️ ROADMAP PLAN")
    print("==============================")

    # Read signals
    crowdedness = 0
    trend_score = 0
    risks = []

    if market_report:
        crowdedness = market_report.get("crowdedness_score_0_to_10", 0)

    if trend_report:
        trend_score = trend_report.get("trend_score_0_to_10", 0)

    if risk_report:
        risks = risk_report.get("risks", [])

    # -----------------------------
    # Phase 1: Validate
    # -----------------------------
    phase_1 = [
        "Interview 20–30 target users to validate the core problem",
        "Define clear value proposition and target persona",
        "Analyze top 5 competitors and identify gaps",
        "Build simple landing page to test interest"
    ]

    if trend_score < 3:
        phase_1.append("Run deeper market research due to low momentum")

    # -----------------------------
    # Phase 2: Build MVP
    # -----------------------------
    phase_2 = [
        "Design minimal feature set focused on core use-case",
        "Build MVP with focus on usability and reliability",
        "Set up basic analytics and feedback collection",
        "Test with early adopters and iterate quickly"
    ]

    if any("AI" in r for r in risks):
        phase_2.append("Invest extra time in model accuracy and evaluation")

    # -----------------------------
    # Phase 3: Launch
    # -----------------------------
    phase_3 = [
        "Prepare product messaging and positioning",
        "Launch to targeted communities (founders, startups, builders)",
        "Collect user feedback and fix critical issues",
        "Introduce simple pricing or waitlist-based access"
    ]

    if crowdedness >= 6:
        phase_3.append("Emphasize differentiation strongly in marketing")

    # -----------------------------
    # Phase 4: Scale
    # -----------------------------
    phase_4 = [
        "Improve performance, reliability, and UX",
        "Add advanced features based on user demand",
        "Expand marketing channels (content, partnerships, SEO)",
        "Refine monetization and retention strategy"
    ]

    if trend_score >= 7:
        phase_4.append("Invest aggressively in growth and partnerships")

    # -----------------------------
    # Build Roadmap
    # -----------------------------
    roadmap = {
        "Phase 1: Validate": phase_1,
        "Phase 2: Build MVP": phase_2,
        "Phase 3: Launch": phase_3,
        "Phase 4: Scale": phase_4
    }

    # -----------------------------
    # Print Clean Output
    # -----------------------------
    for phase, steps in roadmap.items():
        print(f"\n{phase}")
        print("-" * len(phase))
        for i, step in enumerate(steps, 1):
            print(f"{i}. {step}")

    return {
        "idea": idea_text,
        "roadmap": roadmap
    }
