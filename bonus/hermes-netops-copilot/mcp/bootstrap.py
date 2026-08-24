from __future__ import annotations

import sys
from pathlib import Path

BONUS_DIR = Path(__file__).resolve().parents[1]
WORKSHOP_ROOT = BONUS_DIR.parents[1]
SRC_DIR = WORKSHOP_ROOT / "src"

for path in (WORKSHOP_ROOT, SRC_DIR, BONUS_DIR):
    value = str(path)
    if value not in sys.path:
        sys.path.insert(0, value)
