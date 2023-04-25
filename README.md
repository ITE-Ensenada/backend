# Animeinfo

## Objetivo

Que y porque estamos haciendo esto?

El Anime como se le conoce al tipo de animacion japonesa, cada dia toma
mas auge y relevancia fuera del pais nipon. Debido a que el anime tiene
una gran cantidad de información es que se diseño Animeinfo.

### Objetivos especificos

- Brindar informacion sobre animes modernos como antiguos.

-  Sitio web amigable para navegar.

- Herramientas de busqueda especifica.

### No Objetivos

- No venderemos merchandise como blu-ray en la pagina.

- No apoyaremos a paginas que trasmiten anime de forma ilegal ni que tenemos la intension de incentivar la practica.

- No mostraremos como contenido principal material para adulto.

## Background

Cuál es el contexto de este proyecto?

Incluye recursos, como otros design docs si es necesario

No escribas acerca de tu diseño o requerimientos aquí

## Overview

Overview a alto nivel de tu propuesta

Esta sección debería ser entendible por nuevos miembros de tu equipo que no están relacionados al proyecto

Pon detalles en la siguiente sección

## Detailed Design

Usa diagramas donde veas necesario

Herramientas como Excalidraw son buenos recursos para esto

Cubre los cambios principales:

- Cuales son las nuevas funciones que vas a escribir? - Porque necesitas nuevos componentes? - Hay código que puede ser reusable?

No elabores minuciosamente la implementación.

## Instalación

Los siguientes pasos son necesarios para la instalacion de la api Animeinfo.

El proyecto fue construido en python 3.8

Instalar el modulo virtualenv

    pip install virtualenv

Crear el entorno virtual

    python -m venv venv

Activar el entorno virtual

    venv\Scripts\activate.bat

Instalar los requirements

    pip install -r requirements.txt

Ejecutar flask

    flask --app main run


## End poins API
0.	https://api.animeinfo.com/v1/anime/all

1.	https://api.animeinfo.com/v1/anime/{anime-id}

2.	https://api.animeinfo.com/v1/anime/ranking

3.	https://api.animeinfo.com/v1/anime/season/{year}/{season}

4.	https://api.animeinfo.com/v1/anime/search/{title}

5.	https://api.animeinfo.com/v1/anime/characters/{name}

6.	https://api.animeinfo.com/v1/anime/{genre}

7.	https://api.animeinfo.com/v1/anime/rating

8.	https://api.animeinfo.com/v1/anime/recommendations/{anime-id}

9.	https://api.animeinfo.com/v1/anime/status/{start-date}{end-date}

10.	https://api.animeinfo.com/v1/anime/autor/{mangaka}
