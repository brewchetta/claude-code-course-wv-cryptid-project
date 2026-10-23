from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/.env and backend/.env.local, wherever the process is started from.
# Later files win, so .env.local overrides .env. Missing files are skipped.
BACKEND_DIR = Path(__file__).resolve().parent.parent
ENV_FILES = (BACKEND_DIR / ".env", BACKEND_DIR / ".env.local")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILES, env_prefix="MSAN_")

    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "msan"
    cors_origins: list[str] = ["http://localhost:5173"]
    # Shared secret for the moderation endpoints. Empty disables them.
    admin_key: str = ""
    # Sent in the User-Agent of outside API calls so providers can reach us.
    contact_email: str = ""
    # Reference point for the live moon/weather readout (roughly central West Virginia).
    conditions_lat: float = 38.66
    conditions_lon: float = -80.71
    conditions_label: str = "Central WV"


settings = Settings()
