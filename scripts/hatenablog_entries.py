from slack_diary_importer.config import settings
from slack_diary_importer.hatena import HatenaImporter


def main() -> None:
    importer = HatenaImporter(
        settings.hatena_oauth_consumer_key,
        settings.hatena_oauth_consumer_secret,
        settings.hatena_oauth_token,
        settings.hatena_oauth_token_secret,
    )
    for entry in importer.get_entries(settings.hatena_id, settings.hatena_blog_id):
        entry_id = (entry.id if entry.id else "").split("-")[-1]
        print(f"{entry_id}: {entry.updated} {entry.category}")
        print(entry.content)
        print()


if __name__ == "__main__":
    main()
