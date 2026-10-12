# Источники и ограничения

Обязательные источники:
- OpenAI Deployment Safety Hub, GPT-6 Astra System Card / Sol-Luna appendix: https://deploymentsafety.openai.com/gpt-6-astra/sec%3Aappendix-sol-luna
- OpenAI Safety overview: https://openai.com/index/safety-overview-gpt-6-astra/
- OpenAI GPT-6 Astra: https://openai.com/index/gpt-6-astra/
- ARC-AGI-2: https://arcprize.org/arc-agi/2
- ARC Prize 2026 ARC-AGI-2: https://arcprize.org/competitions/2026/arc-agi-2
- ARC Prize 2026 ARC-AGI-3: https://arcprize.org/competitions/2026/arc-agi-3

Из публичных материалов OpenAI перенесены инженерные принципы: соблюдение authorized scope, изоляция, least privilege, blocking evaluations, мониторинг действий и траекторий, red-team/regression tests, human escalation. Мониторинг — дополнительный слой, не замена alignment; CoT-only monitoring имеет ограничения, поэтому нужны наблюдаемые действия и независимые контроли.

ARC-AGI — ориентир для тестирования обобщения/эффективности, не доказательство финансовой эффективности. «Sol/Luna» — имена моделей в system card; «планировщик + контролёр» здесь — наш проектный паттерн, а не требование OpenAI.

Вложение `Anthropic(2).txt` подчёркивает: сильный агент — это system + context + tools + loop + selective subagents + durable state + verification + evals, а не один магический промпт. Это синтез, а не официальный prompt Anthropic.

Загрузка архива в чат не создаёт принудительную системную политику. Данные marketplace быстро меняются; перепроверять актуальные условия перед каждой задачей.
