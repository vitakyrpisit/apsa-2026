#!/bin/bash
# APSA-2026 Deploy Script —一键 деплой на Vercel
# Запуск: bash deploy.sh
set -e

echo "🚀 APSA-2026 Deploy на Vercel"
echo ""

# Проверка vercel CLI
if ! command -v vercel &> /dev/null; then
  echo "📦 Установка Vercel CLI..."
  npm install -g vercel
fi

echo "📋 Шаг 1: Деплой..."
vercel --prod --yes

echo ""
echo "✅ Деплой завершен!"
echo ""
echo "📋 Шаг 2: Получи URL из вывода выше"
echo "   Например: https://apsa-2026.vercel.app"
echo ""
echo "📋 Шаг 3: Сохрани URL и сообщи агенту"
echo "   URL нужен для регистрации на Agent402 + x402dash"
echo ""
