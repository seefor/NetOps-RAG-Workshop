PYTHON ?= python

install:
	$(PYTHON) -m pip install -e .

preflight:
	$(PYTHON) scripts/preflight.py

stats:
	netops-rag stats --data data

ingest:
	netops-rag ingest --data data --reset

ask:
	netops-rag ask "Why did the BGP session between atl-core-r1 and nyc-edge-r1 flap?"

streamlit:
	$(PYTHON) -m streamlit run streamlit_app.py

test:
	$(PYTHON) -m unittest discover -s tests -v
