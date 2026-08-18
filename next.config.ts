import type { NextConfig } from "next";

const isPagesEnv = process.env.GITHUB_PAGES === "true";
const basePath = isPagesEnv ? "/meu-projeto" : "";

const nextConfig: NextConfig = {
  output: "export",
  ...(isPagesEnv && { basePath, assetPrefix: basePath }),
  env: { NEXT_PUBLIC_BASE_PATH: basePath },
};

export default nextConfig;
