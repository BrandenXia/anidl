from textual.reactive import Reactive, reactive

from anidl.config import Config
from anidl.utils.video import VIDEO_SUFFIXS

from .search_list import SearchList


class EpisodeList(SearchList):
    selected_anime: Reactive[str] = reactive("", recompose=True)

    invalid_message = "No anime selected. Please select an anime to view episodes."
    no_item_message = "No episodes found for the selected anime."

    def get_items(self) -> list[str]:
        if not self.selected_anime:
            return []

        anime_dir = Config().get_anime_dir() / self.selected_anime
        return (
            [
                i.name
                for i in anime_dir.iterdir()
                if i.is_file() and i.suffix in VIDEO_SUFFIXS
            ]
            if anime_dir.exists()
            else []
        )

    def invalid_check(self) -> bool:
        return not Config().get_anime_dir().exists() or not self.selected_anime

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.id = "episode-list"
        self.border_title = "Episodes"
