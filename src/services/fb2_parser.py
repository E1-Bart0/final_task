import logging
from pathlib import Path
from typing import Optional, Union

from defusedxml import ElementTree


class FB2Parser:
    """Parse book.fb2 and extract book name, author full name and book published year"""

    def __init__(
        self, filename: Optional[Union[str, Path]] = None, text: Optional[str] = None
    ):

        if text is None:
            logging.debug(f"Parsing file: {filename}")
            self.root = ElementTree.parse(filename).getroot()
        else:
            logging.debug("Parsing text")
            self.root = ElementTree.fromstring(text)
        self.cleanup()

    @property
    def name(self) -> str:
        """Parse book and extract book name"""
        return self.root.find("./description/title-info/book-title").text

    @property
    def author_first_name(self) -> Optional[str]:
        """Parse book and extract author name"""
        element_name = self.root.find("./description/title-info/author/first-name")
        return element_name.text if element_name is not None else None

    @property
    def author_last_name(self) -> Optional[str]:
        """Parse book and extract author name"""
        element_last_name = self.root.find("./description/title-info/author/last-name")
        return element_last_name.text if element_last_name is not None else None

    @property
    def published_year(self) -> Optional[int]:
        """Parse book and extract published year"""
        element_year = self.root.find("./description/publish-info/year")
        return int(element_year.text) if element_year is not None else None

    @property
    def as_dict(self):
        return {
            "name": self.name,
            "author_first_name": self.author_first_name,
            "author_last_name": self.author_last_name,
            "year": self.published_year,
        }

    def cleanup(self) -> None:
        """Reformat tag: {URL}description -> description"""
        for element in self.root.iter():
            element.tag = element.tag.partition("}")[-1]
