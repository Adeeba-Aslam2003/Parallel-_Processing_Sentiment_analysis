import streamlit as st
from processing import analyze_sentiment
from auth import login_user

# --- Page config ---
st.set_page_config(page_title="Sentiment Analysis App", page_icon="💬", layout="centered")


# ---------- UI SECTIONS ----------
def render_login() -> None:
    st.title("🔐 Sentiment Analysis Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid credentials")


def render_app() -> None:
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
        st.rerun()


# ---------- ENTRY POINT ----------
def main() -> None:
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        render_login()
    else:
        render_app()


if __name__ == "__main__":
    main()
