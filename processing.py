import pandas as pd
import re
from textblob import TextBlob
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# ✅ Clean text
def clean_text(text):
    text = text.lower()  # convert to lowercase
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)  # remove URLs
    text = re.sub(r'@\w+|#\w*','', text)  # remove mentions and hashtags
    text = re.sub(r'[^A-Za-z\s]', '', text)  # remove special characters and numbers
    return text.strip()

# ✅ Load and preprocess dataset
def load_dataset(csv_path, sample_size=5000):
    df = pd.read_csv(csv_path, encoding='latin-1', nrows=sample_size)
    df.columns = ['target', 'ids', 'date', 'flag', 'user', 'text']
    
    df['text'] = df['text'].apply(clean_text)
    df['sentiment'] = df['target'].replace({0: 'negative', 2: 'neutral', 4: 'positive'})
    df = df[['text', 'sentiment']]
    
    return df

# ✅ Split dataset
def prepare_data(df):
    X_train, X_test, y_train, y_test = train_test_split(
        df['text'], df['sentiment'], test_size=0.2, random_state=42
    )
    return X_train, X_test, y_train, y_test

# ✅ Vectorize text
def vectorize_text(X_train, X_test, method='tfidf'):
    if method == 'count':
        vectorizer = CountVectorizer(max_features=5000)
    else:
        vectorizer = TfidfVectorizer(max_features=5000)
        
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    return X_train_vec, X_test_vec, vectorizer



def analyze_sentiment(text: str) -> str:
    """
    Return 'positive' | 'neutral' | 'negative' using TextBlob polarity.
    """
    if text is None:
        return "neutral"
    text = str(text).strip()
    if not text:
        return "neutral"

    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.05:
        return "positive"
    elif polarity < -0.05:
        return "negative"
    else:
        return "neutral"

def analyze_sentiment_series(series):
    """Vectorized helper for pandas Series."""
    return series.fillna("").astype(str).apply(analyze_sentiment)
