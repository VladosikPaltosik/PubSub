lint:
	flake8 .
start:
	uvicorn app.main:app --port 8000 --reload
