from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Generator, Optional

from slack_bolt import App


@dataclass
class Message:
    user_name: str
    timestamp: datetime
    text: str


class SlackExporter:
    def __init__(self, token: str) -> None:
        self.app = App(token=token)
        self.users = dict()
        # Get members and cache their display names
        for user in self.app.client.users_list().data["members"]:
            if user["is_bot"] or not user["is_email_confirmed"]:
                continue
            self.users[user["id"]] = user["profile"]["display_name"]

    def histories(
        self, channel: str, min_date: Optional[date] = None
    ) -> Generator[Any, None, None]:
        for response in self.app.client.conversations_history(channel=channel):
            for message in response.data["messages"]:
                # Check timestamp
                timestamp = datetime.fromtimestamp(int(float(message["ts"])))
                if min_date is not None and timestamp.date() < min_date:
                    return
                # Check user
                user = self.users.get(message["user"])
                if user is None:
                    continue
                # Construct message content including emoji
                text = ""
                for block in message.get("blocks", []):
                    for element in block["elements"]:
                        if element["type"] != "rich_text_section":
                            raise ValueError(f"Unexpected element type: {element}")
                        for e in element["elements"]:
                            if e["type"] == "emoji":
                                emoji = "".join(
                                    [chr(int(c, 16)) for c in e["unicode"].split("-")]
                                )
                                text += emoji
                            else:
                                text += e["text"]
                if not text:
                    continue
                yield Message(user, timestamp, text)
