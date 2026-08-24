from __future__ import annotations

import argparse
from pathlib import Path


BASE = Path(__file__).resolve().parents[1] / "mock_state"
ACTIVE = BASE / ".active_scenario"


def scenarios() -> list[str]:
    return sorted(path.name for path in BASE.iterdir() if path.is_dir() and (path / "scenario.json").exists())


def main() -> None:
    parser = argparse.ArgumentParser(description="Select the active synthetic NetOps scenario")
    parser.add_argument("scenario", nargs="?")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()

    valid = scenarios()
    if args.list:
        print("\n".join(valid))
        return
    if args.show:
        print(ACTIVE.read_text(encoding="utf-8").strip() if ACTIVE.exists() else "bgp-policy-drift")
        return
    if not args.scenario:
        parser.error("provide a scenario or use --list/--show")
    if args.scenario not in valid:
        parser.error(f"unknown scenario {args.scenario!r}; valid: {', '.join(valid)}")
    ACTIVE.write_text(args.scenario + "\n", encoding="utf-8")
    print(f"Active scenario: {args.scenario}")


if __name__ == "__main__":
    main()
