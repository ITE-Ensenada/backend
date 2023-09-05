import React from 'react'
import { Grafica } from '../components/Grafica'

export const TablaComposicion = ({ porcentajes, masas, densidad }) => {
  return (
    <div className='w-3/4  h-fit p-4 rounded-md'>
      <h1 className='text-xl font-bold mb-2'>Resultados</h1>

      <table className='w-full table-auto text-left border-collapse border-y mb-2 bg-terciary'>
        <thead>
          <tr>
            <th>
              Componente
            </th>
            <th>
              Porcentaje
            </th>
            <th>
              Kilogramos
            </th>
          </tr>
        </thead>
        <tbody>
          <tr className='border-y'>
            <td>
              Masa grasa
            </td>
            <td>
              {(porcentajes.masa_grasa / 10).toFixed(2)} %
            </td>
            <td>

              {masas.masa_grasa.toFixed(2)} kg
            </td>
          </tr>

          <tr className='border-y'>
            <td>
              Masa osea
            </td>
            <td>

              {(porcentajes.masa_osea.toFixed(2) / 100).toFixed(2)} %
            </td>
            <td>
              {masas.masa_osea.toFixed(2)} kg
            </td>
          </tr>

          <tr className='border-y'>
            <td>
              Masa residual
            </td>

            <td>

              {(porcentajes.masa_residual).toFixed(2)} %
            </td>

            <td>
              {masas.masa_residual} kg
            </td>
          </tr>

          <tr>
            <td>
              Masa muscular
            </td>
            <td>
              {((porcentajes.masa_muscular / 100).toFixed(2)) * -1} %
            </td>
            <td>
              {masas.masa_muscular.toFixed(2)} kg
            </td>
          </tr>

        </tbody>
      </table>
      <span> Densidad corporal: {densidad.toFixed(3)} </span>

      <div className='w-full hsm:h-screen md:h-screen lg:h-auto '>
        <Grafica masa_osea={(porcentajes.masa_osea.toFixed(2) / 100)} masa_grasa={(porcentajes.masa_grasa.toFixed(2) / 10)}
          masa_muscular={((porcentajes.masa_muscular.toFixed(2) / 100) * -1)} masa_residual={(porcentajes.masa_residual).toFixed(2)} /></div>
    </div >

  )
}