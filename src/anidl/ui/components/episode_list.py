from typing import Collection

from textual.reactive import Reactive, reactive
from textual.widgets.option_list import Option

from anidl.config import Config
from anidl.utils.video import VIDEO_SUFFIXS, check_video_integrity

from .search_list import SearchList


def to_id(text: str) -> str:
    return (
        text.lower()
        .replace(" ", "-")
        .replace("'", "")
        .replace('"', "")
        .replace(".", "_")
    )


class EpisodeList(SearchList):
    selected_anime: Reactive[str] = reactive("", recompose=True)

    invalid_message = "No anime selected. Please select an anime to view episodes."
    no_item_message = "No episodes found for the selected anime."

    def get_items(self) -> Collection[str | Option]:
        if not self.selected_anime:
            return []

        eps_dir = Config().get_anime_dir() / self.selected_anime
        eps = (
            [
                i.name
                for i in eps_dir.iterdir()
                if i.is_file() and i.suffix in VIDEO_SUFFIXS
            ]
            if eps_dir.exists()
            else []
        )

        for anime in eps:
            self.run_worker(self.check_ep(anime))

        return tuple(map(lambda ep: Option(ep, id=to_id(ep)), eps))

    def invalid_check(self) -> bool:
        return not Config().get_anime_dir().exists() or not self.selected_anime

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.id = "episode-list"
        self.border_title = "Episodes"

    async def check_ep(self, ep: str):
        valid = await check_video_integrity(
            Config().get_anime_dir() / self.selected_anime / ep
        )
        list_view = self.list_view
        option = list_view.get_option_index(to_id(ep))
        if valid:
            list_view.replace_option_prompt_at_index(option, f"{ep} ✅")
        else:
            list_view.replace_option_prompt_at_index(option, f"{ep} (broken)")
