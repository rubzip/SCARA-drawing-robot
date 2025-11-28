VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
ACTIVATE = . $(VENV_DIR)/bin/activate

venv:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requiFILE ?=
	run_drawing:
		$(PYTHON) -m src.scara_simmulation.app_drawing $(FILE)rements.txt

activate:
	$(ACTIVATE)

run_segment_extractor:
	$(VENV_DIR)/bin/streamlit run src/segment_extractor/app.py

run_follower:
	$(PYTHON) -m src.scara_simmulation.app_control

FILE ?=
run_drawing:
	$(PYTHON) -m src.scara_simmulation.app_drawing $(FILE)

