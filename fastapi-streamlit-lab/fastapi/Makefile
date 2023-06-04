local-test:
	uvicorn main:app --reload --port 8000
prod-test:
	gunicorn -k uvicorn.workers.UvicornWorker main:app
