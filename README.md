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

## Slack API

https://slack.dev/bolt-python/tutorial/getting-started

Create an app and get "Bot User OAuth Token".

OAuth Scope: `groups:history`, `users:read`

## Hatena OAuth token

https://developer.hatena.ne.jp/ja/documents/auth/apis/oauth/

Create an OAuth app, get "Consumer Key" and "Consumer Secret".

```
poetry run python script/hatena_oauth.py
```
