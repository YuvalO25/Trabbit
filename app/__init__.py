# Compatibility wrapper to expose backend.app as app
from backend.app.api import app  # re-export FastAPI instance

__all__ = ["app"]
