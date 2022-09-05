VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

export OPENWEATHER_API_KEY=${OPENWEATHER_API_KEY}

run: $(VENV)/bin/activate
	 $(PYTHON) main.py


$(VENV)/bin/activate:
	 python3 -m venv $(VENV)
	 $(PIP) install requests boto3


clean:
	 rm -rf __pycache__
	 rm -rf $(VENV)