# app.py
import io
import pandas as pd
import streamlit as st
from auth import login_user
from processing import clean_text, analyze_textblob, analyze_llm, process_dataframe

st.set_page_config(page_title="Sentiment App", page_icon="💬", layout="wide")

# ------------------ LOGIN ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Sentiment Analysis Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_user(email, password):
            st.session_state.logged_in = True
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid credentials")
    st.stop()  # block rest of app until logged in

# ------------------ APP STATE ------------------
if "df_raw" not in st.session_state:
    st.session_state.df_raw = None
if "df_processed" not in st.session_state:
    st.session_state.df_processed = None
if "text_col" not in st.session_state:
    st.session_state.text_col = None

# ------------------ SIDEBAR / NAV ------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Steps",
    ["Welcome", "Load Data", "Preprocess & WordCount", "Compare Models", "Download Results", "Email Results"],
    index=0
)
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ------------------ PAGES ------------------

# 1) Welcome
if page == "Welcome":
    st.title("🎉 Welcome to the Topic Modeling / Sentiment Application!")
    st.write("""
Use the sidebar to navigate through the steps:

1. **Load Data**: Upload your dataset (CSV/Excel).
2. **Preprocess & WordCount**: Clean text + show word statistics.
3. **Compare Models**: Run **TextBlob** vs **LLM-like heuristic** and compare.
4. **Download Results**: Export processed results.
5. **Email Results**: (Optional) Email results if SMTP secrets are set.
""")

# 2) Load Data
elif page == "Load Data":
    st.title("📥 Load Data")
    f = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls"])
    if f is not None:
        try:
            if f.name.lower().endswith(".csv"):
                df = pd.read_csv(f)
            else:
                df = pd.read_excel(f)
            st.session_state.df_raw = df
            st.success(f"Loaded shape: {df.shape}")
            st.dataframe(df.head(20), use_container_width=True)

            # Choose text column
            text_col = st.selectbox("Select the text column", df.columns, index=0)
            st.session_state.text_col = text_col

        except Exception as e:
            st.error(f"Failed to read file: {e}")

# 3) Preprocess & WordCount
elif page == "Preprocess & WordCount":
    st.title("🧹 Preprocess & WordCount")
    if st.session_state.df_raw is None or st.session_state.text_col is None:
        st.warning("Please load data first (and choose a text column).")
    else:
        df = st.session_state.df_raw.copy()
        tcol = st.session_state.text_col
        st.subheader("Preview")
        st.dataframe(df[[tcol]].head(20), use_container_width=True)

        with st.spinner("Cleaning text..."):
            df["clean_text"] = df[tcol].astype(str).apply(clean_text)

        st.subheader("Examples (cleaned)")
        st.dataframe(df[[tcol, "clean_text"]].head(20), use_container_width=True)

        # simple word count
        st.subheader("Word Count")
        wc = df["clean_text"].str.split().map(len)
        st.write("Average words per row:", float(wc.mean()))
        st.bar_chart(wc.head(200))  # quick look

        st.info("Proceed to **Compare Models** to run TextBlob vs LLM-like heuristic.")
        st.session_state.df_processed = None  # reset downstream

# 4) Compare Models
elif page == "Compare Models":
    st.title("⚖️ Compare Models: TextBlob vs LLM-like Heuristic")
    if st.session_state.df_raw is None or st.session_state.text_col is None:
        st.warning("Please load data first.")
    else:
        df = st.session_state.df_raw
        tcol = st.session_state.text_col

        run_full = st.checkbox("Run on FULL dataset", value=False,
                               help="Unchecked = run on first 500 rows for speed")
        n = len(df) if run_full else min(500, len(df))
        use_df = df.head(n)

        if st.button("Run Comparison"):
            with st.spinner("Running comparison..."):
                out = process_dataframe(use_df, tcol)
            st.session_state.df_processed = out
            st.success(f"Done! Processed {len(out)} rows.")
            st.dataframe(out.head(30), use_container_width=True)

            st.subheader("Label distribution")
            col1, col2 = st.columns(2)
            with col1:
                st.write("TextBlob labels")
                st.bar_chart(out["textblob_label"].value_counts())
            with col2:
                st.write("LLM-like labels")
                st.bar_chart(out["llm_label"].value_counts())

        # quick single-line tester
        st.markdown("---")
        st.subheader("Try a single sentence")
        txt = st.text_input("Enter text to analyze sentiment")
        if st.button("Analyze single text") and txt.strip():
            c = clean_text(txt)
            l1, s1 = analyze_textblob(c)
            l2, s2 = analyze_llm(c)
            st.write(f"**TextBlob:** {l1} (score {s1:.2f})")
            st.write(f"**LLM-like:** {l2} (score {s2:.2f})")

# 5) Download Results
elif page == "Download Results":
    st.title("💾 Download Results")
    dfp = st.session_state.df_processed
    if dfp is None:
        st.warning("Please run **Compare Models** first.")
    else:
        buf = io.BytesIO()
        dfp.to_csv(buf, index=False)
        st.download_button(
            "Download CSV",
            data=buf.getvalue(),
            file_name="sentiment_results.csv",
            mime="text/csv"
        )
        st.dataframe(dfp.head(30), use_container_width=True)

# 6) Email Results (optional)
elif page == "Email Results":
    st.title("📧 Email Results")
    st.info("To enable emailing, add SMTP settings in **Streamlit Secrets** (optional).")
    st.code(
        """
# In Streamlit Cloud -> App -> Settings -> Secrets
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = "your_email@gmail.com"
EMAIL_PASS = "your_app_password"  # Gmail App Password
EMAIL_TO   = "recipient@example.com"
        """.strip()
    )
    dfp = st.session_state.df_processed
    if dfp is None:
        st.warning("Please run **Compare Models** first.")
    else:
        try:
            host = st.secrets.get("EMAIL_HOST")
            port = int(st.secrets.get("EMAIL_PORT", 587))
            user = st.secrets.get("EMAIL_USER")
            pwd  = st.secrets.get("EMAIL_PASS")
            to   = st.secrets.get("EMAIL_TO")

            if not all([host, port, user, pwd, to]):
                st.error("Secrets not set. Please add EMAIL_* secrets to send emails.")
            else:
                import smtplib, ssl, base64
                from email.message import EmailMessage

                # attach results as CSV
                buf = io.StringIO()
                dfp.to_csv(buf, index=False)
                csv_bytes = buf.getvalue().encode()

                msg = EmailMessage()
                msg["Subject"] = "Sentiment Results"
                msg["From"] = user
                msg["To"] = to
                msg.set_content("Attached are the sentiment results.")
                msg.add_attachment(csv_bytes, maintype="text", subtype="csv", filename="sentiment_results.csv")

                context = ssl.create_default_context()
                with smtplib.SMTP(host, port) as server:
                    server.starttls(context=context)
                    server.login(user, pwd)
                    server.send_message(msg)
                st.success(f"Email sent to {to} ✅")
        except Exception as e:
            st.error(f"Email failed: {e}")
