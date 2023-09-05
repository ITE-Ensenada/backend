import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

export const Grafica = ({ masa_osea, masa_grasa, masa_muscular, masa_residual }) => {
    const chartRef = useRef(null);

    useEffect(() => {
        if (chartRef.current) {
            new Chart(chartRef.current, {
                type: 'pie',
                data: {
                    labels: ['Masa Ósea', 'Masa Grasa', 'Masa Muscular', 'Masa Residual'],
                    datasets: [{
                        data: [masa_osea, masa_grasa, masa_muscular, masa_residual],
                        backgroundColor: ['red', 'blue', 'yellow', 'green'],
                    }],
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                        },
                    },
                },
            });
        }
    }, [masa_osea, masa_grasa, masa_muscular, masa_residual]);

    return (
        <div style={{ width: '600px', height: '600px', backgroundColor: 'gray' }}>
            <h1>Gráfica de Pastel</h1>
            <canvas ref={chartRef} id="pieChart"></canvas>
        </div>
    );
};
