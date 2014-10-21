who-scorecards
==============

WHO Scorecard System

Structure
============
The program consists of a Python DJango application and a PhantomJS server running in the background.

The DJango application is used to do the following:

1. Retrieve data from .xls files and create corresponding DJango models to save in database.

2. Show the data in a DJango template, using svg graphics.

The PhantomJS server is used just to take the URL to the DJango template and render it to a PDF using a tool named rasterize.js


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


Changing static values inside templates
=================================
The files named *front.svg* and *back.svg* located at *recipients/code/dashboard/oda/static/svg/* have inside it the static values that appear in the final result.
It also has other dummy values in it, when the URL hosted in the DJango server is hit, this dummy values are dynamically changed to the real values of the corresponding country.

Changing dynamic values inside templates
=================================
These values are taken from three different places:

1. From the models of the DJango app (stored in the database)

2. Calculated in the logic inside the DJango view.

3. Calculated using javascript inside the page.

## Changing the value of the years:

1. Changing the static values inside the corresponding .svg files

2. Changing the all_years variable inside **scorecard.js**

3. Changing the variables inside the view named **front_data**