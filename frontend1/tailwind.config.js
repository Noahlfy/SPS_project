/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html', 
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Poppins', 'sans-serif']
      },
      gridTemplateColumns: {
        '70/30': '70% 28%',
      },
      colors: {
        primary: 'var(--primary-color)',
        secondary: 'var(--secondary-color)',
      },
      spacing: {
        '128': '32rem',    // Ajoute une marge/padding de 128 unités (512px)
        '144': '36rem',    // Ajoute une marge/padding de 144 unités (576px)
      },
      maxWidth: {
        '8xl': '90rem',    // Ajoute une largeur maximale personnalisée
        '9xl': '100rem',
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}

