#!/bin/bash
# APSA-2026 Marketplace Registration
# Запуск: PUBLIC_URL=https://your-url.vercel.app bash register.sh
set -e

URL="${PUBLIC_URL:-}"
if [ -z "$URL" ]; then
  echo "❌ Укажи URL: PUBLIC_URL=https://your-url.vercel.app bash register.sh"
  exit 1
fi

echo "🚀 Регистрация на маркетплейсах..."
echo "   URL: $URL"
echo ""

# 1. Agent402
echo "📋 1/3: Agent402..."
curl -s -X POST https://agent402.tools/api/index/register \
  -H "Content-Type: application/json" \
  -d "{\"endpoint\":\"${URL}/api/market-analysis\",\"manifest\":\"${URL}/.well-known/x402-manifest.json\",\"serviceId\":\"market-analysis\",\"price\":0.05,\"network\":\"base-mainnet\",\"payTo\":\"0x829f877daAb94D766BB2b8511ad486C40f2C2BDA\"}" \
  && echo " ✅" || echo " ❌ (попробуй позже)"

echo ""
echo "📋 2/3: SentinelShield на Agent402..."
curl -s -X POST https://agent402.tools/api/index/register \
  -H "Content-Type: application/json" \
  -d "{\"endpoint\":\"${URL}/api/x402/sentinelshield\",\"manifest\":\"${URL}/.well-known/x402-manifest.json\",\"serviceId\":\"sentinel-shield\",\"price\":9.5,\"network\":\"base-mainnet\",\"payTo\":\"0x829f877daAb94D766BB2b8511ad486C40f2C2BDA\"}" \
  && echo " ✅" || echo " ❌"

echo ""
echo "📋 3/3: Проверка manifest..."
curl -s "${URL}/.well-known/x402-manifest.json" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(f'  Services: {len(d.get(\"services\",[]))}'); [print(f'    {s[\"serviceId\"]}: \${s[\"priceUSDC\"]}') for s in d.get('services',[])]" 2>&1 || echo "  ❌ manifest недоступен"

echo ""
echo "✅ Регистрация завершена!"
echo "   Покупатели могут найти эндпоинты через Agent402"
