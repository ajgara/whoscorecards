# Documentation for ODA Scorecards

### Installing the app

This guide assumes you're using Ubuntu or another Debian based Linux distribution. In case of using the already existing VM environment you can omit the following steps and jump straight to the **Running the app** section.

First we create a directory to store the files for the project:

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

To generate the PDF for a specific country:

```sh
./make COUNTRY_ISO=ARG COUNTRY_NAME=Argentina
```

To join them in an unique file:
```sh
$ ./join_pdfs
```

**join_pdfs** creates two files in that same directory. The first one is all the PDF's inside the folder **output** joined. The other one is the same, but with all of the cards rotated.

You can also generate output checksum excels with the data shown in the PDFs. To do so you can enter the following URL's onto your web browser navigation bar:

First Page
```
http://localhost:8000/oda/front/xls/table-1/
http://localhost:8000/oda/front/xls/purpose-commitment/
http://localhost:8000/oda/front/xls/purpose-disbursement/
```

Second Page
```
http://localhost:8000/oda/back/xls/data
```

### Adapting the app to work with other years

We need to create a new folder to store the info for the corresponding year:

```sh
$ cd whoscorecards/recipients/data/
$ mkdir {YEAR}
```

Inside that directory you should put the excel files with the information for each country. Make sure the names for the pages, columns and the structure of the file in general is the same for these new files and the ones that you'll find for past years. If names were changed you'll need to modify the files inside **whoscorecards/recipients/code/dashboard/oda/management/commands**.

**Important note:** make sure that the main csv file, with the recipient countries for the current year, only contains **LF (line feed)** at the end of each line instead of containing **CRLF (carriage return plus line feed)**.

Now you have to tell the program to grab the data from the new files. Inside the directory **whoscorecards/recipients/code/dashboard** change the Makefile, substituting the references to past data files for new ones.

In the settings for this DJango project (file **whoscorecards/recipients/code/dashboard/dashboard/settings.py**) modify the variables **FIRST_YEAR** and **LAST_YEAR** to their corresponding values.

Inside the file **whoscorecards/recipients/code/dashboard/oda/views/front/indicator_table.py** change the values of the variable **GENERIC_INDICATOR_NAMES** to work with the values in your new excel files. You can see past years excel data files and python code as an example.

Inside the file **whoscorecards/recipients/code/dashboard/oda/views/front/data.py** change the value of the variable **hd_indicator** to match the name of the ODA for Health Disbursements indicator for the **LAST_YEAR** in your new excel files. Also check that there's no need for adding new per-country base year overrides for indicating the starting year from which there is information available on those countries. This is stored in the **overrides** array variable. Finally, update the **base_year** and **last_year** variables as well.

You can now generate the PDFs again as in step 2. **Some references to pasts years will remain in the output, these are static and should be replaced manually using a vector graphics editor, such as Inkscape. The files you need to modify are the following:**

- whoscorecards/recipients/code/dashboard/oda/static/svg/back.svg
- whoscorecards/recipients/code/dashboard/oda/static/svg/front.svg

Also make sure to update the two backpages textboxes with the new texts.

### Adding bleeds and cropmarks

The process of adding bleeds and cropmarks should be done by a designer based on the (non rotated) comprehensive pdf. The following steps will need to be performed (roughly):

1. Download the MultiPageImporter script (v2.5 or later) for Adobe InDesign.
2. Configure the script on Adobe InDesign.
3. Set the correct page size before importing the comprehensive pdf.
4. Run the MultiPageImporter script to import all the pdf pages into an Adobe InDesign document. Set the cropmarks to "Crop" when importing.
5. Create, or use a previously created **front** master template which add rectangles of different colors (grey and magenta) to simulate the bleed for the front page. Apply this template to the back layer of all pages.
6. Create, or use a previously created **back** master template which add rectangles of different colors (grey and magenta) to simulate the bleed for the back page. Apply this template to the back layer of all **even** pages.
7. Export the Adobe InDesign document to pdf.
8. Use Acrobat Writer, or other pdf editting software, for rotating all pages 90 degrees counterclockwise.

# Documentación ODA Scorecards

### Instalando el proyecto

Para la siguiente documentación se asume que se utiliza una distribución de Linux basada en Debian (preferentemente Ubuntu). En caso de utilizar el entorno VM existente omitir los siguientes pasos e ir directamente a la sección **Corriendo el proyecto**.

Primero creamos una carpeta para guardar los archivos asociados al proyecto.

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

Introducir allí los excel con la información. Asegurarse que los nombres de las hojas, las columnas y su estructura sean iguales a la del año pasado. Si los nombres fueron modificados hay que actualizar los archivos dentro de la carpeta **whoscorecards/recipients/code/dashboard/oda/management/commands**.

**Importante:** Asegurarse que el archivo csv principal, que tiene los paises que se procesarán para el año en curso, solo contienga **LF (line feed)** al final de cada línea en vez de **CRLF (carriage return y line feed)**.

Ahora hay que modificar el programa que toma los datos de los excel para que utilice los nuevos archivos. En la carpeta **whoscorecards/recipients/code/dashboard** modificar el archivo Makefile sustituyendo las referencias a los archivos por sus equivalentes para el año nuevo.

En las settings del proyecto (archivo **whoscorecards/recipients/code/dashboard/dashboard/settings.py**) modificar las variables **FIRST_YEAR** y **LAST_YEAR** a los valores correspondientes.

En el archivo **whoscorecards/recipients/code/dashboard/oda/views/front/indicator_table.py** cambiar la variable **GENERIC_INDICATOR_NAMES**, del lado derecho poner los nombres que se utilizan en el excel para denominar a las variables correspondientes.

En el archivo **whoscorecards/recipients/code/dashboard/oda/views/front/data.py** cambiar el valor de la variable **hd_indicator** para coincidir con el nombre del indicador de ODA for Health Disbursements del **LAST_YEAR** que se utiliza en los nuevos excels. También asegurarse de que no sea necesario agregar overrides para el "año base" de cada país, que indica desde que año existe información disponible para dichos países. Esta información se guarda en la variable array **overrides**. Por último, actualizar los valores de las variables **base_year** y **last_year**.

Generar nuevamente los PDF como en el paso 2. **Todas las menciones a años anteriores que todavía persistan en los archivos, deberán ser reemplazadas manualmente con un programa de edición de gráficos vectoriales, como el Inkscape, modificando los archivos:**

- whoscorecards/recipients/code/dashboard/oda/static/svg/back.svg
- whoscorecards/recipients/code/dashboard/oda/static/svg/front.svg

También asegurarse de modificar los dos cuadros de texto de las backpages con los textos actualizados.

### Agregando demasía y marcas de corte

El proceso de agregado de demasía y marcas de corte debe ser realizado por un diseñador basandose en el pdf (no rotado) que contiene todos los países juntos. El proceso consta (aproximadamente) de los siguientes pasos:

1. Descargar el script MultiPageImporter (v2.5 o superior) para Adobe InDesign.
2. Configurar el script en Adobe InDesign.
3. Configurar el tamaño correcto de página antes de importar el pdf.
4. Ejecutar el script MultiPageImporter para importar todas las hojas del pdf en un documento de Adobe InDesign. Elegir la opcion "Crop" para los cropmarks al realizar la importación.
5. Crear, o utilizar el template maestro **front** previamente creado que le agrega rectángulos de diferentes colores (grises y violetas) que se extienden de los extremos para simular demasía en la front page y aplicarlo al layer de fondo de todas las páginas.
6. Crear, o utilizar el template maestro **back** previamente creado que le agrega rectángulos de diferentes colores (grises y violetas) que se extienden de los extremos para simular demasía en la back page y aplicarlo al layer de fondo de todas las páginas **pares**.
7. Exportar el documento de Adobe InDesign a pdf.
8. Usar el Acrobat Writer, o algún otro software de edición de pdfs, para rotar 90 grados contra reloj las hojas del documento.
