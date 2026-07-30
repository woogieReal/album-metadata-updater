import re
import os
from mutagen.id3 import ID3, ID3NoHeaderError, TALB, TPE1, TDRC, TIT2, TRCK


class MetadataService:

    def read_tags(self, filepath: str) -> dict:
        try:
            tags = ID3(filepath)
        except ID3NoHeaderError:
            return {}

        def text(tag):
            return str(tags[tag]) if tag in tags else None

        return {
            "album": text("TALB"),
            "artist": text("TPE1"),
            "year": text("TDRC"),
            "title": text("TIT2"),
            "track_number": text("TRCK"),
        }

    def clean_track_title(self, filename: str) -> str:
        name = os.path.splitext(filename)[0]
        name = re.sub(r'^\s*(\d+|\[\d+\])[\s._\-)]*', '', name)
        return name.strip()

    def assign_track_numbers(self, filepaths: list) -> list:
        sorted_paths = sorted(filepaths, key=lambda p: os.path.basename(p))
        return [(path, idx + 1) for idx, path in enumerate(sorted_paths)]

    def write_tags(self, filepath: str, tags: dict) -> bool:
        try:
            try:
                id3 = ID3(filepath)
            except ID3NoHeaderError:
                id3 = ID3()

            mapping = {
                "album": (TALB, lambda v: TALB(encoding=3, text=v)),
                "artist": (TPE1, lambda v: TPE1(encoding=3, text=v)),
                "year": (TDRC, lambda v: TDRC(encoding=3, text=v)),
                "title": (TIT2, lambda v: TIT2(encoding=3, text=v)),
                "track_number": (TRCK, lambda v: TRCK(encoding=3, text=str(v))),
            }

            for key, (frame_cls, make_frame) in mapping.items():
                if key in tags and tags[key] is not None:
                    id3.add(make_frame(tags[key]))

            id3.save(filepath)
            return True
        except Exception as e:
            print(f"[MetadataService] write_tags 실패 ({filepath}): {e}")
            return False
