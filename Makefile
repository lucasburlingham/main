all: install run


install: 
	@echo "Installing dependencies..."
	@echo "Using PHP version $(shell php -v | head -n 1 | cut -d " " -f 2)"
	@echo "Using Python version $(shell python3 -V | cut -d " " -f 2)"
	@echo "Using Pip to install dependencies..."
	@python3 -m venv .venv
	@pip3 install -r requirements.txt
	@echo "Creating database..."
	@python3 src/db.py


run: install
	@echo "Running..."
	@cd src && FLASK_APP=app.py FLASK_ENV=development FLASK_DEBUG=1 FLASK_RUN_PORT=5000 FLASK_RUN_HOST=0.0.0.0
	@python3 src/app.py

reset:
	@echo "Resetting..."
	@rm -rf .venv __pycache__ ping.db
	@echo "Done."