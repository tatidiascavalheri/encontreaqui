# EncontreAqui Marketplace Monorepo

Plataforma marketplace Cliente ↔ Profissional com módulo de anúncios para fornecedores.

## 1) Stack escolhida e justificativa
- **Mobile:** React Native (Expo) com `expo-location` e `expo-notifications` (rápido ciclo, code-sharing JS).
- **Web Admin/Advertiser:** Next.js (App Router) para dashboards SSR + API routes futuras.
- **Backend:** FastAPI (Python) por produtividade e tipagem com Pydantic.
- **Banco:** PostgreSQL + PostGIS para geobusca (`ST_DWithin`, `ST_Distance`).
- **Cache/Fila:** Redis + RQ (jobs assíncronos para notificações, webhooks e relatórios).
- **Realtime:** WebSocket nativo do FastAPI para chat por Job. Trade-off: menor lock-in, porém exige scaling com pub/sub em produção.
- **Pagamentos:** Stripe Connect (escrow-like via `PaymentIntent` capturado e payout postergado). Abstraído via `PaymentProvider`.
- **Infra:** Docker + docker-compose; imagens em S3 compatível via interface abstrata `StorageProvider`.

## 2) Arquitetura (modular monolith)
- `services/api`: módulos de domínio (auth, search, jobs, chat, payments, ratings, ads, admin)
- `apps/mobile`: app cliente/profissional
- `apps/web-admin`: painel administrativo
- `apps/web-advertiser`: portal de fornecedor
- `packages/shared`: contratos compartilhados (OpenAPI e tipos)

### Fluxos-chave
1. Cliente busca profissionais por categoria + proximidade.
2. Cliente cria Job (`requested`) e profissional aceita (`accepted`).
3. Pagamento fica em retenção; após `completed` e sem disputa, payout.
4. Chat por Job via WebSocket.
5. Avaliação mútua (1 por parte por Job concluído).
6. Ads servidos por placement com targeting e tracking.

## 3) ER (resumo textual)
- `users` (RBAC) 1:1 com `clients` / `professionals` / `advertisers`
- `professionals` N:N `categories` via `professional_categories`
- `jobs` liga cliente-profissional e contém estados; histórico em `job_status_history`
- `chat_threads` 1:1 com job, `chat_messages` N:1 thread
- `ratings` vinculadas a `job_id`, com unicidade (job, rater, target)
- `payments` e eventos em `payment_events`; `refunds` e `payouts`
- `campaigns` pertencem a `advertisers`; `creatives`, `targeting_rules`, `ad_events`

## 4) Execução local
```bash
make dev
```

### Comandos úteis
```bash
make migrate
make seed
make test
```

## 5) Variáveis de ambiente (API)
Copie `services/api/.env.example` para `.env`.

## 6) Como testar geobusca e ads
1. Rode seed (`make seed`).
2. Chame:
```bash
curl "http://localhost:8000/search/professionals?category_id=1&lat=-23.56&lng=-46.65&radius_km=20"
curl "http://localhost:8000/ads/serve?placement=HOME&lat=-23.56&lng=-46.65&role=client"
```

## 7) Política de cancelamento/disputa
- Cancelamento antes de `in_progress`: tentativa de estorno automático.
- `in_dispute`: payout pausado.
- `refunded`: encerra financeiro do Job.

## 8) Prova de aceitação (seed)
Seed inclui 5 profissionais em SP com coordenadas para validação de ordenação por distância.
