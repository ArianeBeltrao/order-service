test:
	pytest -v -s

lint:
	pylint . --ignore=venv

setup:
	pip3 install -r requirements.txt

run:
	docker compose up -d && uvicorn main:app --reload --port 8001 --log-config=configs/log_conf.yml  

coverage:
	pytest . -v --cov=. && coverage html
