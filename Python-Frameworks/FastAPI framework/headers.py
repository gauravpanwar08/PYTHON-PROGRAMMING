# HEADERS:
# Used to send metadata with HTTP requests.
# FastAPI automatically extracts header values using Header() and HTTP headers use hyphen format.
#
# Common Uses:
# - JWT tokens
# - Authorization tokens
# - API keys
# - Content type
# - Client/browser information
# --------------------------------------------------------------

from typing import Optional

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/headers")
def get_headers(

    # Standard Headers
    host: Optional[str] = Header(default=None),
    user_agent: Optional[str] = Header(default=None),
    accept: Optional[str] = Header(default=None),
    accept_language: Optional[str] = Header(default=None),
    content_type: Optional[str] = Header(default=None),
    authorization: Optional[str] = Header(default=None),
    cache_control: Optional[str] = Header(default=None),
    referer: Optional[str] = Header(default=None),

    # Custom Header
    api_key: Optional[str] = Header(default=None)

):
    
    return {

        "host": host,
        "user_agent": user_agent,
        "accept": accept,
        "accept_language": accept_language,
        "content_type": content_type,
        "authorization": authorization,
        "cache_control": cache_control,
        "referer": referer,

        # Custom Header
        "api_key": api_key
    }
    