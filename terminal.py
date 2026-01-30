
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
    mode_attributes: list[str] = ["-"] * 5

    if file_mode & stat.FILE_ATTRIBUTE_DIRECTORY:
        mode_attributes[0] = "d"
    if file_mode & stat.FILE_ATTRIBUTE_ARCHIVE:
        mode_attributes[1] = "a"
    if file_mode & stat.FILE_ATTRIBUTE_READONLY:
        mode_attributes[2] = "r"
    if file_mode & stat.FILE_ATTRIBUTE_SYSTEM:
        mode_attributes[3] = "s"
    if file_mode & stat.FILE_ATTRIBUTE_HIDDEN:
        mode_attributes[4] = "h"

    return "".join(mode_attributes)

def unicode_finder(file):
    file_icons = {
        "directory": "\U0001F4C1",
        "text": "\U0001F4C4",
        "pdf": "\U0001F4D5",
        "image": "\U0001F5BC",
        "video": "\U0001F39E",
        "audio": "\U0001F3B5",
        "exe": "\u2699",
        "zip": "\U0001F5DC",
        "shortcut": "\U0001F517",
        "hidden": "\U0001F47B",
        "trash": "\U0001F5D1",
        "generic": "\U0001F5CE"
    }
    suffix_icons = {
        ".png": file_icons["image"],
        ".jpg": file_icons["image"],
        ".mp4": file_icons["video"],
        ".mov": file_icons["video"],
        ".txt": file_icons["text"],
        ".json": file_icons["text"],
        ".csv": file_icons["text"],
        ".pdf": file_icons["pdf"],
        ".zip": file_icons["zip"]
    }

    if file.is_dir():
        return file_icons["directory"]

    elif file.is_file():
        return suffix_icons.get(file.suffix.lower(), file_icons["generic"])


if __name__ == "__main__":
    main()
