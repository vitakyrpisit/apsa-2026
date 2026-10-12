# Кошельки и мониторинг

| Сеть | Актив | Публичный адрес | Обозреватель |
|---|---|---|---|
| Ethereum Mainnet | ETH/ERC-20 | `0x829f877daAb94D766BB2b8511ad486C40f2C2BDA` | https://etherscan.io/address/0x829f877daAb94D766BB2b8511ad486C40f2C2BDA |
| Arbitrum One | ETH/токены | `0x829f877daAb94D766BB2b8511ad486C40f2C2BDA` | https://arbiscan.io/address/0x829f877daAb94D766BB2b8511ad486C40f2C2BDA |
| Solana | SOL/SPL | `EyTxSdVtku7QtbwgntLvUwyxMvraJyAxoPoZ8ALdG6qL` | https://solscan.io/account/EyTxSdVtku7QtbwgntLvUwyxMvraJyAxoPoZ8ALdG6qL |
| Tron | TRX/TRC-20 | `TVVhpdHEg1ZgvPjJNSe2P28bhUDE4m85ZX` | https://tronscan.org/#/address/TVVhpdHEg1ZgvPjJNSe2P28bhUDE4m85ZX |
| Bitcoin | BTC | `bc1qaedy7cmqujxlmkezlxlytkrecv0ufku970tk9c` | https://mempool.space/address/bc1qaedy7cmqujxlmkezlxlytkrecv0ufku970tk9c |

Число `578354`, ранее упомянутое рядом с Arbitrum, не имеет подтверждённого значения; не использовать как memo/tag.

Запуск:
`python scripts/monitor_wallets.py --config config/wallets.json --once`
`python scripts/monitor_wallets.py --config config/wallets.json --interval 60`

Монитор поддерживает обнаружение кандидатов через Blockscout (ETH/Arbitrum), mempool.space (BTC), Solana RPC (подписи, не точные суммы) и TronGrid (кандидаты; API key может понадобиться). Token transfers и точные суммы для SOL/TRON требуют дополнительного декодирования и проверки. API может менять схему/ограничивать запросы.

Для каждого перевода проверять chain/network, адрес назначения, актив/decimals, сумму, статус/финальность, собственные переводы и связь с задачей. QR/URI нужно декодировать обратно и проверить; для Arbitrum лучше отдельно указывать сеть и explorer, а не полагаться на универсальный URI. Страница локальная, пока не опубликована на доступном оператору хостинге.
