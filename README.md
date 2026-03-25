# dp-document-appointments

Checks availability of appointment slots at [berlin.pasport.org.ua](https://berlin.pasport.org.ua/solutions/e-queue) and sends a Telegram notification when slots open up. Runs every 5 minutes via GitHub Actions.

## Setup

Copy `.env` and fill in your values:

```bash
cp .env .env.local  # or just edit .env directly
```

`.env` fields:

| Variable | Description |
|---|---|
| `TELEGRAM_TOKEN` | Bot token from [@BotFather](https://t.me/BotFather) |
| `TELEGRAM_CHAT_ID` | Chat ID to send notifications to |

## Running locally (mirrors CI)

Uses Docker + Xvfb to replicate the GitHub Actions environment exactly.

**Build the image:**

```bash
docker build -t dp-check .
```

**Run:**

```bash
docker run --rm --env-file .env -v $(pwd):/app dp-check
```

The `-v $(pwd):/app` mount means code changes take effect without rebuilding the image.
