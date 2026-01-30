from pathlib import Path
from datetime import datetime
import stat


def main():

    origin_folder = r'C:\Users\liebe\OneDrive\programming'
    current_folder = Path(origin_folder)

    try:
        while True:
            try:
                command= input(f"{current_folder}> ")
                command_split  = command.split(' ')

                if command == "ls":
                    Command_ls(current_folder)
                elif command_split[0] == "cd" or command_split[0] == "cd..":
                    current_folder = Command_cd(current_folder, command_split)
            except IndexError:
                print("index error")


    except EOFError:
        print(current_folder)


def Command_ls(current_folder):

    headings = {"Mode": "<19", "LastWriteTime": ">19", "Length": ">12", "Name": ""}
    print(" ".join((f"{heading:{formatting}}" for heading, formatting in headings.items())))
    print(" ".join((f"{'-' * len(heading):{formatting}}" for heading, formatting in headings.items())))

    for file_or_dir in current_folder.iterdir():
        file_stats = Path.stat(file_or_dir)
        date_info = datetime.fromtimestamp(file_stats.st_mtime).strftime('%m/%d/%Y, %I:%M%p')
        modes = Determine_Mode(file_or_dir)

        print(f"{modes:<19} {date_info:<19} {file_stats.st_size:>10}  {file_or_dir.name}")



def Command_cd(old_folder, cd_check):
    for cd_file in cd_check:
        if cd_file in("cd..",".."):
            p = Path(old_folder)
            return p.parent

    else:
        destination = old_folder / cd_check[1]
        if destination.is_dir() and destination.exists():
            new_folder = old_folder / cd_check[1]
            return new_folder
        else:
            print(f"cd : Cannot find path {cd_check[1]} because it does not exist.")
            return old_folder







def Determine_Mode(file):

    mode = file.stat().st_file_attributes
    attributes = ["-"] * 5
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
