from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pathlib import Path
import json

router = APIRouter()

# Python excpects the files to be in the current working dir where you call the app
BASE_DIR = Path(__file__).resolve().parent.parent
CATS_FILE = BASE_DIR / "cats.json"


# Liveness route- is the app alive?
@router.get("/healthz")
def liveness():
    return {"status": "alive"}


# Readiness route- is the app ready for traffic?
@router.get("/readyz")
def readiness():
    try:
        # Make sure datafile is present and loads ok.
        if not CATS_FILE.exists():
            raise Exception("Data file missing")

        with open(CATS_FILE) as f:
            json.load(f)

        return {"status": "ready"}
    # Return 503 if service isn't ready.
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not ready", "reason": str(e)},
        )