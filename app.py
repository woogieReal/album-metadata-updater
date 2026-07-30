from typing import Optional
from textual.app import App
from screens.explorer import ExplorerScreen


class AlbumTagApp(App):
    TITLE = "앨범 메타데이터 업데이터"

    selected_folder: Optional[str] = None
    selected_files: list = []

    def on_mount(self) -> None:
        self.push_screen(ExplorerScreen())
