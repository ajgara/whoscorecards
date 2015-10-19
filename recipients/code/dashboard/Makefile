clean:
	rm -f dashboard/dashboard.db

all: clean

	python manage.py syncdb --noinput
	python manage.py load_countries "../../data/2015/Countries_for_the_2015_report.csv"

	# 2013 (To be published in 2015/2016)
	python manage.py load_general_indicators "../../data/2015/Table1_2015_report.xls"
	python manage.py load_allocation "../../data/2015/Table2_2015_report.xlsx"
	python manage.py load_allocation "../../data/2015/Table3_2015_report.xlsx"
	python manage.py load_disbursements_sources "../../data/2015/Table4_Disb_Sources.xlsx"
	python manage.py load_largest_disbursements "../../data/2015/7_largest_disbursements_2015_report.xlsx"
	python manage.py load_5largest_disbursements "../../data/2015/5_Largest_Sources_of_disbursements.xlsx"

    # 2012 (To be published in 2014/2015)
	# python manage.py load_general_indicators "../../data/2012/2012_Table1.xlsx"
	# python manage.py load_allocation "../../data/2012/2012_purpose_commitments.xlsx"
	# python manage.py load_allocation "../../data/2012/2012_purpose_disbursements.xlsx"
	# python manage.py load_disbursements_sources "../../data/2012/2012_Disbursements_sources.xlsx"
	# python manage.py load_largest_disbursements "../../data/2012/2012_7largest_disbursement.xlsx"
	# python manage.py load_5largest_disbursements "../../data/2012/2012_5_Largest_donors.xlsx"

	# 2011
	# python manage.py load_general_indicators "../../data/Table1.xlsx"
	# python manage.py load_allocation "../../data/2011_purpose_commitments.xls"
	# python manage.py load_allocation "../../data/2011_purpose_disbursements.xls"
	# python manage.py load_disbursements_sources "../../data/2011_disbursement_sources.xls"
	# python manage.py load_largest_disbursements "../../data/2011_largest_disbursements.xls"
	# python manage.py load_5largest_disbursements "../../data/2011_5largest_disbursements.xls"

	python manage.py createsuperuser --username=admin --email=admin