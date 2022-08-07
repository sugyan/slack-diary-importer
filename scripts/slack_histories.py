import logging

from slack_diary_importer.config import settings
from slack_diary_importer.slack import SlackExporter
from slack_sdk.errors import SlackApiError


def main() -> None:
    exporter = SlackExporter(settings.slack_bot_token)
    try:
        for message in exporter.histories(settings.slack_channel):
            print(f"{message.timestamp}: {message.user_name}")
            print(message.text)
            print()
    except SlackApiError as e:
        logging.error(e)


if __name__ == "__main__":
    main()
