#!/usr/bin/env python3
"""
Entrypoint to run the Fact Knowledge Layer application.
Usage:
    python run.py
"""

import sys
import uvicorn

if __name__ == "__main__":
    print("\n========================================================")
    print("🚀 Starting Fact Knowledge Layer...")
    print("📍 Web Interface: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("========================================================\n")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
