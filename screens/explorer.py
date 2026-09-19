import asyncio
from pathlib import Path
from typing import List

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widgets import Button, Checkbox, DirectoryTree, Footer, Header

from screens.metadata import MetadataScreen


class ExplorerScreen(Screen):

    BINDINGS = [
        Binding("r", "refresh", "새로고침"),
    ]

    CSS = """
    #tree-container {
        height: 1fr;
    }
    #file-list-container {
        display: none;
        height: 1fr;
    }
    #bottom-bar {
        height: 3;
        align: center middle;
    }
    #bottom-bar Button {
        margin: 0 1;
    }
    #back-btn {
        display: none;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self._current_dir: str = str(Path.cwd())
        self._mp3_files: List[Path] = []
        self._in_file_mode: bool = False
        self._syncing: bool = False

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(DirectoryTree(Path.home()), id="tree-container")
        yield ScrollableContainer(id="file-list-container")
        yield Horizontal(
            Button("새로고침", id="refresh-btn"),
            Button("폴더 다시 선택", id="back-btn"),
            Button("현재 폴더 사용하기", id="action-btn", variant="primary"),
            Button("앱 재시작", id="restart-btn"),
            id="bottom-bar",
        )
        yield Footer()

    def on_mount(self) -> None:
        self.set_timer(0.3, self._expand_to_cwd)

    async def _expand_to_cwd(self) -> None:
        cwd = Path(self._current_dir)
        home = Path.home()
        try:
            parts = list(cwd.relative_to(home).parts)
        except ValueError:
            return

        tree = self.query_one(DirectoryTree)
        node = tree.root
        node.expand()

        for part in parts:
            # wait up to 3s for the children of the current node to load
            for _ in range(30):
                await asyncio.sleep(0.1)
                names = [
                    Path(c.data.path).name
                    for c in node.children
                    if c.data and hasattr(c.data, "path")
                ]
                if part in names:
                    break

            target = next(
                (
                    c
                    for c in node.children
                    if c.data and hasattr(c.data, "path") and Path(c.data.path).name == part
                ),
                None,
            )
            if target is None:
                return

            node = target
            node.expand()

        tree.select_node(node)
        tree.scroll_to_node(node, animate=False)

    def on_directory_tree_directory_selected(
        self, event: DirectoryTree.DirectorySelected
    ) -> None:
        self._current_dir = str(event.path)

    async def action_refresh(self) -> None:
        await self._refresh()

    async def _refresh(self) -> None:
        if not self._in_file_mode:
            tree = self.query_one(DirectoryTree)
            await tree.reload()
            self.notify("파일 트리를 새로고침했습니다.")
        else:
            await self._show_file_list()
            self.notify("파일 목록을 새로고침했습니다.")

    def _back_to_tree(self) -> None:
        self.query_one("#tree-container").display = True
        self.query_one("#file-list-container").display = False
        self.query_one("#action-btn", Button).label = "현재 폴더 사용하기"
        self.query_one("#back-btn", Button).display = False
        self._in_file_mode = False

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "refresh-btn":
            await self._refresh()
            return
        if event.button.id == "back-btn":
            self._back_to_tree()
            return
        if event.button.id == "restart-btn":
            self.app.action_restart_app()
            return
        if event.button.id != "action-btn":
            return
        if not self._in_file_mode:
            await self._show_file_list()
        else:
            self._go_to_metadata()

    async def _show_file_list(self) -> None:
        folder = Path(self._current_dir)
        self._mp3_files = sorted(
            [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() == ".mp3"],
            key=lambda f: f.name,
        )

        if not self._mp3_files:
            self.notify("선택한 폴더에 MP3 파일이 없습니다.", severity="warning")
            if self._in_file_mode:
                self._back_to_tree()
            return

        file_list = self.query_one("#file-list-container", ScrollableContainer)
        await file_list.remove_children()
        checkboxes = [Checkbox("전체 선택/해제", value=True, id="select-all")]
        for i, mp3 in enumerate(self._mp3_files):
            checkboxes.append(Checkbox(mp3.name, value=True, id=f"file-{i}"))
        await file_list.mount_all(checkboxes)

        self.query_one("#tree-container").display = False
        file_list.display = True
        self.query_one("#action-btn", Button).label = "설정할 메타데이터 고르기"
        self.query_one("#back-btn", Button).display = True
        self._in_file_mode = True

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        if self._syncing or event.checkbox.id != "select-all":
            return
        self._syncing = True
        for i in range(len(self._mp3_files)):
            self.query_one(f"#file-{i}", Checkbox).value = event.value
        self._syncing = False

    def _go_to_metadata(self) -> None:
        selected = [
            str(self._mp3_files[i])
            for i in range(len(self._mp3_files))
            if self.query_one(f"#file-{i}", Checkbox).value
        ]

        if not selected:
            self.notify("파일을 하나 이상 선택해 주세요.", severity="warning")
            return

        self._back_to_tree()

        self.app.selected_folder = self._current_dir
        self.app.selected_files = selected
        self.app.push_screen(MetadataScreen(selected))
