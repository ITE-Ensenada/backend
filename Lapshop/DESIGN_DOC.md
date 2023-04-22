# LAPSHOP Prime

Author(s): Miguel A. & Andre C.

Status: [Draft, Ready for review, In Review, Reviewed]

Ultima actualización: 2023-02-27

## Contenido
- Goals
- Non-Goals
- Background
- Overview
- Detailed Design
  - Solucion 1
    - Frontend
    - Backend
- Consideraciones
- Métricas

## Links
- [Al Repositorio](https://github.com/AndreCaze/Python)

## Objetivo
Una aplicacion web para facilitar el proceso de compra de laptops nuevas, usadas, y reconstruidas.

_Incluye contexto para las personas que no están familiarizadas con el proyecto._

## Goals
- Proveer un catalogo completo de laptops de diversos fabricantes.
- Facilitar el proceso de compra de laptops.
- Ofrecer una extensa lista de componentes personalizables para cada laptop.
## Non-Goals
- Incluir computadores de escritorio, celulares, tabletas u otros dispositivos diferentes a las laptops.
- Venta de componentes por separado.

## Background
Hace poco estuvimos viendo cuantas APIs hay dedicada a la venta de Laptops, y descubrimos que casi todas ofrecian laptops nuevas o proveian de un catalogo minusculo de componentes extras de laptops.

Actualmente los usuarios de Laptops requieren dispositivos que se adapten a sus necesidades o situaciones donde los componentes que tienen no son suficientes para el trabajo que desean desempeñar

_Incluye recursos, como otros design docs si es necesario_

_No escribas acerca de tu diseño o requerimientos aquí_

## Overview
Necesitamos un API que contenga todas las marcas de Laptops y todos los componentes que se le pueden agregar a una.

Cada Laptop tendra una id, en la cual se podra consultar su existencia o disponibilidad junto con cualquier componente que se le quiera añadir.

Los End Points tendran el siguiente formato:
- 1.-/v0.1/LapShopP/laptops
- 2.-/v0.1/LapShopP/laptops/all
- 3.-/v0.1/LapShopP/manufacturer/all
- 4.-/v0.1/LapShopP/processor/all
- 5.-/v0.1/LapShopP/graphics/all
- 6.-/v0.1/LapShopP/series/all
- 7.-/v0.1/LapShopP/ram/all
- 8.-/v0.1/LapShopP/screens/all
- 9.-/v0.1/LapShopP/storages/all
- 10.-/v0.1/LapShopP/about
- 11.-/v0.1/LapShopP/about/terms-of-use

_Esta sección debería ser entendible por nuevos miembros de tu equipo que no están relacionados al proyecto_

_Pon detalles en la siguiente sección_

## Detailed Design
_Usa diagramas donde veas necesario_

_Herramientas como [Excalidraw](https://excalidraw.com) son buenos recursos para esto_

_Cubre los cambios principales:_

 _- Cuales son las nuevas funciones que vas a escribir?_
 _- Porque necesitas nuevos componentes?_
 _- Hay código que puede ser reusable?_

_No elabores minuciosamente la implementación._

## Solution 1
### Frontend
_Frontend…_
### Backend
_Backend…_

## Consideraciones
_Preocupaciones / trade-offs / tech debt_

## Métricas
_Que información necesitas para validar antes de lanzar este feature?_
