#!/bin/bash
# filepath: run_api.sh
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000