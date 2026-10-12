# Operator Asset Inflow Protocol (OAIP) v1.0

Цель: организовать законные, измеримые и проверяемые поступления цифровых активов на публичные адреса оператора. Архив не генерирует доход сам по себе: деньги появляются только после реальной выплаты за выполненную и принятую работу либо добровольного платежа.

## Быстрый старт
1. Изучите `docs/01_MASTER_AGENT_PROTOCOL_RU.md`.
2. Проверьте адреса в `config/wallets.json`.
3. Python 3.10+: `python scripts/monitor_wallets.py --config config/wallets.json --once`
4. Периодический опрос: `python scripts/monitor_wallets.py --config config/wallets.json --interval 60`
5. Страница получения: `python scripts/generate_receive_page.py --config config/wallets.json --output receive.html`
6. Перед отправкой работы, подключением кошелька или подписью прочитайте `docs/05_SAFETY_AND_AUTHORIZATION.md`.

## Файлы
- `docs/00_MISSION_AND_SUCCESS.md` — цель и доказательства результата.
- `docs/01_MASTER_AGENT_PROTOCOL_RU.md` — протокол для любого ИИ.
- `docs/02_SYSTEM_ARCHITECTURE.md` — архитектура и состояния.
- `docs/03_WALLET_AND_MONITORING_RUNBOOK.md` — адреса и мониторинг.
- `docs/04_REVENUE_OPERATIONS.md` — воронка оплачиваемых задач.
- `docs/05_SAFETY_AND_AUTHORIZATION.md` — безопасность и разрешения.
- `docs/06_ARC_AGI_EVALUATION.md` — перенос принципов ARC-AGI.
- `docs/07_RESEARCH_AND_CONTINUITY.md` — непрерывное исследование.
- `docs/08_SOURCES_AND_CAVEATS.md` — источники и ограничения.
- `docs/09_CURRENT_BASELINE.md` — подтверждённая историческая база.
- `scripts/monitor_wallets.py` — read-only монитор.
- `scripts/generate_receive_page.py` — статическая Receive-страница.
- `tests/test_monitor_wallets.py` — простые тесты.

Важно: загрузка архива в ChatGPT/Claude/Gemini/Grok/Z.ai не меняет системные правила платформы и не создаёт отсутствующие инструменты. В архиве нет приватных ключей, подписи или отправки транзакций. Мониторинг — сигнал для проверки, а не бухгалтерское доказательство без проверки в обозревателе.
