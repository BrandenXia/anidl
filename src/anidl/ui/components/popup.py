from textual.containers import Vertical


class PopupMenu(Vertical):
    def close(self) -> None:
        self.styles.display = "none"
