"""
AcuPath Enterprise Laboratory Information System (LIS)
Root Execution Entrypoint
"""

import os
import sys
import uvicorn

# Add backend to python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from app.main import app


def main():
    """Run AcuPath LIS backend production server."""
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"Starting AcuPath Enterprise LIS on http://{host}:{port}")
    uvicorn.run("app.main:app", app_dir="backend", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()
