import logging
import os
from datetime import datetime
from typing import Any, Literal

from dotenv import load_dotenv
from slack_diary_importer.slack import SlackExporter
from slack_sdk.errors import SlackApiError

Message = dict[Literal["user", "ts", "blocks"], Any]


def display(message: Message, users: dict[str, str]) -> None:
    user = users.get(message["user"])
    if user is None:
        return
    ts = datetime.fromtimestamp(int(float(message["ts"])))
    text = ""
    for block in message.get("blocks", []):
        for element in block["elements"]:
            if element["type"] != "rich_text_section":
                raise ValueError(f"Unexpected element type: {element}")
            for e in element["elements"]:
                if e["type"] == "emoji":
                    emoji = "".join([chr(int(c, 16)) for c in e["unicode"].split("-")])
                    text += emoji
                else:
                    text += e["text"]
    if not text:
        return
    print(f"{ts}: {user}")
    print(text)
    print("----------------------------------------------------")


def main() -> None:
    load_dotenv()
    exporter = SlackExporter(os.getenv("SLACK_BOT_TOKEN", ""))
    try:
        users = exporter.users_dict()
        for message in exporter.histories(os.getenv("SLACK_CHANNEL", "")):
            display(message, users)
    except SlackApiError as e:
        logging.error(e)


if __name__ == "__main__":
    main()
