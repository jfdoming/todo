.PHONY: all run build install

all: run

run:
	@. env/bin/activate && python3 src/main.py

build:
	@. env/bin/activate && pyinstaller src/main.py -Fn todo

install:
	@[ -d env ] || python3 -m venv env
	@. env/bin/activate && python3 -m pip install -r requirements.txt
