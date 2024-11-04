// src/utils/utils.js

const CHART_COLORS = {
    red: 'rgba(255, 99, 132, 1)',
    blue: 'rgba(54, 162, 235, 1)',
    green: 'rgba(75, 192, 192, 1)',
    yellow: 'rgba(255, 206, 86, 1)',
    orange: 'rgba(255, 159, 64, 1)',
    purple: 'rgba(153, 102, 255, 1)',
    grey: 'rgba(201, 203, 207, 1)'
};

// Fonction pour rendre une couleur transparente
const transparentize = (color, opacity) => {
    const rgba = color.replace(/^rgba?\(([^)]+)\)$/, (match, p1) => {
        const rgbaValues = p1.split(',').map(Number);
        return `rgba(${rgbaValues[0]}, ${rgbaValues[1]}, ${rgbaValues[2]}, ${opacity})`;
    });
    return rgba;
};

// Exportez les constantes et les fonctions
export default {
    CHART_COLORS,
    transparentize
};
