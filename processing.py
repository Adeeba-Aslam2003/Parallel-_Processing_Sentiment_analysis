# processing.py
import re
import pandas as pd
from textblob import TextBlob

# ---------- Text cleaning ----------
def clean_text(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[@#]\w+", "", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ---------- TextBlob sentiment ----------
def analyze_textblob(text: str):
    """Return (label, polarity in [-1,1])."""
    tb = TextBlob(text)
    polarity = float(tb.sentiment.polarity)
    if polarity > 0.05:
        label = "positive"
    elif polarity < -0.05:
        label = "negative"
    else:
        label = "neutral"
    return label, polarity

# ---------- Optional: LLM sentiment (fallback = simple heuristic) ----------
def analyze_llm(text: str):
    """
    If you later add an API key in Streamlit secrets (OPENAI_API_KEY),
    you can replace this with a real LLM call. For now we use a small
    heuristic so the app works out of the box.
    """
    txt = text.lower()
    pos_words = ["good", "great", "excellent", "love", "happy", "fantastic", "awesome"]
    neg_words = ["bad", "terrible", "hate", "sad", "awful", "worst", "angry"]

    score = 0
    for w in pos_words:
        if w in txt: score += 1
    for w in neg_words:
        if w in txt: score -= 1

    if score > 0:
        return "positive", min(1.0, 0.1 * score)
    elif score < 0:
        return "negative", max(-1.0, 0.1 * score)
    else:
        return "neutral", 0.0

# ---------- CSV/Excel pipeline ----------
def process_dataframe(df: pd.DataFrame, text_col: str) -> pd.DataFrame:
    out = df.copy()
    out["clean_text"] = out[text_col].astype(str).apply(clean_text)

    tb_labels, tb_scores = [], []
    llm_labels, llm_scores = [], []

    for t in out["clean_text"]:
        l1, s1 = analyze_textblob(t)
        l2, s2 = analyze_llm(t)
        tb_labels.append(l1); tb_scores.append(s1)
        llm_labels.append(l2); llm_scores.append(s2)

    out["textblob_label"] = tb_labels
    out["textblob_score"] = tb_scores
    out["llm_label"] = llm_labels
    out["llm_score"] = llm_scores
    return out
