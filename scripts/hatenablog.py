import os

from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session


def main() -> None:
    client_key = os.getenv("HATENA_OAUTH_CONSUMER_KEY", "")
    client_secret = os.getenv("HATENA_OAUTH_CONSUMER_SECRET", "")
    oauth_token = os.getenv("HATENA_OAUTH_TOKEN", "")
    oauth_token_secret = os.getenv("HATENA_OAUTH_TOKEN_SECRET", "")
    hatena_id = os.getenv("HATENA_ID", "")
    hatena_blog_id = os.getenv("HATENA_BLOG_ID", "HATENA_BLOG_ID")

    hatena = OAuth1Session(
        client_key,
        client_secret=client_secret,
        resource_owner_key=oauth_token,
        resource_owner_secret=oauth_token_secret,
    )
    response = hatena.get(
        f"https://blog.hatena.ne.jp/{hatena_id}/{hatena_blog_id}/atom/entry"
    )
    print(response.text)


if __name__ == "__main__":
    load_dotenv()
    main()
