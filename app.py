import streamlit as st
from processing import analyze_sentiment
from auth import login_user

st.set_page_config(page_title="Sentiment Analysis App", page_icon="💬", layout="centered")

# ---- helper so it works on every Streamlit version ----
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Sentiment Analysis Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.success("✅ Login successful!")
            safe_rerun()
        else:
            st.error("❌ Invalid credentials")
else:
    st.title("💭 Sentiment Analysis Using Parallel Processing")

    text_input = st.text_area("Enter text to analyze sentiment:", height=150)

    col_analyze, col_logout = st.columns(2)
    with col_analyze:
        if st.button("Analyze Sentiment", use_container_width=True):
            if text_input.strip():
                with st.spinner("Analyzing sentiment..."):
                    sentiment, confidence = analyze_sentiment(text_input)
                st.success(f"**Sentiment:** {sentiment}")
                st.write(f"**Confidence:** {confidence:.2f}")
            else:
                st.warning("⚠️ Please enter some text to analyze.")
    with col_logout:
        if st.button("Logout", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            safe_rerun()
