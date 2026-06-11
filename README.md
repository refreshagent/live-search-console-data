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

This skill connects Claude Code to the RefreshAgent API, which acts as an authenticated proxy for Google Search Console and Google Analytics 4. Your Google credentials are handled securely through refreshagent.com — no service account JSON files, no OAuth consent screen configuration.

## Requirements

- [Claude Code](https://claude.ai/download) (or any agent with skills.sh compatibility)
- A RefreshAgent account (free tier available)
- A Google account with Search Console or GA4 access

## Links

- [refreshagent.com](https://refreshagent.com)
- [skills.sh directory](https://skills.sh/refreshagent/live-search-console-data)
- [Agent Skills Format](https://agentskills.io)
