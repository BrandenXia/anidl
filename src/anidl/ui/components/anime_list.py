from anidl.config import Config

from .search_list import SearchList


def get_animes() -> list[str]:
    anime_dir = Config().get_anime_dir()
    return (
        [i.name for i in anime_dir.iterdir() if i.is_dir()]
        if anime_dir.exists()
        else []
    )


class AnimeList(SearchList):
    get_items = staticmethod(get_animes)
    invalid_message = (
        "Invalid anime directory. Please set it in setting or press 'r' to refresh."
    )
    no_item_message = "No downloaded anime found."

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.border_title = "Downloaded Animes"

    def invalid_check(self) -> bool:
        return not Config().get_anime_dir().exists()
