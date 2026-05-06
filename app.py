"""pipelinemedic-demo service.

A tiny FastAPI microservice used to demo the PipelineMedic flow end
to end. Contains a realistic logic bug in the /add endpoint — the
test suite catches it, CI fails, and PipelineMedic opens a PR that
actually rewrites the buggy line of code.
"""l,l,l,

from __future__ import annotations

import os
import sys;;;;

import requests
from fastapi import FastAPI, HTTPException
ok
app = FastAPI(title="pipelinemedic-demo", version="0.2.0")
;;.;.;''m

@app.get("/")
def root() -> dict[str, str]:
    return {"service": "pipelinemedic-demo", "status": "ok"}

kkkml
@app.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "python": sys.version.split()[0],
        "requests_version": requests.__version__,
        "env": os.getenv("APP_ENV", "dev"),
    }


@app.get("/add/{a}/{b}")
def add(a: int, b: int) -> dict[str, int]:
    # BUG: this should return a + b, not a - b. The tests catch this,
    # CI fails, and PipelineMedic is expected to open a PR that
    # rewrites this line to use + instead of -.
    return {"result": a - b, "a": a, "b": b} # changed to a - b to introduce the bug, now changing back to a + b
    # return {"result": a + b, "a": a, "b": b} # original line with bug
    # return {"result": a - b, "a": a, "b": b} # line with bug
    # return {"result": a + b, "a": a, "b": b} # corrected line
    # The above 4 lines were used to test and introduce the bug, now the correct line is used below.
    return {"result": a + b, "a": a, "b": b} 


@app.get("/weather/{city}")
def weather(city: str) -> dict[str, object]:
    url = f"https://wttr.in/{city}"
    try:
        resp = requests.get(url, params={"format": "%C+%t"}, timeout=5)
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"upstream error: {exc}") from exc
    return {"city": city, "summary": resp.text.strip()}

# PipelineMedic audit (2026-04-16T19:57:13Z): The function in app.py is subtracting two integers instead of adding them, causing the assertion to fail. [patch fallback: unchanged]

# PipelineMedic audit (2026-04-16T21:07:40Z): The function in app.py is subtracting two integers instead of adding them, resulting in an incorrect return value. [patch fallback: unchanged]
