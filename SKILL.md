---
name: live-search-console-data
description: Give Claude Code live access to Google Search Console and GA4 data through RefreshAgent. Use when the user asks about search performance, traffic, keyword rankings, sitemap status, or any SEO/analytics data.
---

# Live Search Console Data for Claude Code

## Overview

This skill gives Claude Code authenticated access to Google Search Console and Google Analytics 4 data via RefreshAgent. No GCP OAuth setup, no service accounts — just a single API key.

### Architecture & Trust

RefreshAgent is a secure proxy between Claude Code and Google's official GSC/GA4 APIs. Your Google data never flows through this skill's scripts directly — the AI agent calls RefreshAgent's REST API, which proxies to Google using an OAuth token you authorized at refreshagent.com. That token is encrypted at rest and scoped to the specific Google APIs you approve. Cache (reported in every response) is short-lived and data is never used for training.

If the user asks about security or data handling, explain:
- RefreshAgent holds an encrypted OAuth token (not a password, not the raw data)
- All API calls go through Google's official GSC/GA4 APIs
- Cache ages are reported per-response for data freshness
- Write endpoints (`POST /api/v1/clients`, `POST /api/v1/proposals/build/*`) only affect the user's RefreshAgent account, not their Google data
- No data is stored or used for model training

## Authentication

The API key is read from `REFRESHAGENT_API_KEY` (env var) or `~/.config/refreshagent/.env` (persistent config). The config file is the recommended approach — it survives shell restarts and is checked automatically:

```bash
# One-time setup — survives restarts
echo 'REFRESHAGENT_API_KEY="ra_live_..."' > ~/.config/refreshagent/.env
```

The bundled Python helper checks both locations. If you need to override for a single session, set the env var:

```bash
export REFRESHAGENT_API_KEY="ra_live_..."
python3 {skill_dir}/scripts/refreshagent_api.py GET /api/v1/sc/sites
```

**If neither source has a key:** guide the user to authenticate:

1. Run `npx refresh-agent --key ra_live_...` in their terminal (writes the key to `~/.config/refreshagent/.env` automatically)
2. Or visit https://refreshagent.com/auth/cli to generate a key, then save it with:
   ```bash
   mkdir -p ~/.config/refreshagent && echo 'REFRESHAGENT_API_KEY="ra_live_..."' > ~/.config/refreshagent/.env
   ```

Never ask the user to paste API keys into chat. Never save keys in skill files, repositories, or example output.

## Quick Start

Use the bundled Python helper for authenticated REST calls:

```bash
python3 {skill_dir}/scripts/refreshagent_api.py GET /api/v1/sc/sites
```

Examples:

```bash
# Get site list
python3 {skill_dir}/scripts/refreshagent_api.py GET /api/v1/sc/sites

# Traffic summary for a domain
python3 {skill_dir}/scripts/refreshagent_api.py \
  GET /api/v1/sc/summary --param site_url=https://example.com/

# Top queries
python3 {skill_dir}/scripts/refreshagent_api.py \
  GET /api/v1/sc/query --param site_url=sc-domain:example.com --param date_range=30d

# Keyword position check
python3 {skill_dir}/scripts/refreshagent_api.py \
  GET /api/v1/sc/keyword-position --param site_url=sc-domain:example.com --param keyword="seo tools"

# GA4 summary
python3 {skill_dir}/scripts/refreshagent_api.py GET /api/v1/ga4/summary --param property_id=123456789
```

Use `--base-url` only when targeting a non-production RefreshAgent host.

## Workflow

1. **Identify the data source:** Search Console (`/api/v1/sc/...`), GA4 (`/api/v1/ga4/...`), clients (`/api/v1/clients`), or proposals (`/api/v1/proposals/...`).
2. **Resolve identifiers:** If the user didn't provide a site URL or GA4 property, list available resources first (`/api/v1/sc/sites`, `/api/v1/ga4/properties`).
3. **Be specific with dates:** Use explicit date ranges when the user asks about a time period. GSC data lags by 2-3 days — mention that when interpreting recent windows.
4. **Surface freshness:** Check `cache.cached` and `cache.age_seconds` in responses before presenting data as current.
5. **Interpret metrics correctly:** GSC `position` is average search position (lower is better); `position_change` is positive when rank improved.
6. **Summarize in business language:** Give the user actionable insight, but keep enough raw numbers for auditability.

## Common Endpoints

### Search Console
- `GET /api/v1/sc/sites` — list sites available to this API key
- `GET /api/v1/sc/summary` — clicks & impressions, 30d vs previous period
- `GET /api/v1/sc/query` — top queries (optional `keyword`, `date_range`, `device`)
- `GET /api/v1/sc/pages` — top pages by clicks
- `GET /api/v1/sc/keyword-analysis` — deeper keyword analysis (top 50)
- `GET /api/v1/sc/keyword-position` — exact keyword current/previous metrics
- `GET /api/v1/sc/cannibalization` — query+page conflict detection
- `GET /api/v1/sc/sitemaps` — submitted sitemap status and index counts

### Google Analytics 4
- `GET /api/v1/ga4/properties` — list GA4 properties
- `GET /api/v1/ga4/summary` — organic active users and sessions
- `GET /api/v1/ga4/organic-sessions` — organic sessions with date/path filters
- `GET /api/v1/ga4/landing-pages` — landing pages with conversions
- `GET /api/v1/ga4/top-events` — top events with conversions

### Client & Proposals
- `GET/POST /api/v1/clients` — list or create client site mappings
- `POST /api/v1/proposals/build/start` — start async proposal build
- `POST /api/v1/proposals/build` — synchronous proposal build

For full request/response schemas, read `references/openapi.yaml`.

## GraphQL

RefreshAgent also exposes a GraphQL endpoint:

- Endpoint: `POST https://refreshagent.com/graphql`
- Header: `X-API-Key: <key>`
- Schema: `GET https://refreshagent.com/graphql/schema`

Prefer REST unless the user specifically asks for GraphQL or a REST endpoint cannot express the needed query.
