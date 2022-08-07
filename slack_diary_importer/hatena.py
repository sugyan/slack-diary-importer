from dataclasses import dataclass
from typing import Generator, Optional

from lxml.builder import E, ElementMaker
from lxml.etree import fromstring, tostring
from requests_oauthlib import OAuth1Session


@dataclass
class Entry:
    id: Optional[int]
    title: str
    content: str
    updated: str
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
        self, hatena_id: str, hatena_blog_id: str
    ) -> Generator[Entry, None, None]:
        response = self.oauth.get(
            f"https://blog.hatena.ne.jp/{hatena_id}/{hatena_blog_id}/atom/entry"
        )
        et = fromstring(response.content)
        for entry in et.xpath(
            "//atom:entry",
            namespaces={"atom": "http://www.w3.org/2005/Atom"},
        ):
            category = entry.find("./category", et.nsmap)
            yield Entry(
                id=entry.find("./id", et.nsmap).text,
                title=entry.find("./title", et.nsmap).text,
                content=entry.find("./summary", et.nsmap).text,
                updated=entry.find("./updated", et.nsmap).text,
                category=category.get("term") if category is not None else None,
            )

    def post_entry(self, hatena_id: str, hatena_blog_id: str, entry: Entry) -> None:
        root = ElementMaker(nsmap={"app": "http://www.w3.org/2007/app"}).entry(
            E("title", entry.title),
            E("content", entry.content.replace("\n", "<br />"), type="text/plain"),
            E("updated", entry.updated),
            E("category", term=entry.category),
            xmlns="http://www.w3.org/2005/Atom",
        )
        data = tostring(root, xml_declaration=True, pretty_print=True, encoding="utf-8")
        response = self.oauth.post(
            f"https://blog.hatena.ne.jp/{hatena_id}/{hatena_blog_id}/atom/entry",
            data=data,
        )
        response.raise_for_status()
