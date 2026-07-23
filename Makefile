install:
	pip install -r requirements.txt

load:
	python src/etl/loader.py

test:
	pytest

clean:
	rm -rf output/*

report:
	python src/report.py

dashboard:
	python dashboard.py

api:
	python api.py