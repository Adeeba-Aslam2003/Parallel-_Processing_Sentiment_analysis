import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# One-time download (safe if already present)
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")

_sia = SentimentIntensityAnalyzer()

def _clean(text: str) -> str:
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    text = re.sub(r"[@#]\w+", "", text)
    return text.strip()

def analyze_sentiment(text: str):
    """
    Returns: (label: 'positive'|'neutral'|'negative', confidence: 0..1)
    """
    text = _clean(text or "")
    scores = _sia.polarity_scores(text)
    comp = scores["compound"]
    if comp >= 0.05:
        label = "positive"
        conf = comp
    elif comp <= -0.05:
        label = "negative"
        conf = -comp
    else:
        label = "neutral"
        conf = 1.0 - abs(comp)
    return label, float(conf)
