who-scorecards
==============

WHO Scorecard System

Installation
============

1. Installing ubuntu package dependencies:

    **$ sudo apt-get install libxml2-dev libxslt-dev texlive phantomjs pdfjam**

2. Creating virtual enviroment for python packages:

    **$ mkvirtualenv whoscorecards**

3. Installing the fonts for the project:

    **$ cp recipients/code/dashboard/oda/static/fonts/* ~/.fonts/**

    **$ sudo fc-cache -f -v**

4. Installing the widgetlabs plugin for inkscape

    **$ git clone https://github.com/adieyal/widgetlabs.git**

    **$ cp widgetlabs/inkscape/* ~/.config/inkscape/extensions/**

5. Edit ~/.config/inkscape/extensions/ in line 12. Change url = ..... to url=localhost:8080 or wherever your phantomjs server is listening.

6. Run the PhantomJS server.

    **$ phantomjs main.js**

To create the donor scorecards
==============================

cd PROJECTROOT/donor
python donors/code/who/manage.py runserver

-- in another session
cd PROJECTROOT/
scripts/generate.py

-- all pdfs will be generated in the output folder

To create the recipient scorecards
=================================

cd PROJECTROOT/recipients/code/dashboard/manage.py
python manage.py runserver

-- in another session
cd PROJECTROOT/scripts
for i `cat ../data/recipients/data/countries.csv | cut -d , -f 1`;
do
    make COUNTRY=$i
done


pip install -r requirements.txt
