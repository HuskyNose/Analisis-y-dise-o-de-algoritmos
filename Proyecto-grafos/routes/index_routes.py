from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "ok": True,
        "service": "GeoRutas GraphGPS",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }