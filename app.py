from textual.app import App
from screens.explorer import ExplorerScreen


class AlbumTagApp(App):
    def on_mount(self) -> None:
        self.push_screen(ExplorerScreen())
