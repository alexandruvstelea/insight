/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    REACT_APP_API_URL: "http://fiesc-backend:5000", // REACT_APP_API_URL: 'http://127.0.0.1:5000',
    GOOGLE_ANALYTICS: "G-VPQDW8R82P",
  },
};

module.exports = nextConfig;
