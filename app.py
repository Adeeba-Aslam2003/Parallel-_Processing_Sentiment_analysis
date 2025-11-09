# app.py
import io
import streamlit as st

# Import safely; show errors in the UI instead of crashing to blank
try:
    from processing import (
        analyze_sentiment, analyze_textblob, analyze_llm, process_csv, _load_llm
    )
except Exception as e:
    st.set_page_config(page_title="Sentiment App", page_icon="💬")
    st.error("Import error in modules. Check files/requirements.")
    st.exception(e)
    st.stop()

st.set_page_config(page_title="Sentiment Analysis Using Parallel Processing", page_icon="💬", layout="centered")
st.title("💬 Sentiment Analysis Using Parallel Processing")

with st.sidebar:
    st.subheader("Options")
    llm_available = _load_llm() is not None
    if llm_available:
        st.success("LLM is available")
    else:
        st.warning("LLM not available yet (model download failed or blocked). TextBlob will still work.")

# --------- Single text analysis ----------
st.subheader("Analyze a Single Text")
text = st.text_area("Enter text to analyze sentiment:", height=120, key="single_text")
col1, col2 = st.columns(2)
with col1:
    if st.button("Analyze (TextBlob)"):
        s, c = analyze_textblob(text)
        st.success(f"TextBlob → **{s}** (confidence {c:.2f})")
with col2:
    if st.button("Analyze (LLM)"):
        s, c = analyze_llm(text)
        if s == "unavailable":
            st.error("LLM unavailable on this deployment. Try again later or check requirements.")
        else:
            st.success(f"LLM → **{s}** (confidence {c:.2f})")

st.divider()

# --------- Dataset upload and compare ----------
st.subheader("Batch Compare (CSV)")
st.caption("Upload a CSV with a **text** column. We'll run TextBlob & LLM and show a comparison table.")

file = st.file_uploader("Upload CSV", type=["csv"])
if file is not None:
    try:
        df_result = process_csv(file)
        st.dataframe(df_result, use_container_width=True)

        # Download button
        buf = io.BytesIO()
        df_result.to_csv(buf, index=False)
        st.download_button(
            "⬇️ Download results as CSV",
            data=buf.getvalue(),
            file_name="sentiment_results.csv",
            mime="text/csv",
        )
    except Exception as e:
        st.error("Could not process the CSV. Make sure it has a 'text' column.")
        st.exception(e)
