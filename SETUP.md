# Setup

## Recommended classroom baseline

Use Python 3.11 or 3.12 for attendees when possible. The workshop code is tested more broadly, but a conservative classroom baseline reduces environment variability.

## macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[hermes]"
cp .env.example .env
ollama pull llama3.2
ollama pull embeddinggemma
python scripts/preflight.py
```

## Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[hermes]"
Copy-Item .env.example .env
ollama pull llama3.2
ollama pull embeddinggemma
python scripts/preflight.py
```

Your pre-workshop goal is only to get the preflight to pass. Do not complete the labs ahead of time.
