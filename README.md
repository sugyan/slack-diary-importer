# slack-diary-importer

## Setup

Using [`poetry`](https://python-poetry.org/)

```
poetry install
```

## Environment variables

```
cp .env.example .env
```

## Slack OAuth Token

https://slack.dev/bolt-python/tutorial/getting-started

Create an app and get "Bot User OAuth Token".

OAuth Scope: `groups:history`, `users:read`

## Hatena OAuth token

https://developer.hatena.ne.jp/ja/documents/auth/apis/oauth/

Create an OAuth app, get "Consumer Key" and "Consumer Secret".

```
poetry run python script/hatena_oauth.py
```

## Export & Import

```
poetry run python main.py --days 7
```

## Deply to Cloud Functions

```
poetry export --without-hashes -o requirements.txt
gcloud functions deploy $FUNCTION_NAME \
    --gen2 \
    --runtime python310 \
    --source . \
    --entry-point cloudfunctions_main \
    --trigger-topic $TOPIC
```
