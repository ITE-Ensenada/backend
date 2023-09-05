'use client'

import { FormularioCompCorporal } from '../components/FormularioCompCorporal'
import { TablaComposicion } from '../components/TablaComposicion'
import React, { useState } from 'react'

export const Densidad = () => {


  const [densidad, setDensidad] = useState(null)

  const [porcentajes, setPorcentajes] = useState({
    masa_osea: null,
    masa_grasa: null,
    masa_residual: null,
    masa_muscular: null
  })

  const [masas, setMasas] = useState({
    masa_osea: null,
    masa_grasa: null,
    masa_residual: null,
    masa_muscular: null

  })

  const calcularDensidad = (inputValues) => {
    const { genero, bicep, tricep, subscapular, supraileaco, femur, bistiloideo, talla, peso } = inputValues;

    const sumaPliegues = inputValues.tricep + inputValues.bicep + inputValues.subscapular + inputValues.supraileaco;
    console.log(sumaPliegues)

    const calcularMasaOsea = () => {
      return Math.pow(Math.pow(talla, 2) * (femur / 100) * (bistiloideo / 100) * 400, 0.712) * 3.02;
    };

    const calcularDensidadYResidual = () => {
      let densidadCorporal;
      let residual;

      if (inputValues.genero === 'hombre' || genero === 'mujer') {
        if (inputValues.genero === 'hombre') {
          densidadCorporal = 1.1765 - (0.0744 * Math.log10(sumaPliegues));
        } else {
          densidadCorporal = 1.1567 - (0.0717 * Math.log10(sumaPliegues));
        }

        if (inputValues.genero === 'hombre') {
          residual = peso * 0.24;
        } else {
          residual = peso * 0.21;
        }

      } else {
        console.log('El género debe ser "hombre" o "mujer" para realizar el cálculo.');
      }

      return { densidadCorporal, residual };
    };

    const densidadYMasas = () => {
      const { densidadCorporal, residual } = calcularDensidadYResidual();
      setDensidad(densidadCorporal);



      //Porcentajes
      const grasa = (495 / densidadCorporal) - 450;
      const porcentajeMasaOsea = (calcularMasaOsea() * 100) / peso;
      const porcentajeMasaResidual = (residual / peso) * 100;
      const porcentajeMasaMuscular = 100 - (grasa + porcentajeMasaOsea + porcentajeMasaResidual);


      //Masas
      const masaGrasaKilos = peso * (grasa / 100);
      const masaMuscularKilos = peso - (masaGrasaKilos + calcularMasaOsea() + residual);

      setMasas((prevValues) => ({
        ...prevValues,
        masa_osea: calcularMasaOsea(),
        masa_grasa: masaGrasaKilos,
        masa_muscular: masaMuscularKilos,
        masa_residual: residual,
      }));

      setPorcentajes((prevValues) => ({
        ...prevValues,
        masa_osea: porcentajeMasaOsea,
        masa_grasa: grasa,
        masa_muscular: porcentajeMasaMuscular,
        masa_residual: porcentajeMasaResidual,
      }));
    };

    densidadYMasas();
  };




  return (
    <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-2 gap-4 bg-secondary p-4 md:p-8 h-auto md:h-screen'>

      <FormularioCompCorporal calcularDensidad={calcularDensidad} />


      {densidad && <TablaComposicion porcentajes={porcentajes} masas={masas} densidad={densidad} />}

    </div>
  )
}

export default Densidad