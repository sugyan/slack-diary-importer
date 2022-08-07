from requests_oauthlib import OAuth1Session
from slack_diary_importer.config import settings


def main() -> None:
    oauth = OAuth1Session(
        settings.hatena_oauth_consumer_key,
        client_secret=settings.hatena_oauth_consumer_secret,
        callback_uri="oob",
    )
    request_token_response = oauth.fetch_request_token(
        "https://www.hatena.com/oauth/initiate",
        data={"scope": "read_private,write_private"},
    )
    authorization_url = oauth.authorization_url(
        "https://www.hatena.ne.jp/oauth/authorize"
    )
    print(f"Please go here and authorize, {authorization_url}")
    verifier = input("Please input the verifier: ")
    oauth_tokens = OAuth1Session(
        settings.hatena_oauth_consumer_key,
        client_secret=settings.hatena_oauth_consumer_secret,
        resource_owner_key=request_token_response.get("oauth_token"),
        resource_owner_secret=request_token_response.get("oauth_token_secret"),
        verifier=verifier,
    ).fetch_access_token("https://www.hatena.com/oauth/token")
    for key in ["oauth_token", "oauth_token_secret"]:
        value = oauth_tokens.get(key)
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
