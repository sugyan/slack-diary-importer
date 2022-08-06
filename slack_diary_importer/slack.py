from typing import Any, Generator

from slack_bolt import App


class SlackExporter:
    def __init__(self, token: str) -> None:
        self.app = App(token=token)

    def users_dict(self) -> dict[str, str]:
        ret = dict()
        for user in self.app.client.users_list().data["members"]:
            if user["is_bot"] or not user["is_email_confirmed"]:
                continue
            ret[user["id"]] = user["profile"]["display_name"]
        return ret

    def histories(self, channel: str) -> Generator[Any, None, None]:
        for response in self.app.client.conversations_history(channel=channel):
            for message in response.data["messages"]:
                yield message
