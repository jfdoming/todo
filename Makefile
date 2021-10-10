all: install

install:
	@[ -d env ] || python3 -m venv env
	@. env/bin/activate && python3 -m pip install -r requirements.txt
