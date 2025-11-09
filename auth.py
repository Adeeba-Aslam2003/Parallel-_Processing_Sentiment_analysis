# auth.py
# Simple demo authentication. You can switch to Streamlit secrets anytime.

from typing import Tuple
try:
    import streamlit as st
except Exception:  # when running outside Streamlit
    st = None

# Default demo creds (fallback)
_DEMO_EMAIL = "adeebaslam054@gmail.com"
_DEMO_PASS  = "Adeeba@123"

def _creds_from_secrets() -> Tuple[str, str]:
    """Prefer Streamlit cloud secrets if available, else fallback to defaults."""
    if st is not None and hasattr(st, "secrets"):
        email = st.secrets.get("demo_email", _DEMO_EMAIL)
        passwd = st.secrets.get("demo_password", _DEMO_PASS)
        return str(email), str(passwd)
    return _DEMO_EMAIL, _DEMO_PASS

def login_user(email: str, password: str) -> bool:
    """
    Returns True if the provided credentials match the configured demo credentials.
    """
    demo_email, demo_pass = _creds_from_secrets()
    return str(email).strip().lower() == demo_email.lower() and str(password) == demo_pass
