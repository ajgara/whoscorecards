who-scorecards
==============

WHO Scorecard System

installation
============

This installation is really messy and might never be cleaned up. Hopefully this guide will be useful

sudo apt-get install libxml2-dev libxslt-dev texlive phantomjs pdfjam
virtualenv ~./.virtualenvs/who
source ~/.virtualenvs/who/bin/activate

-- install the fonts in recipients/code/dashboard/oda/static/fonts/ into .fonts
sudo fc-cache -f -v

cd /path/to/devfolder/
git clone 
mkdir -p /path/
https://github.com/adieyal/widgetlabs.git
cp /path/to/devfolder/widgetlabs/inkscape/* ~/.config/inkscape/extensions/
-- edit ~/.config/inkscape/extensions/ in line 12. Change url = ..... to url=localhost:8080 or wherever your phantomjs server is listening
cd /path/to/devfolder/server
phantomjs main.js

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
