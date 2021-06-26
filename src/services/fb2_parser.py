from pathlib import Path
from typing import Optional, Union

from defusedxml import ElementTree


class FB2Parser:
    """Parse book.fb2 and extract book name, author full name and book published year"""

    def __init__(
        self, filename: Optional[Union[str, Path]] = None, text: Optional[str] = None
    ):
        if text is None:
            self.root = ElementTree.parse(filename).getroot()
        else:
            self.root = ElementTree.fromstring(text)
        self.cleanup()

    @property
    def name(self) -> str:
        """Parse book and extract book name"""
        return self.root.find("./description/title-info/book-title").text

    @property
    def author_full_name(self) -> Optional[str]:
        """Parse book and extract author name"""
        element_first_name = self.root.find(
            "./description/title-info/author/first-name"
        )
        element_last_name = self.root.find("./description/title-info/author/last-name")
        if element_first_name is None or element_last_name is None:
            return None
        return f"{element_first_name.text} {element_last_name.text}"

    @property
    def published_year(self) -> Optional[int]:
        """Parse book and extract published year"""
        element_year = self.root.find("./description/publish-info/year")
        return int(element_year.text) if element_year is not None else None

    @property
    def as_dict(self):
        return {
            "name": self.name,
            "author": self.author_full_name,
            "year": self.published_year,
        }

    def cleanup(self) -> None:
        """Reformat tag: {URL}description -> description"""
        for element in self.root.iter():
            element.tag = element.tag.partition("}")[-1]
