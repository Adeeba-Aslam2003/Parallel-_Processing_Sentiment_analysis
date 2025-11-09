# auth.py
# Simple email/password authentication

ALLOWED_EMAIL = "adeebaslam054@gmail.com"
ALLOWED_PASS  = "Adeeba@123"

def login_user(email: str, password: str) -> bool:
    """Return True if email & password match."""
    return str(email).strip().lower() == ALLOWED_EMAIL and str(password) == ALLOWED_PASS
