#!/usr/bin/env bash
playwright install
uvicorn backend.main:app --host 0.0.0.0 --port 10000