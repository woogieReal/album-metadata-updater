from typing import Optional
from textual.app import App
from textual.binding import Binding
from screens.explorer import ExplorerScreen


class AlbumTagApp(App):
    TITLE = "앨범 메타데이터 업데이터"

    BINDINGS = [
        Binding("ctrl+r", "restart_app", "앱 재시작"),
    ]

    selected_folder: Optional[str] = None
    selected_files: list = []
    restart_requested: bool = False

    def on_mount(self) -> None:
        self.push_screen(ExplorerScreen())

    def action_restart_app(self) -> None:
        self.restart_requested = True
        self.exit()
