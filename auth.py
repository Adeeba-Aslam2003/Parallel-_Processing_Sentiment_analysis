import streamlit as st

# ✅ Simple login authentication (demo purpose)
def check_login():
    # You can replace this with a database or .streamlit/secrets.toml later
    users = {"admin": "1234", "adeeba": "2003"}

    # Store login state in session
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # If not logged in, show login form
    if not st.session_state.logged_in:
        st.title("🔐 Login Page")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.success("✅ Login successful!")
                st.experimental_rerun()
            else:
                st.error("❌ Invalid username or password")

        st.stop()  # Stop execution until login succeeds
