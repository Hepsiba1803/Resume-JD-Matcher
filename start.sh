#!/bin/bash
uvicorn backend.app.main:web_app --host 0.0.0.0 --port $PORT
