install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	pylint --disable=R,C,E1120 scrape.py
	
test:
	python -m pytest -vv --cov=scrape test_scrape.py
	#python -m pytest --nbval notebook.ipynb