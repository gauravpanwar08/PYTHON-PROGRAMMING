# ============================================================
#              FASTAPI + PYDANTIC SETTINGS
# ============================================================

from fastapi import FastAPI

from config import settings


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)


# --------------------------------------------------------
# Application Information
# --------------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "API is running",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug
    }


# --------------------------------------------------------
# Server Configuration
# --------------------------------------------------------

@app.get("/config/server")
def server_config():

    return {
        "host": settings.host,
        "port": settings.port
    }


# --------------------------------------------------------
# Database Configuration
# --------------------------------------------------------

@app.get("/config/database")
def database_config():

    return {
        "database_configured": bool(
            settings.database_url
        )
    }


# --------------------------------------------------------
# Redis Configuration
# --------------------------------------------------------

@app.get("/config/redis")
def redis_config():

    return {
        "redis_configured": bool(
            settings.redis_url
        )
    }
