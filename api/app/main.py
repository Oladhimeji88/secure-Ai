from fastapi import FastAPI

from app.core.logging import configure_logging
from app.routers import alerts, assets, auth, gateway, ingest, overview, remediation, settings

configure_logging()

app = FastAPI(title="Aegis API", version="0.1.0")


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


app.include_router(auth.router, prefix="/api/v1")
app.include_router(overview.router, prefix="/api/v1")
app.include_router(alerts.router, prefix="/api/v1")
app.include_router(assets.router, prefix="/api/v1")
app.include_router(remediation.router, prefix="/api/v1")
app.include_router(gateway.router, prefix="/api/v1")
app.include_router(settings.router, prefix="/api/v1")
app.include_router(ingest.router, prefix="/api/v1")
