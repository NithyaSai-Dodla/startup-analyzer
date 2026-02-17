import warnings, time, re
warnings.filterwarnings("ignore")

from pytrends.request import TrendReq
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd


# ---------------------------------
# STEP 1: Smarter Keyword Extraction
# ---------------------------------
def extract_keywords_smart(idea_text, top_n=4):
    idea_text = idea_text.lower()
    idea_text = re.sub(r'[^a-zA-Z\s]', '', idea_text)

    stop_words_extra = [
        "build", "create", "make", "provide", "provides",
        "analyze", "analyzes", "automated", "tool",
        "system", "platform"
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(2,3),
        max_features=30
    )

    X = vectorizer.fit_transform([idea_text])
    scores = zip(vectorizer.get_feature_names_out(), X.toarray()[0])
    sorted_keywords = sorted(scores, key=lambda x: x[1], reverse=True)

    keywords = []
    for word, score in sorted_keywords:
        if any(bad in word for bad in stop_words_extra):
            continue
        if len(word.split()) < 2:
            continue
        keywords.append(word)

    return keywords[:top_n]


# ---------------------------------
# STEP 2: Fetch Google Trends (Rate-limit safe)
# ---------------------------------
def get_trends(keywords, retries=3):
    pytrends = TrendReq(hl="en-US", tz=330)

    for attempt in range(retries):
        try:
            time.sleep(6)  # ⏳ wait to avoid rate limit
            pytrends.build_payload(keywords, timeframe="today 12-m")
            return pytrends.interest_over_time()
        except Exception as e:
            print(f"⚠️ Google Trends error, retrying... ({attempt+1}/{retries})")
            time.sleep(10)

    print("❌ Failed to fetch trends after retries.")
    return pd.DataFrame()


# ---------------------------------
# STEP 3: Market-Aware Trend Analysis
# ---------------------------------
def analyze_trends_smart(trend_df):

    if trend_df.empty:
        print("No trend data found.")
        return

    strong_keywords = []
    total_growth = 0
    total_avg = 0
    count = 0

    for col in trend_df.columns:
        if col == "isPartial":
            continue

        series = trend_df[col]
        growth = float(series.iloc[-1] - series.iloc[0])
        avg_interest = float(series.mean())

        # Ignore weak signals
        if avg_interest < 5:
            continue

        strong_keywords.append(col)
        total_growth += growth
        total_avg += avg_interest
        count += 1

        print(f"\nKeyword: {col}")
        print(f"  Avg Interest: {round(avg_interest,2)}")
        print(f"  Growth: {round(growth,2)}")

    if count == 0:
        print("\nAll keywords had weak search volume.")
        return

    avg_growth = total_growth / count
    avg_interest = total_avg / count

    # Scoring
    normalized_interest = min(avg_interest / 50, 1) * 6
    normalized_growth = min(max(avg_growth, 0) / 30, 1) * 4
    final_score = round(normalized_interest + normalized_growth, 2)

    if final_score > 7:
        label = "Hot Opportunity 🔥"
    elif final_score > 4:
        label = "Growing Market 📈"
    elif final_score > 2:
        label = "Moderate / Niche 😐"
    else:
        label = "Low Momentum 📉"

    print("\n==============================")
    print("SMART TREND SUMMARY")
    print("==============================")
    print("Strong Keywords Used:", strong_keywords)
    print("Average Interest:", round(avg_interest,2))
    print("Average Growth:", round(avg_growth,2))
    print("Trend Score (0–10):", final_score)
    print("Classification:", label)

    return {
        "trend_score_0_to_10": final_score,
        "classification": label,
        "strong_keywords": strong_keywords
    }


# ---------------------------------
# MAIN TREND AGENT
# ---------------------------------
def trend_agent_smart(idea_text):

    print("\n🧠 Extracting smart market-aware keywords...")
    keywords = extract_keywords_smart(idea_text)
    print("Candidate Keywords:", keywords)

    if not keywords:
        print("No meaningful keywords extracted.")
        return None

    print("\n📈 Fetching Google Trends data...")
    trend_data = get_trends(keywords)

    print("\n📊 Analyzing trends...")
    result = analyze_trends_smart(trend_data)

    return result
