# Live Google Search Console Data for Claude Code

<p align="center">
  <a href="https://skills.sh/refreshagent/live-search-console-data"><img src="https://skills.sh/b/refreshagent/live-search-console-data" alt="Install via skills.sh"></a>
</p>

Skip the GCP OAuth setup. Give Claude Code live access to your Google Search Console and GA4 data in 60 seconds.

## Installation

```bash
npx skills add refreshagent/live-search-console-data
```

## How to Authenticate

After installing, ask Claude about your search traffic. The skill will detect that you need to authenticate and provide a secure link to connect your Google account at refreshagent.com. One click, and Claude has live data.

## What You Can Ask

- "Which pages lost the most traffic last month?"
- "Show me my top keywords by impressions"
- "Is my sitemap indexing correctly?"
- "What's my organic traffic trend for the last 30 days?"
- "Do any of my pages compete for the same keyword?"
- "Which landing pages have the best conversion rate?"

## How It Works

This skill connects Claude Code to the RefreshAgent API, which acts as a secure proxy for Google Search Console and Google Analytics 4.

### Data Flow & Trust Model

1. **You authenticate with Google** via refreshagent.com's OAuth flow — same Google permissions as granting access to any third-party tool (e.g., Semrush, Ahrefs).
2. **RefreshAgent stores an encrypted OAuth token** — not your Google password, not your data. The token is scoped to the GSC/GA4 APIs you authorize.
3. **The AI agent calls RefreshAgent's API** using your API key (`ra_live_...`). RefreshAgent proxies the request to Google's official APIs using your stored token.
4. **Data is cached briefly** (seconds to minutes) to avoid redundant API calls. Cache age is reported in every response.
5. **No data leaves RefreshAgent for training.** Responses are ephemeral — they exist only in the agent's context window.

This is the same architecture used by every SEO tool that offers Google data integration — we handle the OAuth boilerplate so you don't have to configure a GCP project, set up a service account, or manage token refreshes.

### Why a Proxy Instead of Direct API Calls?

Google's Search Console and GA4 APIs require:
- A Google Cloud Project with OAuth 2.0 configured
- A registered redirect URI per client
- Handling token refresh flows
- Managing service account JSON files for server-to-server access

None of these work inside an AI agent's ephemeral execution environment. RefreshAgent handles this infrastructure so the agent can focus on answering your questions.

### Write Endpoints

This skill is primarily read-only, but does expose two write endpoints for creating client site mappings and proposals (`POST /api/v1/clients`, `POST /api/v1/proposals/build/*`). These require your explicit API key and only affect your own RefreshAgent account — they do not modify your Google Search Console or GA4 data.

## Requirements

- [Claude Code](https://claude.ai/download) (or any agent with skills.sh compatibility)
- A RefreshAgent account (free tier available)
- A Google account with Search Console or GA4 access

## Links

- [refreshagent.com](https://refreshagent.com)
- [skills.sh directory](https://skills.sh/refreshagent/live-search-console-data)
- [Agent Skills Format](https://agentskills.io)
- [Google Search Console API](https://developers.google.com/webmaster-tools)
- [Google Analytics Data API](https://developers.google.com/analytics/devguides/reporting/data/v1)
