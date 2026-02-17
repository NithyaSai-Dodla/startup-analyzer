# market_agent.py

import os
from serpapi import GoogleSearch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------
# Load API Key
# -------------------------------
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
if not SERPAPI_KEY:
    raise RuntimeError("❌ SERPAPI_KEY not set. Please set it as an environment variable.")

# -------------------------------
# Search competitors using SerpAPI
# -------------------------------
def search_competitors_serpapi(query, num_results=10):
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": num_results
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    competitors = []
    for item in results.get("organic_results", []):
        competitors.append({
            "name": item.get("title"),
            "url": item.get("link"),
            "snippet": item.get("snippet", "")
        })

    return competitors

# -------------------------------
# Compute similarity vs idea
# -------------------------------
def compute_similarity(idea_text, competitors):
    if not competitors:
        return []

    docs = [idea_text] + [c["snippet"] or "" for c in competitors]
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform(docs)
    sims = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()

    for i, score in enumerate(sims):
        competitors[i]["similarity"] = float(score)

    competitors = sorted(competitors, key=lambda x: x["similarity"], reverse=True)
    return competitors

# -------------------------------
# Crowdedness score (0–10)
# -------------------------------
def crowdedness_score(scored_competitors, top_k=5):
    if not scored_competitors:
        return 0.0, "No data"

    top = scored_competitors[:top_k]
    avg_sim = sum(c["similarity"] for c in top) / len(top)

    score = round(avg_sim * 10, 2)  # scale to 0–10

    if score < 3:
        label = "Low competition 🟢"
    elif score < 6:
        label = "Moderate competition 🟡"
    else:
        label = "High competition 🔴"

    return score, label

# -------------------------------
# Main Market Scanner Agent
# -------------------------------
def market_scanner_agent(idea_text, num_results=10):
    print("🔎 Searching competitors...")
    competitors = search_competitors_serpapi(idea_text, num_results=num_results)

    print("🧮 Computing similarity...")
    scored = compute_similarity(idea_text, competitors)

    print("📊 Calculating crowdedness...")
    score, label = crowdedness_score(scored)

    report = {
        "idea": idea_text,
        "crowdedness_score_0_to_10": score,
        "competition_label": label,
        "top_competitors": scored[:5]  # top 5 most similar
    }

    return report

# -------------------------------
# Quick test
# -------------------------------
if __name__ == "__main__":
    test_idea = "An AI tool that analyzes startup ideas"
    out = market_scanner_agent(test_idea)
    print(out)
