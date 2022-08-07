import base64
import logging
from argparse import ArgumentParser
from datetime import date, datetime, timedelta
from typing import Any, Optional

from slack_diary_importer.config import settings
from slack_diary_importer.hatena import Entry, HatenaImporter
from slack_diary_importer.slack import SlackExporter


def cloudfunctions_main(event: Any, context: Any) -> None:
    print(
        "This Function was triggered by messageId {} published at {} to {}".format(
            context.event_id, context.timestamp, context.resource["name"]
        )
    )
    data = base64.b64decode(event["data"]).decode("utf-8")
    min_date = datetime.today().date() - timedelta(days=int(data))
    logging.basicConfig(level=logging.INFO)
    logging.info(f"Start export & import data since {min_date} to today")
    # run(min_date)
    run(None)


def run(min_date: Optional[date]) -> None:
    exporter = SlackExporter(settings.slack_bot_token)
    importer = HatenaImporter(
        settings.hatena_oauth_consumer_key,
        settings.hatena_oauth_consumer_secret,
        settings.hatena_oauth_token,
        settings.hatena_oauth_token_secret,
    )
    published = dict()
    try:
        for entry in importer.get_entries(
            settings.hatena_id, settings.hatena_blog_id, min_date
        ):
            updated = datetime.fromisoformat(entry.updated)
            if entry.id:
                published[int(updated.timestamp())] = entry.id.split("-")[-1]
        logging.info(f"{len(published)} entries found")

        for message in exporter.histories(settings.slack_channel, min_date):
            logging.info(message)
            entry_id = published.get(int(message.timestamp.timestamp()))
            if entry_id:
                logging.info(f"PUT {entry_id}")
            else:
                logging.info("POST new entry")
            importer.publish_entry(
                settings.hatena_id,
                settings.hatena_blog_id,
                Entry(
                    title=message.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    content=message.text,
                    updated=message.timestamp.isoformat(),
                    category=message.user_name,
                ),
                entry_id,
            )
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--days", type=int)
    args = parser.parse_args()

    min_date = None
    if args.days:
        min_date = datetime.today().date() - timedelta(days=args.days)

    logging.basicConfig(level=logging.INFO)
    run(min_date)
