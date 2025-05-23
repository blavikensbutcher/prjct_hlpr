from prettytable import PrettyTable
from datetime import datetime
import csv
import re
import colorama
from src.format import format_table


class Note:

    def __init__(self, author, title, note, tags=None, date=None):
        self.author = author
        self.title = title
        self.note = note
        self.tags = tags
        self.date = datetime.now().strftime("%d.%m.%Y,%H:%M") if date is None else date

    def change_note(self, field, new_data):
        fields_mapping = {
            "author": "author",
            "title": "title",
            "note": "note",
            "tags": "tags",
            "date": "date",
        }

        if field in fields_mapping:
            if field == "date":
                date_pattern = re.compile(
                    r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.\d{4},(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])$"
                )
                if not date_pattern.match(new_data):
                    raise ValueError("Invalid date format. Should be DD.MM.YYYY,HH:MM")
            setattr(self, fields_mapping[field], new_data)
        else:
            print(f"Invalid field: {field}")

    def __str__(self):
        tags_str = f"tags: {self.tags}; " if self.tags else ""
        return f"author: {self.author}; title: {self.title}; note: {self.note}; tags: {tags_str}; date: {self.date}."


class NoteManager:

    def __init__(self, csv_file=None):
        self.csv_file = csv_file
        self.notes = []
        if csv_file is not None:
            self.load_notes()

    def add_note(self, note):
        self.notes.append(note)
        print("Note added successfully.")

    def add_tag(self, note, tag):
        if note in self.notes:
            if note.tags == None:
                note.tags = tag
                print("Tag added successfully.")
            else:
                note.tags += ", " + tag
                print("Tag added successfully.")
        else:
            print("Note not found in the list.")

    def search_notes(self, info):
        result = []
        for note in self.notes:
            if (
                info in note.author
                or info in note.title
                or info in note.note
                or info in note.tags
                or info in note.date
            ):
                result.append(note)
        table = PrettyTable(["Author", "Title", "Note", "Tags", "Date"])
        table.align = "l"
        for data in result:
            table.add_row([data.author, data.title, data.note, data.tags, data.date])
        print(table)

    def remove_note(self, note):
        if note in self.notes:
            self.notes.remove(note)
            print("Note removed successfully.")
        else:
            print("Note not found in the list.")

    def save_notes(self):
        with open("notes_save.csv", "w", newline="") as fd:
            fields = ["author", "title", "note", "tags", "date"]
            writer = csv.DictWriter(fd, fieldnames=fields)
            writer.writeheader()

            for note in self.notes:
                writer.writerow(
                    {
                        "author": note.author,
                        "title": note.title,
                        "note": note.note,
                        "tags": note.tags,
                        "date": note.date,
                    }
                )

    def load_notes(self):
        with open("notes_save.csv", "r") as fd:
            reader = csv.DictReader(fd)
            for row in reader:
                note = Note(
                    row["author"],
                    row["title"],
                    row["note"],
                    row["tags"],
                    date=row["date"],
                )
                self.notes.append(note)

    def clear_notes(self):
        self.notes = []
        print("Notes cleared successfully.")

    def print_notes(self):
        colorama.init(autoreset=True)
        if not self.notes:
            print(colorama.Fore.RED + "No notes available." + colorama.Style.RESET_ALL)
            return
        headers = ["Автор", "Назва", "Нотатка", "Теги", "Дата створення"]
        colors = [
            colorama.Fore.YELLOW,  # Author
            colorama.Fore.CYAN,  # Title
            colorama.Fore.GREEN,  # Note
            colorama.Fore.MAGENTA,  # Tags
            colorama.Fore.BLUE,  # Date
        ]
        rows = [
            [note.author, note.title, note.note, ", ".join(note.tags), note.date]
            for note in self.notes
        ]
        print(format_table(rows, headers, colors))

    def search_notes_by_tags(self, search_tags: str):
        colorama.init(autoreset=True)
        if not search_tags:
            return colorama.Fore.RED + "Nothing to show" + colorama.Style.RESET_ALL
        search_tag_list = [x.strip() for x in search_tags.split(",")]
        result = set()
        for note in self.notes:
            if any(tag in note.tags for tag in search_tag_list):
                result.add(note)
        if not result:
            return colorama.Fore.RED + "Nothing to show" + colorama.Style.RESET_ALL

        headers = ["Author", "Title", "Note", "Tags", "Date"]
        colors = [
            colorama.Fore.YELLOW,
            colorama.Fore.CYAN,
            colorama.Fore.GREEN,
            colorama.Fore.MAGENTA,
            colorama.Fore.BLUE,
        ]

        rows = [
            [n.author, n.title, n.note, ", ".join(n.tags), str(n.date)] for n in result
        ]

        return format_table(rows, headers, colors)
