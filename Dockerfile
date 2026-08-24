FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY prompts ./prompts
COPY data ./data

RUN pip install --no-cache-dir -e .

EXPOSE 8501
CMD ["python", "-m", "streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0"]
