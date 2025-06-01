from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class Provider(ABC):
    type AnimeID = Any
    type EpID = Any

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the provider."""

    @abstractmethod
    def search(self, query: str, page: int = 1) -> dict[str, AnimeID]:
        """
        Search for an anime by query.
        Should return a dict of str and some kind of AnimeID, where it can used to
        fetch more information about a specific anime.
        """

    @abstractmethod
    def get_eps(self, anime_id: AnimeID) -> dict[str, EpID]:
        """
        Get episodes for an anime by its ID.
        Should return a dict of str and some kind of EpID, where it can be used to
        select and download a specific episode.
        """

    @abstractmethod
    def download_ep(self, ep_id: EpID, path: Path):
        """
        Download an episode by its ID to the specified path.
        Should raise an exception if the download fails.
        """


class QDMProvider(Provider):
    pass
