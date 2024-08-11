/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  env: {
    API_URL: process.env.API_URL || "http://localhost:80/api",
  },
};

export default nextConfig;
