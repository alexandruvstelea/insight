import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
     
      colors: {
        'blue-dark': 'var(--main-blue-dark)',
        'blue-light': 'var(--main-blue-light)',
      },
      backgroundImage: {
        'gradient': 'var(--main-gradient)',
      },
    },
  },
  plugins: [],
};
export default config;
