# Set default target
.DEFAULT_GOAL := help

# Variables

## Python
PYTHON := python3
PIP := pip
VENV_NAME := venv

# .env file
ENV_FILE := .env

# Help target
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  1. install           	    Install dependencies and set up the environment"
	@echo "  2. run_schema_gen			Run the function schema generating flow (First step in the pipeline)"
	@echo "  3. run_user_query_gen		Run the user query generating flow (Second step in the pipeline)"
	@echo "  4. run_dummy_function_gen  Run the dummy function generating flow (Third step in the pipeline)"
	@echo "  5. clean             		Remove the virtual environment and its contents"

# Copy the .env.example file to .env only if it doesn't exist
copy_env:
	if [ ! -f $(ENV_FILE) ]; then cp .env.example $(ENV_FILE); fi

# Install dependencies and set up the environment
install: copy_env
	$(PYTHON) -m venv $(VENV_NAME)
	. $(VENV_NAME)/bin/activate && \
	$(PIP) install -r requirements.txt 

# Run the function schema generating flow 
run_schema_gen:
	. $(VENV_NAME)/bin/activate && \
	$(PYTHON) main.py --flow function_generation

# Run the user query generating flow
run_user_query_gen:
	. $(VENV_NAME)/bin/activate && \
	$(PYTHON) main.py --flow user_query_generation

# Run the dummy function generating flow
run_dummy_function_gen:
	. $(VENV_NAME)/bin/activate && \
	$(PYTHON) main.py --flow dummy_function_generation

# Run the function calling flow
run_function_call:
	. $(VENV_NAME)/bin/activate && \
	$(PYTHON) main.py --flow function_calling

# Run all the flows
run_all:
	. $(VENV_NAME)/bin/activate && \
	$(PYTHON) main.py --flow function_generation && \
	$(PYTHON) main.py --flow user_query_generation && \
	$(PYTHON) main.py --flow dummy_function_generation 

# Clean the virtual environment
clean:
	rm -rf $(VENV_NAME)