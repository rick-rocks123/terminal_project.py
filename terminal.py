from pathlib import Path
from datetime import datetime
import stat

def main() -> None:
    origin_folder: str = r'C:\Users\liebe\OneDrive\programming'
    current_folder: Path = Path(origin_folder)

    try:
        while True:
            try:
                command: str = input(f"{current_folder}> ")
                command_split: list[str] = command.split(' ')

                if command == "ls":
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
        print(f"{modes:<19} {date_info:<19} {file_stats.st_size:>10}  {file_or_dir.name}")


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
    mode: int = file.stat().st_file_attributes
    attributes: list[str] = ["-"] * 5

    if mode & stat.FILE_ATTRIBUTE_DIRECTORY:
        attributes[0] = "d"
    if mode & stat.FILE_ATTRIBUTE_ARCHIVE:
        attributes[1] = "a"
    if mode & stat.FILE_ATTRIBUTE_READONLY:
        attributes[2] = "r"
    if mode & stat.FILE_ATTRIBUTE_SYSTEM:
        attributes[3] = "s"
    if mode & stat.FILE_ATTRIBUTE_HIDDEN:
        attributes[4] = "h"

    return "".join(attributes)


if __name__ == "__main__":
    main()

