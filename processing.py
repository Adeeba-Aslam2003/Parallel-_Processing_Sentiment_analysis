# processing.py
import pandas as pd
from textblob import TextBlob

# ---- Lazy load LLM (only when used) ----
_MODEL = None
_LLMDONE = False

def _load_llm():
    """Try to load a small HuggingFace sentiment pipeline on first use."""
    global _MODEL, _LLMDONE
    if _LLMDONE:
        return _MODEL
    try:
        from transformers import pipeline
        # default is distilbert-base-uncased-finetuned-sst-2-english
        _MODEL = pipeline("sentiment-analysis")
    except Exception:
        _MODEL = None
    _LLMDONE = True
    return _MODEL

# ---- Single text analyzers ----
def analyze_textblob(text: str):
    text = (text or "").strip()
    if not text:
        return "neutral", 0.0
    pol = TextBlob(text).sentiment.polarity
    if pol > 0:
        return "positive", float(pol)
    if pol < 0:
        return "negative", float(-pol)
    return "neutral", 0.0

def analyze_llm(text: str):
    text = (text or "").strip()
    if not text:
        return "neutral", 0.0
    model = _load_llm()
    if model is None:
        # LLM not available; fall back
        return "unavailable", 0.0
    r = model(text)[0]
    return r["label"].lower(), float(r["score"])

# Keep this name because your app imports it
def analyze_sentiment(text: str):
    # Default to TextBlob; your UI can still call analyze_llm for compare
    return analyze_textblob(text)

# ---- CSV processing (compare TextBlob vs LLM) ----
def process_csv(file_like):
    """
    Expects a CSV with a 'text' column. Returns a DataFrame:
    [text, TextBlob Sentiment, TextBlob Confidence, LLM Sentiment, LLM Confidence]
    If LLM not available, LLM columns are 'unavailable'/0.0.
    """
    df = pd.read_csv(file_like)
    if "text" not in df.columns:
        raise ValueError("CSV must contain a 'text' column")

    out = []
    for t in df["text"].astype(str):
        tb_s, tb_c = analyze_textblob(t)
        llm_s, llm_c = analyze_llm(t)
        out.append({
            "text": t,
            "TextBlob Sentiment": tb_s,
            "TextBlob Confidence": tb_c,
            "LLM Sentiment": llm_s,
            "LLM Confidence": llm_c,
        })
    return pd.DataFrame(out)
