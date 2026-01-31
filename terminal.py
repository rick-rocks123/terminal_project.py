
from pathlib import Path
from datetime import datetime
import stat

def main() -> None:
    origin_folder: str = r'C:\Users\liebe\OneDrive\programming'
    current_folder: Path = Path(origin_folder)

    try:
        while True:
            try:
                terminal_command: str = input(f"{current_folder}> ")
                command_split: list[str] = terminal_command.split(' ')

                if terminal_command == "ls":
                    command_ls(current_folder)
                elif command_split[0] in ("cd", "cd.."):
                    # Reuse variable without re-annotating type
                    current_folder = command_cd(current_folder, command_split)
            except IndexError:
                print("index error")

    except EOFError:
        print(current_folder)


def command_ls(current_folder: Path) -> None:
    headings: dict[str, str] = {"Mode": "<19", "LastWriteTime": ">19", "Length": ">12", "Name": ""}
    print(" ".join(f"{heading:{formatting}}" for heading, formatting in headings.items()))
    print(" ".join(f"{'-' * len(heading):{formatting}}" for heading, formatting in headings.items()))

    for file_or_dir in current_folder.iterdir():
        file_stats = file_or_dir.stat()
        date_info: str = datetime.fromtimestamp(file_stats.st_mtime).strftime('%m/%d/%Y, %I:%M%p')
        modes: str = determine_mode(file_or_dir)
        unicode = unicode_finder(file_or_dir)
        print(f"{modes:<19} {date_info:<19} {file_stats.st_size:>10}  {unicode}{file_or_dir.name}")


def command_cd(old_folder: Path, cd_check: list[str]) -> Path:
    for cd_file in cd_check:
        if cd_file in ("cd..", ".."):
            return old_folder.parent
    else:
        destination: Path = old_folder / cd_check[1]
        if destination.is_dir() and destination.exists():
            return destination
        else:
            print(f"cd : Cannot find path {cd_check[1]} because it does not exist.")
            return old_folder


def determine_mode(file: Path) -> str:
    file_mode: int = file.stat().st_file_attributes
    mode_attributes: list[str] = ["-"] * 15

    mode_and_position: dict[int, tuple[int, str]] = {
        stat.FILE_ATTRIBUTE_DIRECTORY: (0, "d"),  # directory
        stat.FILE_ATTRIBUTE_ARCHIVE: (1, "a"),  # archive
        stat.FILE_ATTRIBUTE_READONLY: (2, "r"),  # read-only
        stat.FILE_ATTRIBUTE_SYSTEM: (3, "t"),  # system file
        stat.FILE_ATTRIBUTE_HIDDEN: (4, "h"),  # hidden file
        stat.FILE_ATTRIBUTE_COMPRESSED: (5, "c"),  # compressed file
        stat.FILE_ATTRIBUTE_OFFLINE: (6, "o"),  # offline file
        stat.FILE_ATTRIBUTE_TEMPORARY: (7, "e"),  # temporary file
        stat.FILE_ATTRIBUTE_ENCRYPTED: (8, "n"),  # encrypted file
        stat.FILE_ATTRIBUTE_NOT_CONTENT_INDEXED: (9, "i"),  # not content indexed
        stat.FILE_ATTRIBUTE_REPARSE_POINT: (10, "l"),  # reparse point / symlink / junction
        stat.FILE_ATTRIBUTE_SPARSE_FILE: (11, "u"),  # sparse file
        stat.FILE_ATTRIBUTE_VIRTUAL: (12, "s"),  # virtual file
        stat.FILE_ATTRIBUTE_DEVICE: (13, "a"),  # device
        stat.FILE_ATTRIBUTE_NORMAL: (14, "r"),  # normal file
    }

    for key, (index, char) in mode_and_position.items():
        if file_mode & key:
            mode_attributes[index] = char

    return "".join(mode_attributes)

def unicode_finder(file: Path) -> str:

    file_icons: dict[str, str] = {
        # General / categories
        "directory": "\U0001F4C1",  # 📁
        "text": "\U0001F4C4",  # 📄
        "pdf": "\U0001F4D5",  # 📕
        "image": "\U0001F5BC",  # 🖼️
        "video": "\U0001F39E",  # 🎞️
        "audio": "\U0001F3B5",  # 🎵
        "exe": "\u2699",  # ⚙️
        "zip": "\U0001F5DC",  # 🗜️
        "shortcut": "\U0001F517",  # 🔗
        "hidden": "\U0001F47B",  # 👻
        "trash": "\U0001F5D1",  # 🗑️
        "generic": "\U0001F5CE",  # 🗎

        # Extensions
        ".txt": "\U0001F4C4",  # text
        ".md": "\U0001F4C4",
        ".json": "\U0001F4C4",
        ".csv": "\U0001F4C4",
        ".log": "\U0001F4DC",  # 📜 scroll
        ".pdf": "\U0001F4D5",  # pdf
        ".doc": "\U0001F4C4",
        ".docx": "\U0001F4C4",
        ".png": "\U0001F5BC",  # image
        ".jpg": "\U0001F5BC",
        ".jpeg": "\U0001F5BC",
        ".gif": "\U0001F5BC",
        ".ico": "\U0001F5BC",
        ".svg": "\U0001F5BC",
        ".mp4": "\U0001F39E",  # video
        ".mov": "\U0001F39E",
        ".avi": "\U0001F39E",
        ".mkv": "\U0001F39E",
        ".mp3": "\U0001F3B5",  # audio
        ".wav": "\U0001F3B5",
        ".ogg": "\U0001F3B5",
        ".flac": "\U0001F3B5",
        ".html": "\U0001F310",  # 🌐 web
        ".css": "\U0001F310",
        ".js": "\U0001F310",
        ".py": "\U0001F40D",  # 🐍 python
        ".sh": "\U0001F40D",
        ".bat": "\U0001F40D",
        ".xls": "\U0001F4CA",  # 📊 spreadsheets
        ".xlsx": "\U0001F4CA",
        ".ppt": "\U0001F4C8",  # 📈 presentations
        ".pptx": "\U0001F4C8",
        ".ttf": "\U0001F524",  # 🔤 fonts
        ".otf": "\U0001F524",
        ".db": "\U0001F5C4",  # 🗄️ databases
        ".sql": "\U0001F5C4",
        ".sqlite": "\U0001F5C4",
        ".ini": "\u2699",  # ⚙️ configs
        ".cfg": "\u2699",
        ".yaml": "\u2699",
        ".yml": "\u2699",
        ".zip": "\U0001F5DC",  # 🗜️ archives
        ".rar": "\U0001F5DC",
        ".7z": "\U0001F5DC",
        ".tar": "\U0001F5DC",
        ".gz": "\U0001F5DC",
    }


    # Directories
    if file.is_dir():
        return file_icons["directory"]
    # Files
    if file.is_file():
        return file_icons.get(file.suffix.lower(), file_icons["generic"])

    # Fallback for anything else
    return file_icons["generic"]


if __name__ == "__main__":
    main()
