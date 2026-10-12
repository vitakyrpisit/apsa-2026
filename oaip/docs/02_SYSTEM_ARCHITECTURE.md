# Архитектура

Компоненты: Opportunity Scout → Eligibility & Payout Gate → Task Planner → Executor → Independent Reviewer → Submission Tracker → Settlement Verifier → Evidence Ledger → Research Loop. Для рискованных внешних действий предусмотрен Human Approval Gate.

Состояния: `DISCOVERED → SCREENED → ELIGIBLE → PLANNED → IN_PROGRESS → SUBMITTED → ACCEPTED → PAYOUT_PENDING → ONCHAIN_CONFIRMED → ATTRIBUTED → CLOSED`. Дополнительно: `REJECTED`, `EXPIRED`, `BLOCKED`, `FAILED`, `DISPUTED`, `UNVERIFIED`.

Нельзя переходить в `ACCEPTED` без доказательства приёмки, `ONCHAIN_CONFIRMED` — без подтверждения сети, `ATTRIBUTED` — без связи выплаты с задачей.

Каждая возможность хранит: стабильный ID, URL источника, дату UTC, дедлайн, задачу, критерии приёмки, payout-актив/сеть/сумму, комиссии, депозит/KYC/подпись, риски, статус и evidence URLs.

Рекомендации: простые модули Python/TypeScript; таймауты/backoff/rate limits; SQLite/PostgreSQL для состояния; append-only JSONL для событий; секрет-хранилище для API-ключей; никаких wallet keys в мониторинге; суммы хранить строками/Decimal, timestamps — UTC.
