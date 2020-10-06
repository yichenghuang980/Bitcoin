install:
	pip install --upgrade pip &&\
			pip install -r requirements.txt

format:
	black scrap.py
lint:
	pylint --disable=R,C,E1120 scrap.py
	
test:
	python -m pytest -vv --cov=scrap test_scrap.py
	#python -m pytest --nbval notebook.ipynb