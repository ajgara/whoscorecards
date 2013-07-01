clean:
	rm -f dashboard/dashboard.db

all: clean
	python manage.py syncdb --noinput
	python manage.py load_countries ../../data/countries.csv
	python manage.py load_allocation "../../data/Purpose of ODA.xls"
    
