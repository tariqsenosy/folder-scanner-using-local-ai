from __future__ import annotations

import hashlib
import json
import os
from configparser import ConfigParser
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import Body, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse


def _load_ingest_config() -> dict[str, str]:
    """
    Loads ingest settings from:
    - env: LOG_INGEST_API_KEY, LOG_INGEST_STORAGE_DIR
    - ini: whatsapp-logger/config/settings.ini ([INGEST] section)
    """
    api_key = os.getenv("LOG_INGEST_API_KEY")
    storage_dir = os.getenv("LOG_INGEST_STORAGE_DIR")

    ini_path = Path(__file__).parent / "whatsapp-logger" / "config" / "settings.ini"
    if ini_path.exists():
        config = ConfigParser()
        config.read(str(ini_path))
        if not api_key and config.has_option("INGEST", "api_key"):
            api_key = config.get("INGEST", "api_key").strip() or None
        if not storage_dir and config.has_option("INGEST", "storage_dir"):
            storage_dir = config.get("INGEST", "storage_dir").strip() or None

    return {
        "api_key": api_key or "",
        "storage_dir": storage_dir or str(Path(__file__).parent / "whatsapp-logger" / "ingested_logs"),
    }


def _safe_component(value: str, *, fallback: str) -> str:
    value = (value or "").strip()
    if not value:
        return fallback
    cleaned = []
    for ch in value:
        if ch.isalnum() or ch in ("-", "_", "."):
            cleaned.append(ch)
        else:
            cleaned.append("_")
    out = "".join(cleaned).strip("._")
    return out or fallback


def _utc_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _event_id(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()[:24]


app = FastAPI(title="Log Ingest API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ingest/logs")
async def ingest_logs(
    request: Request,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    body: Any = Body(default=None),
) -> JSONResponse:
    cfg = _load_ingest_config()
    required_key = cfg["api_key"].strip()
    if required_key:
        provided = (x_api_key or "").strip()
        if not provided or provided != required_key:
            raise HTTPException(status_code=401, detail="invalid api key")

    raw_bytes = await request.body()
    if len(raw_bytes) > 2_000_000:
        raise HTTPException(status_code=413, detail="payload too large (max 2MB)")

    content_type = (request.headers.get("content-type") or "").lower()
    source = "unknown"
    record: dict[str, Any]

    if "application/json" in content_type:
        # Prefer already-parsed Body when possible.
        payload_obj = body if body is not None else json.loads(raw_bytes.decode("utf-8"))
        if isinstance(payload_obj, dict):
            source = str(payload_obj.get("source") or payload_obj.get("service") or "unknown")
            record = payload_obj
        else:
            record = {"source": "unknown", "payload": payload_obj}
    else:
        text = raw_bytes.decode("utf-8", errors="replace")
        record = {"source": "unknown", "message": text}

    source = _safe_component(source, fallback="unknown")
    record.setdefault("source", source)
    record.setdefault("received_at", datetime.now(timezone.utc).isoformat())

    storage_dir = Path(cfg["storage_dir"])
    storage_dir.mkdir(parents=True, exist_ok=True)
    out_path = storage_dir / f"{_utc_date()}__{source}.jsonl"

    line_bytes = (json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8")
    event_id = _event_id(line_bytes)

    with open(out_path, "ab") as f:
        f.write(line_bytes)

    return JSONResponse(status_code=202, content={"status": "accepted", "id": event_id, "file": str(out_path)})

