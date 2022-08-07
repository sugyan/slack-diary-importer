import os

from dotenv import load_dotenv
from slack_diary_importer.hatena import HatenaImporter


def main() -> None:
    client_key = os.getenv("HATENA_OAUTH_CONSUMER_KEY", "")
    client_secret = os.getenv("HATENA_OAUTH_CONSUMER_SECRET", "")
    oauth_token = os.getenv("HATENA_OAUTH_TOKEN", "")
    oauth_token_secret = os.getenv("HATENA_OAUTH_TOKEN_SECRET", "")
    hatena_id = os.getenv("HATENA_ID", "")
    hatena_blog_id = os.getenv("HATENA_BLOG_ID", "")

    importer = HatenaImporter(
        client_key, client_secret, oauth_token, oauth_token_secret
    )
    for entry in importer.get_entries(hatena_id, hatena_blog_id):
        print(f"{entry.id}: {entry.updated}")
        print(entry.content)
        print("----------------------------------------------------")


if __name__ == "__main__":
    load_dotenv()
    main()
