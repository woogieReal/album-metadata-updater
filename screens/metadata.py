from pathlib import Path
from typing import List, Optional

import xattr as xattr_lib
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Checkbox, Input, Label


FIELD_CBS = ["cb-album", "cb-artist", "cb-year", "cb-title", "cb-track-number"]


class MetadataScreen(Screen):

    CSS = """
    #top-bar {
        height: 3;
        align: right middle;
    }
    #content {
        height: 1fr;
        padding: 1 2;
    }
    .field-row {
        height: 3;
        align: left middle;
    }
    .field-row Checkbox {
        width: 16;
    }
    .field-row Input {
        width: 1fr;
    }
    .field-info {
        width: 1fr;
        height: 3;
        content-align: left middle;
        color: gray;
    }
    #bottom-bar {
        height: 3;
        align: center middle;
    }
    """

    def __init__(self, selected_files: List[str]) -> None:
        super().__init__()
        self.selected_files = selected_files
        self._syncing = False

    def compose(self) -> ComposeResult:
        yield Container(
            Button("닫기", id="close-btn"),
            id="top-bar",
        )
        yield ScrollableContainer(
            Horizontal(
                Checkbox("전체 항목 선택/해제", value=True, id="select-all"),
            ),
            Horizontal(
                Checkbox("앨범명", value=True, id="cb-album"),
                Input(placeholder="앨범명", id="input-album"),
                classes="field-row",
            ),
            Horizontal(
                Checkbox("아티스트", value=True, id="cb-artist"),
                Input(placeholder="아티스트", id="input-artist"),
                classes="field-row",
            ),
            Horizontal(
                Checkbox("연도", value=True, id="cb-year"),
                Input(placeholder="연도", id="input-year"),
                classes="field-row",
            ),
            Horizontal(
                Checkbox("트랙명", value=True, id="cb-title"),
                Label("파일명 기반 자동 정제 적용", classes="field-info"),
                classes="field-row",
            ),
            Horizontal(
                Checkbox("트랙번호", value=True, id="cb-track-number"),
                Label("파일명 오름차순 기준 순번 자동 부여", classes="field-info"),
                classes="field-row",
            ),
            id="content",
        )
        yield Container(
            Button("메타데이터 수정하기", id="save-btn", variant="primary"),
            id="bottom-bar",
        )

    def on_mount(self) -> None:
        self._load_folder_metadata()

    def _load_folder_metadata(self) -> None:
        folder = self.app.selected_folder
        if not folder:
            return

        try:
            attrs = xattr_lib.xattr(folder)
            album = self._read_xattr(attrs, "user.album")
            artist = self._read_xattr(attrs, "user.artist")
            year = self._read_xattr(attrs, "user.year")
        except Exception:
            album = artist = year = None

        if not album:
            album = Path(folder).name

        self.query_one("#input-album", Input).value = album or ""
        self.query_one("#input-artist", Input).value = artist or ""
        self.query_one("#input-year", Input).value = year or ""

    def _read_xattr(self, attrs, key: str) -> Optional[str]:
        try:
            return attrs[key].decode("utf-8").strip() or None
        except (KeyError, Exception):
            return None

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        if self._syncing or event.checkbox.id != "select-all":
            return
        self._syncing = True
        for cb_id in FIELD_CBS:
            self.query_one(f"#{cb_id}", Checkbox).value = event.value
        self._syncing = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close-btn":
            self.app.pop_screen()
        elif event.button.id == "save-btn":
            pass  # Phase 6에서 구현
