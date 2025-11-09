import streamlit as st
st.set_page_config(page_title="Sentiment App")

try:
    from processing import analyze_sentiment
    from auth import login_user
except Exception as e:
    st.error(f"Startup error: {e}")

def render_app() -> None:
    st.title("💭 Sentiment Analysis Using Parallel Processing")
    st.write("Compare **TextBlob** and **LLM Sentiment Models**")

    option = st.radio("Choose mode:", ["Single Text", "Upload CSV"], horizontal=True)

    if option == "Single Text":
        text_input = st.text_area("Enter text to analyze sentiment:", height=150)
        if st.button("Analyze Sentiment"):
            if text_input.strip():
                with st.spinner("Analyzing sentiment..."):
                    from processing import analyze_textblob, analyze_llm
                    tb_label, tb_conf = analyze_textblob(text_input)
                    llm_label, llm_conf = analyze_llm(text_input)
                    st.subheader("Results:")
                    st.write(f"**TextBlob:** {tb_label} ({tb_conf:.2f})")
                    st.write(f"**LLM:** {llm_label} ({llm_conf:.2f})")
            else:
                st.warning("⚠️ Please enter some text to analyze.")

    else:
        st.subheader("📂 Upload CSV file")
        uploaded = st.file_uploader("Upload CSV with a 'text' column", type=["csv"])
        if uploaded:
            from processing import process_csv
            with st.spinner("Processing dataset..."):
                df_result = process_csv(uploaded)
                st.success("✅ Analysis complete!")
                st.dataframe(df_result)
                csv_out = df_result.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Download results", csv_out, "sentiment_results.csv", "text/csv")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
