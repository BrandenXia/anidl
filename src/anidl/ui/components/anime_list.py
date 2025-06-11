from textual import on

from anidl.config import Config
from anidl.ui.ctx import OperationCtx

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
        def assign_selected(list_widget: EpisodeList) -> None:
            assert isinstance(event.option.prompt, str), (
                "Expected prompt to be a string, got: "
                f"{type(event.option.prompt).__name__}"
            )
            list_widget.selected_anime = event.option.prompt

        self.post_message(
            OperationCtx.Operation("#episode-list", EpisodeList, assign_selected),
        )
