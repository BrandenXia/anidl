from textual import on

from anidl.config import Config
from anidl.ui.ctx import AssignCtx

from .episode_list import EpisodeList
from .search_list import SearchList, ItemList


class AnimeList(SearchList):
    invalid_message = (
        "Invalid anime directory. Please set it in setting or press 'r' to refresh."
    )
    no_item_message = "No downloaded anime found."

    def get_items(self) -> list[str]:
        anime_dir = Config().get_anime_dir()
        return (
            [i.name for i in anime_dir.iterdir() if i.is_dir()]
            if anime_dir.exists()
            else []
        )

    def invalid_check(self) -> bool:
        return not Config().get_anime_dir().exists()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.border_title = "Downloaded Animes"

    @on(ItemList.OptionSelected)
    def on_item_selected(self, event: ItemList.OptionSelected) -> None:
        self.post_message(
            AssignCtx.Assign(
                "#episode-list", EpisodeList, "selected_anime", event.option.prompt
            )
        )
