import requests

# -------------------------------
# Ollama Configuration
# -------------------------------
OLLAMA_URL = "http://localhost:11434/api/generate"

# Use a faster model by default (change to "llama3" if your machine is strong)
MODEL = "mistral"

# Increase timeout because local models can be slow on first run
TIMEOUT_SECONDS = 300  # 5 minutes


def call_llm(prompt: str) -> str:
    """
    Calls Ollama locally and returns the model response as text.
    If Ollama is slow or fails, returns an empty string so the app can fallback safely.
    """

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2
        }
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT_SECONDS)
        r.raise_for_status()
        data = r.json()
        return data.get("response", "").strip()

    except requests.exceptions.Timeout:
        print("⚠️ Ollama request timed out. Using fallback logic.")
        return ""

    except requests.exceptions.ConnectionError:
        print("⚠️ Could not connect to Ollama. Is `ollama serve` running?")
        return ""

    except Exception as e:
        print(f"⚠️ Ollama error: {e}")
        return ""
