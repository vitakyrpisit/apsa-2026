import { NextResponse } from "next/server";
import { EVM_PAYOUT_ADDRESS, BASE_USDC_MAINNET_ADDRESS } from "@/lib/apsa/wallet-registry";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  return NextResponse.json({
    openapi: "3.1.0",
    info: { title: "APSA-2026 x402 Services", version: "2.0.0" },
    servers: [{ url: "https://apsa-2026.vercel.app" }],
    "x402": {
      version: "2.0",
      payoutAddress: EVM_PAYOUT_ADDRESS,
      payoutMode: "receive-only",
      network: "eip155:8453",
      token: "USDC",
      tokenAddress: BASE_USDC_MAINNET_ADDRESS,
    },
    paths: {
      "/api/x402/sentinelshield": {
        post: {
          "x-payment-info": { price: "$9.50 USDC", atomic: "9500000", scheme: "exact" },
          "x-bazaar": { serviceName: "SentinelShield", tags: ["security","audit","sarif"], mimeType: "application/json" },
          responses: { "402": { description: "Payment Required" }, "200": { description: "SARIF report" } },
        },
      },
      "/api/market-analysis": {
        post: {
          "x-payment-info": { price: "$0.05 USDC", atomic: "50000", scheme: "exact" },
          "x-bazaar": { serviceName: "Market Analysis", tags: ["market","analysis","crypto"], mimeType: "application/json" },
          parameters: [{ name: "symbol", in: "query", required: true, schema: { type: "string", enum: ["BTC","ETH","USDC","BASE","SOL","TRX"] } }],
          responses: { "402": { description: "Payment Required" }, "200": { description: "LLM market analysis" } },
        },
      },
      "/api/market-signal": {
        post: {
          "x-payment-info": { price: "$0.001 USDC", atomic: "1000", scheme: "exact" },
          "x-bazaar": { serviceName: "Market Signal", tags: ["trading","signal","snapshot"], mimeType: "application/json" },
          parameters: [{ name: "symbol", in: "query", required: true, schema: { type: "string", enum: ["BTC","ETH","USDC","BASE","SOL","TRX"] } }],
          responses: { "402": { description: "Payment Required" }, "200": { description: "Trading signal snapshot" } },
        },
      },
      "/api/site-audit": {
        post: {
          "x-payment-info": { price: "$0.25 USDC", atomic: "250000", scheme: "exact" },
          "x-bazaar": { serviceName: "Site Audit", tags: ["security","audit","seo","performance"], mimeType: "application/json" },
          parameters: [{ name: "url", in: "query", required: true, schema: { type: "string" } }],
          responses: { "402": { description: "Payment Required" }, "200": { description: "Site audit report" } },
        },
      },
      "/api/company-intel": {
        post: {
          "x-payment-info": { price: "$0.50 USDC", atomic: "500000", scheme: "exact" },
          "x-bazaar": { serviceName: "Company Intelligence", tags: ["business","intelligence","research"], mimeType: "application/json" },
          parameters: [{ name: "name", in: "query", required: true, schema: { type: "string" } }],
          responses: { "402": { description: "Payment Required" }, "200": { description: "B2B intelligence report" } },
        },
      },
      "/api/price": { get: { "x-free": true, parameters: [{ name: "symbol", in: "query" }], responses: { "200": { description: "Crypto price" } } } },
      "/api/x402": { get: { "x-free": true, responses: { "200": { description: "Service catalog" } } } },
      "/api/health": { get: { "x-free": true, responses: { "200": { description: "Health" } } } },
    },
  }, { headers: { "Content-Type": "application/json", "Cache-Control": "public, max-age=300" } });
}
