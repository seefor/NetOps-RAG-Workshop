# Bonus Tests

Run from the workshop root:

```bash
python -m unittest discover -s bonus/hermes-netops-copilot/tests -p "test_*.py" -v
```

The tests validate synthetic evidence, source catalog filters, and Hermes config generation. They do not require a running Hermes process or Ollama server.
