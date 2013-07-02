clean:
	rm -f dashboard/dashboard.db

all: clean

	python manage.py syncdb --noinput
	python manage.py load_countries "../../data/countries.csv"

	python manage.py load_general_indicators "../../data/Table1.xlsx"
	python manage.py load_allocation "../../data/2011_purpose_commitments.xls"
	python manage.py load_allocation "../../data/2011_purpose_disbursements.xls"
	python manage.py load_disbursements_sources "../../data/2011_disbursement_sources.xls"
	python manage.py load_largest_disbursements "../../data/2011_largest_disbursements.xls"
	python manage.py createsuperuser --username=adi --email=a@b.com
