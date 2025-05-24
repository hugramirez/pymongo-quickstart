# MongoDB + PyMongo Quickstart con Datos de ECOBICI CDMX

<img src="https://ecobici.cdmx.gob.mx/wp-content/uploads/2025/02/logo-ecobici-2025.png" alt="Ecobici CDMX" width="120"/>

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-%E2%89%A53.6-green.svg)](https://www.mongodb.com/)
[![PyMongo](https://img.shields.io/badge/pymongo-%E2%89%A54.0-brightgreen.svg)](https://pymongo.readthedocs.io/)
[![pandas](https://img.shields.io/badge/pandas-%E2%89%A51.3-brightgreen.svg)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Este proyecto es una guía de inicio rápido para trabajar con **MongoDB** usando **PyMongo**, aplicándolo sobre un dataset real de viajes de bicicletas públicas proporcionado por **ECOBICI CDMX**. A través de este repositorio aprenderás cómo importar, consultar, filtrar y analizar datos estructurados en una base de datos MongoDB, aprovechando las capacidades de búsqueda, agregación y modelado flexible de documentos.

Ideal para desarrolladores, analistas de datos y entusiastas de la movilidad urbana que quieran explorar datos reales con una base de datos NoSQL moderna.

## Tabla de Contenidos

- [Instalación](#instalación)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Ingesta de Datos automatizada](#ingesta-de-datos-automatizada-desde-ecobici-cdmx)
- [Carga de Datos en MongoDB](#carga-de-datos-en-mongodb)
- [Consultas Básicas](#consultas-básicas)
- [Ejemplos de Agregación](#ejemplos-de-agregación)
- [Aplicaciones y Visualización](#aplicaciones-y-visualización)
- [Markmap del Dataset](#markmap-del-dataset)
- [Licencia](#licencia)

## Instalación

Este proyecto utiliza **Python 3.8+**, **MongoDB** y las librerías `pymongo`, `pandas` y `python-dotenv`. Se recomienda trabajar dentro de un entorno virtual.

#### 1. Clona este repositorio

```bash
git clone https://github.com/tu-usuario/pymongo-quickstart.git
cd pymongo-quickstart
```

#### 2. Crea un entorno virtual

Se recomienda crear un entorno virtual para evitar conflictos con otras instalaciones de Python.

En macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

En Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

####  3. Instala las dependencias

Instala las librerías necesarias utilizando pip:

```bash
pip install -r requirements.txt
```

Contenido sugerido del archivo requirements.txt:

```text
pymongo>=4.0
pandas>=1.3
python-dotenv>=1.0
```

#### 4. Configura tu entorno de conexión

Para que el proyecto pueda conectarse a MongoDB, necesitas una instancia de base de datos en ejecución. Puedes usar MongoDB **localmente** o desde la nube con **MongoDB Atlas**.

##### Puedes Instalar MongoDB localmente

- Descarga e instala MongoDB Community Edition desde el sitio oficial:  
   [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)

- Una vez instalado, inicia el servidor MongoDB (puede iniciar automáticamente como servicio en algunos sistemas):

```bash
   mongodhivo
```

Crea un archivo .env en la raíz del proyecto con el siguiente contenido:

```env
MONGODB_URI=mongodb://localhost:27017
```

### Estructura del Proyecto

### Ingesta de Datos automatizada desde Ecobici CDMX

La **ingesta de datos** es el proceso de recopilación e importación de archivos provenientes de diversas fuentes hacia una base de datos para su posterior almacenamiento, procesamiento y análisis. En este proyecto, la ingesta se automatiza mediante técnicas de **web scraping** utilizando `BeautifulSoup`, con las que se exploran las páginas oficiales de Ecobici CDMX para extraer dinámicamente los enlaces públicos a archivos `.csv` históricos.

Una vez recopilados, estos archivos se limpian, transforman y almacenan en una base de datos **MongoDB**, creando así un repositorio centralizado y coherente de datos de movilidad urbana. Esta estructura permite realizar análisis estructurados, consultas eficientes y visualizaciones, sentando las bases para tareas posteriores de análisis avanzado o minería de datos.

