ARGS=

.PHONY: all run build install

all: run

run:
	@. env/bin/activate && CONFIG_HOME=config python3 src/main.py $(ARGS)

build:
	@. env/bin/activate && pyinstaller -p src/ src/main.py -Dyn todo
	@cp config/*.json dist/todo/

install:
	@[ -d env ] || python3 -m venv env
	@. env/bin/activate && python3 -m pip install -r requirements.txt
	@. env/bin/activate && python3 -m pip install -r dev-requirements.txt
