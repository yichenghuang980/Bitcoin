install:
	pip install --upgrade pip &&\
			pip install -r requirements.txt

test:
	python -m pytest -vv --cov=scrap test_scrap.py
	#python -m pytest --nbval notebook.ipynb