from typing import List

from textual.screen import Screen


class MetadataScreen(Screen):

    def __init__(self, selected_files: List[str]) -> None:
        super().__init__()
        self.selected_files = selected_files
