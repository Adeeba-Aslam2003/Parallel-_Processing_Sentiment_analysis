import pandas as pd
from textblob import TextBlob
from transformers import pipeline

# Load the LLM model (Hugging Face DistilBERT)
_sentiment_model = pipeline("sentiment-analysis")

def analyze_sentiment(text):
    """Fallback function name kept for compatibility"""
    return analyze_textblob(text)

def analyze_textblob(text):
    if not text.strip():
        return "neutral", 0.0
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "positive", polarity
    elif polarity < 0:
        return "negative", -polarity
    else:
        return "neutral", 0.0

def analyze_llm(text):
    if not text.strip():
        return "neutral", 0.0
    result = _sentiment_model(text)[0]
    label = result["label"].lower()
    score = float(result["score"])
    return label, score

def process_csv(file):
    """Process uploaded CSV with both models"""
    df = pd.read_csv(file)
    if "text" not in df.columns:
        raise ValueError("CSV must contain a 'text' column")
    
    results = []
    for t in df["text"].astype(str):
        tb_label, tb_score = analyze_textblob(t)
        llm_label, llm_score = analyze_llm(t)
        results.append({
            "text": t,
            "TextBlob Sentiment": tb_label,
            "TextBlob Confidence": tb_score,
            "LLM Sentiment": llm_label,
            "LLM Confidence": llm_score
        })
    return pd.DataFrame(results)
