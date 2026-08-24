# Cross-Platform Hermes Desktop Bonus

The v8.2 setup commands are the same on macOS, Linux, and Windows once the workshop virtual environment is active.

## macOS / Linux

```bash
source .venv/bin/activate
python bonus/hermes-netops-copilot/scripts/desktop_profile_setup.py
python bonus/hermes-netops-copilot/scripts/desktop_preflight.py
python bonus/hermes-netops-copilot/scripts/launch_desktop.py
```

## Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
python bonus\hermes-netops-copilot\scripts\desktop_profile_setup.py
python bonus\hermes-netops-copilot\scripts\desktop_preflight.py
python bonus\hermes-netops-copilot\scripts\launch_desktop.py
```

The setup script detects the active Python executable and passes absolute server paths to Hermes. It also detects whether the installed Hermes `project create` command expects a positional path or `--path`.

MCP registration is global in the tested workshop build. The `netops-workshop` profile still isolates the workshop's working-directory and skill configuration.
