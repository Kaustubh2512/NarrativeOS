# NarrativeOS Data Pipeline — Local Test Runner

Run actors locally without deploying to Apify cloud:

```bash
# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r data/requirements.txt
playwright install chromium

# Run Reddit scraper (locally, not via Apify)
python -c "
import asyncio
from data.actors.reddit_scraper.src.main import main
asyncio.run(main())
"

# Run News scraper
python -c "
import asyncio
from data.actors.news_scraper.src.main import main
asyncio.run(main())
"

# Run SEC scraper
python -c "
import asyncio
from data.actors.sec_scraper.src.main import main
asyncio.run(main())
"
```

## Deploy to Apify Cloud

```bash
# Install Apify CLI
pnpm add -g apify-cli

# Login
apify login

# Deploy Reddit Actor
cd data/actors/reddit-scraper
apify push

# Deploy News Actor
cd ../news-scraper
apify push

# Deploy SEC Actor
cd ../sec-scraper
apify push
```

## Set up schedules via Apify Console

Once deployed, go to Apify Console → Tasks → Create Task for each Actor, then add a Schedule:

| Actor | Schedule | Cron |
|-------|----------|------|
| Reddit | Every 30 min | `*/30 * * * *` |
| News | Every hour | `0 * * * *` |
| SEC | Once daily at 6 AM | `0 6 * * *` |

## Webhook Setup

In Apify Console, for each Actor Task, add a webhook:
- Event: `RUN.SUCCEEDED`
- URL: `{NARRATIVEOS_EVENT_STREAM_URL}` (Member 3's Superplane ingress endpoint)

## Testing the pipeline

```bash
source .venv/bin/activate
python -m data.pipelines.test_pipeline
```
