#!/bin/bash
# filepath: run_api.sh
# ! DEPRECATED
# ! This script is deprecated. Use `docker-compose up` instead.
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000