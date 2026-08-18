import type { NextConfig } from "next";

const isPagesEnv = process.env.GITHUB_PAGES === "true";

const nextConfig: NextConfig = {
  output: "export",
  ...(isPagesEnv && {
    basePath: "/meu-projeto",
    assetPrefix: "/meu-projeto",
  }),
};

export default nextConfig;
