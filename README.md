# Documentation for ODA Scorecards

### Installing the app

This guide assumes you're using Ubuntu or another Debian based Linux distribution. First we create a directory to store the files for the project:

```sh
$ mkdir odascorecards
```

Inside this folder, we clone the GitHub repository:

```sh
$ cd odascorecards
$ git clone https://github.com/ajgara/whoscorecards.git
```

We first need to install some ubuntu packages in order to run the app:

```sh
$ sudo apt-get install libxml2-dev libxslt-dev texlive phantomjs pdfjam virtualenvwrapper python-pip
```

Now we create a virtual enviroment to install python packages in:

```sh 
$ mkvirtualenv whoscorecards
```

We swicth into this new enviroment:

```sh
$ workon whoscorecards
```

Now we install the python dependencies:
```sh
$ pip install -r requirements.txt
```

Installing the fonts used by the app:
```sh
$ cp whoscorecards/recipients/code/dashboard/oda/static/fonts/* ~/.fonts/
$ sudo fc-cache -f -v
```

The app is already installed.

### Running the app

We have to load the countries data first:
```sh
$ cd whoscorecards/recipients/code/dashboard/
$ make all
```
When the console asks for a password just insert 'admin'.

Now we have to run the DJango server:
```sh
$ cd whoscorecards/recipients/code/dashboard/
$./manage.py runserver 8000
```

Now you can open your browser and put the URL "http://127.0.0.1:8000/oda/scorecard/front/AFG/" inside the navigation bar. If everything went correctly, then the card corresponding to Afghanistan should appear with its corresponding values (set in the excel file). To generate the PDFs for all of the countries:

```sh
$ cd whoscorecards/recipients/scripts/
$ ./all_countries ../data/countries.csv
```

To join them in an unique file:
```sh
$ ./join_pdfs
```

**join_pdfs** creates two files in that same directory. The first one is all the PDF's inside the folder **output** joined. The other one is the same, but with all of the cards rotated.


### Adapting the app to work with other years

We need to create a new folder to store the info for the corresponding year:

```sh
$ cd whoscorecards/recipients/data/
$ mkdir {YEAR}
```

Inside that directory you should put the excel files with the information for each country. Make sure the names for the pages, columns and the structure of the file in general is the same for these new files and the ones that you'll find for past years.

Now you have to tell the program to grab the data from the new files. Inside the directory **whoscorecards/recipients/code/dashboard** change the Makefile, substituting the references to past data files for new ones.

In the settings for this DJango project (file **whoscorecards/recipients/code/dashboard/dashboard/settings.py**) modify the variables **FIRST_YEAR** and **LAST_YEAR** to their corresponding values.

Inside file **whoscorecards/recipients/code/dashboard/oda/views/front/indicator_table.py** change the values of the variable **GENERIC_INDICATOR_NAMES** to work with the values in your new excel files. You can see past years excel data files and python code as an example.

You can now generate the PDFs again as in step 2. Some references to pasts years will remain in the output, these are static and should be replaced manually using a vector graphics editor, such as Inkscape. The files you need to modify are the following:

- whoscorecards/recipients/code/dashboard/oda/static/svg/back.svg
- whoscorecards/recipients/code/dashboard/oda/static/svg/front.svg


# Documentación ODA Scorecards

### Instalando el proyecto

Para la siguiente documentación se asume que se utiliza una distribución de Linux basada en Debian (preferentemente Ubuntu). Primero creamos una carpeta para guardar los archivos asociados al proyecto.

```sh
$ mkdir odascorecards
```

Dentro de esa carpeta clonamos el repositorio de GitHub:

```sh
$ cd odascorecards
$ git clone https://github.com/ajgara/whoscorecards.git
```

Instalamos las dependencias de la aplicación:

```sh
$ sudo apt-get install libxml2-dev libxslt-dev texlive phantomjs pdfjam virtualenvwrapper python-pip
```

Creamos un virtual enviroment para instalar los paquetes de python necesarios:

```sh 
$ mkvirtualenv whoscorecards
```

Para trabajar dentro del entorno recién creado:

```sh
$ workon whoscorecards
```

Instalamos las dependencias de python de la aplicación:
```sh
$ pip install -r requirements.txt
```

Instalamos las fuentes utilizadas por la aplicación:
```sh
$ cp whoscorecards/recipients/code/dashboard/oda/static/fonts/* ~/.fonts/
$ sudo fc-cache -f -v
```

La aplicación ya está instalada.

### Corriendo el proyecto

Cargar los datos:
```sh
$ cd whoscorecards/recipients/code/dashboard/
$ make all
```
Cuando pida un password simplemente ingresar 'admin'.

Correr el server de DJango:
```sh
$ cd whoscorecards/recipients/code/dashboard/
$./manage.py runserver 8000
```

Ir a un navegador y probar introduciendo la URL "http://127.0.0.1:8000/oda/scorecard/front/AFG/". Debería verse la card correspondinete a Afghanistan. Para generar los pdfs para todos los países correr:

```sh
$ cd whoscorecards/recipients/scripts/
$ ./all_countries ../data/countries.csv
```

Para unir todos los pdf en uno:
```sh
$ ./join_pdfs
```

Devuelve el output en la misma carpeta, en versión rotada y no rotada.


### Adaptando los valores para años sucesivos

Hay que crear una carpeta con la información del año correspondiente:

```sh
$ cd whoscorecards/recipients/data/
$ mkdir {AÑO}
```

Introducir allí los excel con la información. Asegurarse que los nombres de las hojas, las columnas y su estructura sean iguales a la del año pasado.

Ahora hay que modificar el programa que toma los datos de los excel para que utilice los nuevos archivos. En la carpeta **whoscorecards/recipients/code/dashboard** modificar el archivo Makefile sustituyendo las referencias a los archivos por sus equivalentes para el año nuevo.

En las settings del proyecto (archivo **whoscorecards/recipients/code/dashboard/dashboard/settings.py**) modificar las variables **FIRST_YEAR** y **LAST_YEAR** a los valores correspondientes.

En el archivo **whoscorecards/recipients/code/dashboard/oda/views/front/indicator_table.py** cambiar la variable **GENERIC_INDICATOR_NAMES**, del lado derecho poner los nombres que se utilizan en el excel para denominar a las variables correspondientes.

Generar nuevamente los PDF como en el paso 2. Todas las menciones a años anteriores que todavía persistan en los archivos, deberán ser reemplazadas manualmente con un programa de edición de gráficos vectoriales, modificando los archivos:

- whoscorecards/recipients/code/dashboard/oda/static/svg/back.svg
- whoscorecards/recipients/code/dashboard/oda/static/svg/front.svg
