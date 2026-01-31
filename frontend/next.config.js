/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY: process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY,
    NEXT_PUBLIC_SENTRY_DSN: process.env.NEXT_PUBLIC_SENTRY_DSN,
  },
};

// Sentry: only wrap when org/project are set (e.g. in CI with SENTRY_AUTH_TOKEN).
// Without this, Vercel build fails with "No Sentry organization slug configured".
const { SENTRY_ORG, SENTRY_PROJECT } = process.env;
if (SENTRY_ORG && SENTRY_PROJECT) {
  const { withSentryConfig } = require("@sentry/nextjs");
  module.exports = withSentryConfig(nextConfig, {
    silent: true,
    org: SENTRY_ORG,
    project: SENTRY_PROJECT,
  });
} else {
  module.exports = nextConfig;
}
