# COOKIES:
# Small pieces of data stored in the browser and sent with requests.
#
# Common Uses:
# - Session management
# - User authentication
# - Remember login/preferences
# - Tracking user behavior
# -------------------------------------------------------------------

from typing import Optional

from fastapi import FastAPI, Cookie

app = FastAPI()


@app.get("/cookies")
def get_cookies(
    # Standard/Common Cookies
    session_id: Optional[str] = Cookie(default=None),
    access_token: Optional[str] = Cookie(default=None),
    refresh_token: Optional[str] = Cookie(default=None),
    theme: Optional[str] = Cookie(default=None),
    language: Optional[str] = Cookie(default=None),
    remember_me: Optional[str] = Cookie(default=None),
    tracking_id: Optional[str] = Cookie(default=None),
    csrf_token: Optional[str] = Cookie(default=None),
    # Custom Cookie
    gaurav_cookie: Optional[str] = Cookie(default=None),
):
    return {
        "session_id": session_id,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "theme": theme,
        "language": language,
        "remember_me": remember_me,
        "tracking_id": tracking_id,
        "csrf_token": csrf_token,
        # Custom Cookie
        "gaurav_cookie": gaurav_cookie,
    }
