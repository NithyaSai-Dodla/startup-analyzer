import sys
sys.stdout.reconfigure(encoding="utf-8", errors="ignore")

from orchestrator_crewai import run_with_crewai


def main():
    idea = "An AI tool that analyzes startup ideas and provides automated market validation and roadmap insights"

    print("====================================")
    print("🚀 STARTUP ANALYZER (CrewAI + Ollama)")
    print("====================================\n")

    final_output = run_with_crewai(idea)

    print("\n================ FINAL OUTPUT ================\n")

    for section, content in final_output.items():
        print(f"\n--- {section.upper()} ---")
        print(content)

if __name__ == "__main__":
    main()
