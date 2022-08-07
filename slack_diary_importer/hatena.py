from dataclasses import dataclass
from datetime import date, datetime
from typing import Generator, Optional

from lxml.builder import E, ElementMaker
from lxml.etree import fromstring, tostring
from requests_oauthlib import OAuth1Session


@dataclass
class Entry:
    title: str
    content: str
    updated: str
    id: Optional[str] = None
    category: Optional[str] = None


class HatenaImporter:
    def __init__(
        self,
        client_key: str,
        client_secret: str,
        oauth_token: str,
        oauth_token_secret: str,
    ) -> None:
        self.oauth = OAuth1Session(
            client_key,
            client_secret=client_secret,
            resource_owner_key=oauth_token,
            resource_owner_secret=oauth_token_secret,
        )

    def get_entries(
        self, hatena_id: str, hatena_blog_id: str, min_date: Optional[date] = None
    ) -> Generator[Entry, None, None]:
        url = f"https://blog.hatena.ne.jp/{hatena_id}/{hatena_blog_id}/atom/entry"
        while True:
            response = self.oauth.get(url)
            et = fromstring(response.content)
            for entry in et.xpath(
                "//atom:entry",
                namespaces={"atom": "http://www.w3.org/2005/Atom"},
            ):
                category = entry.find("./category", et.nsmap)
                updated = entry.find("./updated", et.nsmap).text
                if (
                    min_date is not None
                    and datetime.fromisoformat(updated).date() < min_date
                ):
                    continue
                yield Entry(
                    id=entry.find("./id", et.nsmap).text,
                    title=entry.find("./title", et.nsmap).text,
                    content=entry.find("./summary", et.nsmap).text,
                    updated=updated,
                    category=category.get("term") if category is not None else None,
                )
            next = et.find("./link[@rel='next']", et.nsmap)
            if next is not None:
                url = next.get("href")
            else:
                break

    def publish_entry(
        self,
        hatena_id: str,
        hatena_blog_id: str,
        entry: Entry,
        entry_id: Optional[str] = None,
    ) -> None:
        root = ElementMaker(nsmap={"app": "http://www.w3.org/2007/app"}).entry(
            E("title", entry.title),
            E("content", entry.content.replace("\n", "<br />"), type="text/plain"),
            E("updated", entry.updated),
            E("category", term=entry.category),
            xmlns="http://www.w3.org/2005/Atom",
        )
        data = tostring(root, xml_declaration=True, pretty_print=True, encoding="utf-8")

        base_url = f"https://blog.hatena.ne.jp/{hatena_id}/{hatena_blog_id}/atom/entry"
        if entry_id is None:
            response = self.oauth.post(base_url, data=data)
            response.raise_for_status()
        else:
            response = self.oauth.put(f"{base_url}/{entry_id}", data=data)
            response.raise_for_status()
