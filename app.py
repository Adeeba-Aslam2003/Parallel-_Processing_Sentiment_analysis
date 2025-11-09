import streamlit as st
from processing import analyze_sentiment
from auth import login_user

# --- Page configuration ---
st.set_page_config(page_title="Sentiment Analysis App", page_icon="💬", layout="centered")

# --- Safe rerun helper ---
def safe_rerun():
    """Ensure rerun works on all Streamlit versions."""
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st.experimental_rerun, "__call__"):
        st.experimental_rerun()

# --- Login state ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Login page ---
if not st.session_state.logged_in:
    st.title("🔐 Sentiment Analysis Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.success("✅ Login successful!")
            safe_rerun()
        else:
            st.error("❌ Invalid credentials")

# --- Sentiment analysis page ---
else:
    st.title("💭 Sentiment Analysis Using Parallel Processing")

    text_input = st.text_area("Enter text to analyze sentiment:", height=150)

    if st.button("Analyze Sentiment"):
        if text_input.strip():
            with st.spinner("Analyzing sentiment..."):
                sentiment, confidence = analyze_sentiment(text_input)
                st.success(f"**Sentiment:** {sentiment}")
                st.write(f"**Confidence:** {confidence:.2f}")
        else:
            st.warning("⚠️ Please enter some text to analyze.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        safe_rerun()
