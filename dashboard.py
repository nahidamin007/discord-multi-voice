"""Root entrypoint that launches the dashboard inside Exiters-Discord-Multi-Voice."""
import os
import sys
from pathlib import Path

# Ensure inner directory is in sys.path
INNER_DIR = Path(__file__).resolve().parent / "Exiters-Discord-Multi-Voice"
if str(INNER_DIR) not in sys.path:
    sys.path.insert(0, str(INNER_DIR))

# Change current working directory to the inner directory so relative paths work
os.chdir(INNER_DIR)

if __name__ == "__main__":
    import asyncio
    import dashboard
    try:
        asyncio.run(dashboard.main())
    except KeyboardInterrupt:
        pass
