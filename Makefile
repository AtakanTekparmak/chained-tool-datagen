# Set default target
.DEFAULT_GOAL := help

# Variables

## Python
PYTHON := python3
PIP := pip3
VENV_NAME := venv

# data-genie
DATA_GENIE_REPO_URL := https://github.com/interstellarninja/data-genie

# Help target
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  1. install           Install dependencies and set up the environment (should be run first)"
	@echo "  2. data_genie_setup  Clone the data-genie repository and install its dependencies (should be run second)"
	@echo "  2. run               Run the main.py script (should be run third)"
	@echo "  3. clean             Remove the virtual environment and its contents"

# Install dependencies and set up the environment
install:
	$(PYTHON) -m venv $(VENV_NAME)
	. $(VENV_NAME)/bin/activate && \
	$(PIP) install -r requirements.txt 

# Clone the data-genie repository
data_genie_setup:
	@git clone $(DATA_GENIE_REPO_URL) $(DATA_GENIE_REPO_DIR)
	@cd $(DATA_GENIE_REPO_DIR) && \
		. ../$(VENV_NAME)/bin/activate && \
		$(PIP) install -r requirements.txt

# Run the main.py script
run:
	. $(VENV_NAME)/bin/activate && \
	$(PYTHON) main.py

# Clean the virtual environment
clean:
	rm -rf $(VENV_NAME)