import os
import sys
import time
from datetime import datetime
from random import random, choice
import argparse

from prettytable import PrettyTable
from prompt_toolkit import prompt
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.styles import Style as PromptStyle
from colorama import init, Fore, Style as ColoramaStyle

from src.classes import AddressBook, Record
from src.decorators.input_error import input_error
from src.notes import Note, NoteManager


GREEN = "\033[92m"
RESET = "\033[0m"
BOLD = "\033[1m"

matrix_chars = (
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()"
)

init()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def typewriter(text, delay=0.02):
    for char in text:
        sys.stdout.write(GREEN + char + RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def glitch_text(text, glitch_prob=0.1):
    result = ""
    for char in text:
        if random() < glitch_prob:

            effect = choice(
                [
                    lambda c: f"{Fore.LIGHTGREEN_EX}{c}{ColoramaStyle.RESET_ALL}",
                    lambda c: f"{Fore.GREEN}{c}{ColoramaStyle.RESET_ALL}",
                    lambda c: f"{Fore.WHITE}{c}{ColoramaStyle.RESET_ALL}",
                    lambda c: f"\033[38;2;0;{int(200*random())+55};0m{c}{ColoramaStyle.RESET_ALL}",
                    lambda c: "".join(
                        f"{Fore.GREEN}{choice(matrix_chars)}{ColoramaStyle.RESET_ALL}"
                        for _ in range(1, 3)
                    ),
                    lambda c: c.upper() if c.islower() else c.lower(),
                    lambda c: f"{c}{Fore.GREEN}{choice(matrix_chars)}{ColoramaStyle.RESET_ALL}",
                ]
            )
            result += effect(char)
        else:
            result += char
    return result


def typewriter_with_glitch(text, delay=0.02, glitch_prob=0.05):
    glitched_text = glitch_text(text, glitch_prob)
    for char in glitched_text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay * (0.5 + random() * 1.0))
    print()


def show_matrix_intro():
    clear_screen()
    typewriter_with_glitch("Booting up Matrix CLI...\n", 0.03, 0.07)
    time.sleep(0.5)

    progress_bar_length = 20
    for i in range(progress_bar_length + 1):
        bar = "[-" + "|" * i + " " * (progress_bar_length - i) + "-]"
        percentage = int((i / progress_bar_length) * 100)
        sys.stdout.write(
            f"\r{Fore.GREEN}Loading modules... {bar} {percentage}%{ColoramaStyle.RESET_ALL}"
        )
        sys.stdout.flush()
        time.sleep(0.1)
    print()

    time.sleep(0.5)
    typewriter_with_glitch("System initialization...", 0.05, 0.1)
    time.sleep(0.3)
    typewriter_with_glitch("Matrix connection established.", 0.05)
    time.sleep(0.5)
    typewriter_with_glitch(
        f"{Fore.WHITE}{ColoramaStyle.BRIGHT}Welcome, operator.{ColoramaStyle.RESET_ALL}\n",
        0.05,
    )
    time.sleep(0.5)


def matrix_rain(columns=100, lines=50, speed=0.05):
    try:

        streams = [
            {"pos": i, "speed": random() * 0.1 + 0.02, "length": int(random() * 5) + 3}
            for i in range(0, columns, 3)
        ]

        for _ in range(lines):
            line = [" "] * columns

            for stream in streams:

                pos = int(stream["pos"]) % columns
                line[pos] = (
                    f"{Fore.WHITE}{choice(matrix_chars)}{ColoramaStyle.RESET_ALL}"
                )

                for i in range(1, stream["length"]):
                    trail_pos = (pos - i) % columns
                    intensity = int(255 * (1 - i / stream["length"]))
                    line[trail_pos] = (
                        f"\033[38;2;0;{intensity};0m{choice(matrix_chars)}{ColoramaStyle.RESET_ALL}"
                    )

                stream["pos"] = (stream["pos"] + stream["speed"]) % columns

            print("".join(line))
            time.sleep(speed)
    except KeyboardInterrupt:
        pass


def floating_message(messages, width=80, height=15):
    positions = [
        (int(random() * width), int(random() * height)) for _ in range(len(messages))
    ]
    vectors = [(random() * 2 - 1, random() * 2 - 1) for _ in range(len(messages))]

    try:
        for frame in range(100):

            matrix = [
                [choice(matrix_chars) if random() < 0.05 else " " for _ in range(width)]
                for _ in range(height)
            ]

            for i, message in enumerate(messages):
                x, y = int(positions[i][0]), int(positions[i][1])
                if 0 <= y < height:
                    for j, char in enumerate(message):
                        if 0 <= x + j < width:
                            matrix[y][
                                x + j
                            ] = f"{Fore.WHITE}{ColoramaStyle.BRIGHT}{char}{ColoramaStyle.RESET_ALL}"

                positions[i] = (
                    (positions[i][0] + vectors[i][0]) % width,
                    (positions[i][1] + vectors[i][1]) % height,
                )

            clear_screen()
            for row in matrix:
                print(f"{Fore.GREEN}" + "".join(row) + f"{ColoramaStyle.RESET_ALL}")

            time.sleep(0.1)
    except KeyboardInterrupt:
        clear_screen()


@input_error
def handle_hello():
    show_matrix_intro()
    matrix_rain()
    typewriter("Enter a command: (add, edit, help, exit): ", 0.01)


@input_error
def handle_add(name, phone):
    if name not in ADDRESS_BOOK.data.keys():
        record = Record(name)
        try:
            record.add_phone(phone)
            ADDRESS_BOOK.add_record(record)

            table = PrettyTable(["name", "phones", "birthday", "email"])
            table.align = "l"

            answer = input("Would you add birthday or email? (Y/N) - ").lower()
            if answer == "y":
                data = input(
                    "Enter birthday and email separated by space (e.g., 01.01.2000 email@example.com): "
                ).split()
                data.sort()
                if len(data) == 2:
                    birthday, email = data
                    handle_set_email(name, email)
                    handle_set_birthday(name, birthday)
                    table.add_row([name, phone, birthday, email])
                    return table
                elif len(data) == 1:
                    if "@" in data[0]:
                        handle_set_email(name, data[0])
                        table.add_row([name, phone, None, data[0]])
                        return table
                    elif data[0].count(".") == 2:
                        handle_set_birthday(name, data[0])
                        table.add_row([name, phone, data[0], None])
                        return table
                print("Invalid input.")
            elif answer != "n":
                print("Invalid input.")
            table.add_row([name, phone, None, None])
            return table
        except ValueError:
            return "Invalid phone"
    else:
        record = ADDRESS_BOOK.find(name)
        try:
            record.add_phone(phone)
            return f"Phone number {phone} added for contact {name}"
        except ValueError:
            return "Invalid phone"


@input_error
def handle_change(change, name, new, newphone=None):
    record = ADDRESS_BOOK.find(name)
    if record is not None:
        if change == "email":
            try:
                record.change_email(new)
                return f"Email for contact {name} is set as {new}"
            except ValueError:
                return "Invalid email"
        elif change == "birthday":
            try:
                record.change_birthday(new)
                return f"Birthday for contact {name} is set to {new}"
            except ValueError:
                return "Please enter the date in DD.MM.YYYY format."
        elif change == "phone":
            try:
                record.edit_phone(new, newphone)
                return f"Phone number for contact {change} changed to {newphone}"
            except ValueError:
                return "Invalid phone, please enter the phone in XXXXXXXXXX format."
        else:
            return "Unknown command. Please try again."
    else:
        raise KeyError


@input_error
def handle_set_email(name, email):
    record = ADDRESS_BOOK.find(name)
    if record is not None:
        try:
            record.set_email(email)
            return f"Email for contact {name} is set as {email}"
        except IndexError:
            return "Email is already set for this contact, use the 'change' command"
    else:
        raise KeyError


@input_error
def handle_set_birthday(name, day):
    record = ADDRESS_BOOK.find(name)
    if record is not None:
        try:
            record.set_birthday(day)
            return f"Birthday for contact {name} is set to {day}"
        except ValueError:
            return "Please enter the date in DD.MM.YYYY format."
        except IndexError:
            return "Birthday is already set for this contact, use the 'change' command"
    else:
        raise KeyError


@input_error
def days_to_birthday(name):
    record = ADDRESS_BOOK.find(name)
    if record is not None:
        return record.days_to_birthday()
    else:
        raise KeyError


@input_error
def handle_delete(name):
    record = ADDRESS_BOOK.find(name)
    if record is not None:
        ADDRESS_BOOK.delete(name)
        return f"{name} deleted"
    else:
        raise KeyError


@input_error
def handle_remove(name, remove):
    record = ADDRESS_BOOK.find(name)
    if record is not None:
        if remove == "email":
            record.remove_email()
            return f"{remove} for {name} deleted"
        elif remove == "birthday":
            record.remove_birthday()
            return f"{remove} for {name} deleted"
        else:
            try:
                record.remove_phone(remove)
                return f"{remove} for {name} deleted"
            except ValueError:
                return f"Phone number {remove} for contact {name} not found."
            except IndexError:
                return "You cannot delete a single phone number, add another one or use the command 'change'"
    else:
        raise KeyError


@input_error
def handle_phone(name):
    record = ADDRESS_BOOK.find(name)
    if record is not None:
        return record
    raise KeyError


@input_error
def handle_show_all():
    if not ADDRESS_BOOK.data:
        return "The address book is empty."

    table = PrettyTable(["Name", "Phones", "Birthday", "Email"])
    table.align = "l"

    total_contacts = len(ADDRESS_BOOK.data)

    for idx, (name, record) in enumerate(ADDRESS_BOOK.data.items()):
        phones = "\n".join(map(str, record.phones))
        birthday = record.birthday if record.birthday else ""
        email = record.email if record.email else ""
        table.add_row(
            [
                name,
                phones,
                birthday if birthday != "" else None,
                email if email != "" else None,
            ]
        )
        # Add separator line if it's not the last contact
        if idx < total_contacts - 1:
            table.add_row(["-" * 20, "-" * 20, "-" * 20, "-" * 20])

    return str(table)


@input_error
def handle_search(query):
    return ADDRESS_BOOK.search(query)


@input_error
def handle_open():
    global ADDRESS_BOOK
    global NOTES_MANAGER
    csv_file = "new_book.csv"
    csv_file_notes = "notes_save.csv"
    try:
        ADDRESS_BOOK = AddressBook(csv_file)
        NOTES_MANAGER = NoteManager(csv_file_notes)
        return f"Address book opened from {csv_file}"
    except FileNotFoundError:
        ADDRESS_BOOK = AddressBook(None)
        NOTES_MANAGER = NoteManager(None)
        return "Starting with an empty address book."


@input_error
def handle_save(path_dir):
    global ADDRESS_BOOK
    global NOTES_MANAGER
    os.chdir(path_dir)
    csv_file = "new_book.csv"
    csv_file_notes = "notes_save.csv"
    if ADDRESS_BOOK.csv_file is None and NOTES_MANAGER.csv_file is None:
        ADDRESS_BOOK.csv_file = csv_file
        ADDRESS_BOOK.save_to_disk()
        NOTES_MANAGER.csv_file = csv_file_notes
        NOTES_MANAGER.save_notes()
    elif ADDRESS_BOOK.csv_file is None:
        ADDRESS_BOOK.csv_file = csv_file
        ADDRESS_BOOK.save_to_disk()
        return f"Address book saved to to {ADDRESS_BOOK.csv_file}"
    elif NOTES_MANAGER.csv_file is None:
        NOTES_MANAGER.csv_file = csv_file_notes
        NOTES_MANAGER.save_notes()
    else:
        ADDRESS_BOOK.save_to_disk()
        NOTES_MANAGER.save_notes()
        return f"Address book and NOTES_MANAGER saved to {ADDRESS_BOOK.csv_file} , {NOTES_MANAGER.csv_file}"


@input_error
def handle_add_note(author, title):
    for note in NOTES_MANAGER.notes:
        if note.title == title:
            print("It's note is exist")
            return
    text = input("write your text - ")
    note = Note(author, title, text)
    NOTES_MANAGER.add_note(note)
    tag = input("Would you add tags? (Y/N) - ").lower()
    if tag == "y":
        data = input("Enter your data separated by space: ").lower()
        a = data.split()
        tags = ", ".join(a)
        all_notes = NOTES_MANAGER.notes
        match = None
        for el in all_notes:
            note_title = el.title
            if title == note_title:
                match = el
                break
        if match:
            NOTES_MANAGER.add_tag(match, tags)
    elif tag != "n":
        print("Invalid input.")


@input_error
def handle_delete_note(title):
    all_notes = NOTES_MANAGER.notes
    match = None
    for el in all_notes:
        note_title = el.title
        if title == note_title:
            match = el
            break
    if match:
        NOTES_MANAGER.remove_note(match)
    else:
        print("It's note is exist")


@input_error
def handle_add_tags(*args):
    title = args[0]
    tags = ", ".join(args[1:])
    all_notes = NOTES_MANAGER.notes
    match = None
    for el in all_notes:
        note_title = el.title
        if title == note_title:
            match = el
            break
    else:
        print("Сould not find note")
    if match:
        NOTES_MANAGER.add_tag(match, tags)


@input_error
def handle_show_birthday_list(date):
    records = ADDRESS_BOOK.data
    date_now = datetime.now().date()

    try:
        target_date = datetime.strptime(date, "%d.%m.%Y").date()
    except ValueError:
        return "Date not correct, please input in the format DD.MM.YYYY"

    users_within_range = ""

    for key, value in records.items():
        try:
            user_birthday = (
                datetime.strptime(str(value.birthday), "%d.%m.%Y")
                .replace(year=date_now.year)
                .date()
            )

            if date_now <= user_birthday <= target_date:
                users_within_range += (
                    f"{value.name}'s birthday is on {value.birthday}" + "\n"
                )
        except ValueError:
            continue

    return users_within_range


@input_error
def handle_search_note_by_tags(*args):
    tags = ",".join(args)
    return NOTES_MANAGER.search_notes_by_tags(tags)


@input_error
def handle_clear_notes():
    NOTES_MANAGER.clear_notes()


@input_error
def show_all_notes():
    NOTES_MANAGER.print_notes()


def show_help():
    help_message = """
        hello: Вивести вітальне повідомлення.
        save: Зберегти адресну книгу.
        add [іʼмя] [телефон]: Додати новий контакт до адресної книги або до старого контакту додати номер.
        set email [іʼмя] [email]: Додати email для контакту.
        set birthday [іʼмя] [дата]: Встановити день народження для контакту.
        days to birthday [іʼмя]: Розрахувати кількість днів до наступного дня народження для контакту.
        show birthday list [дата] : Показати список днів народженя до певної дати
        change phone [іʼмя] [старий телефон] [новий телефон]: Змінити обраний телефон.
        change email/birthday [іʼмя] [нові дані]: Змінити дані існуючого контакту.
        remove [іʼмя] [телефон/birthday/email]: видалити інформацію для контакту.
        info [іʼмя]: Вивести інформацію про контакт.
        delete [іʼмя]: Видалити контакт з адресної книги.
        show all: Відобразити всі контакти в адресній книзі.
        search [запит]: Пошук в адресній книзі за символами.
        create note [автор] [назва] : Додає нотатку
        append note tags [назва], [тег_1 тег_2...] : Додає тег до нотатків
        showing all notes : Показати усі нотатки
        deletion note [назва] : Видаляє нотатку
        clear notes : Видаляє усі нотатки
        searching note by tags [тег_1 тег_2...] : Шукати по тегам
        """

    commands = [line.strip() for line in help_message.split("\n") if line.strip()]
    table = PrettyTable(["Доступні команди", "Опис"])
    table.align["Доступні команди"] = "l"
    table.align["Опис"] = "l"

    for command in commands:
        command_parts = command.split(":", 1)
        if len(command_parts) == 2:
            table.add_row([command_parts[0].strip(), command_parts[1].strip()])

    return table


COMMANDS = {
    "help": show_help,
    "hello": handle_hello,
    "save": handle_save,
    "add": handle_add,
    "set email": handle_set_email,
    "set birthday": handle_set_birthday,
    "days to birthday": days_to_birthday,
    "change": handle_change,
    "remove": handle_remove,
    "info": handle_phone,
    "delete": handle_delete,
    "show all": handle_show_all,
    "searching note by tags": handle_search_note_by_tags,
    "search": handle_search,
    "append note tags": handle_add_tags,
    "create note": handle_add_note,
    "show all notes": show_all_notes,
    "deletion note": handle_delete_note,
    "clear notes": handle_clear_notes,
    "show birthday list": handle_show_birthday_list,
}

command_list = [
    "help",
    "hello",
    "save",
    "add",
    "change birthday",
    "change email",
    "change phone",
    "remove",
    "info",
    "show all",
    "set birthday",
    "set email",
    "days to birthday",
    "delete",
    "searching note by tags",
    "search",
    "append note tags",
    "create note",
    "show all notes",
    "deletion note",
    "clear notes",
    "show birthday list",
    "exit",
    "close"
]


custom_style = PromptStyle.from_dict(
    {
        "prompt": "bg:black #39FF14",
        "completion-menu.completion": "bg:black #FFFFFF",
        "completion-menu.completion.current": "bg:black #39FF14",
        "completion-menu.border": "bg:#008000 #ffffff",
    }
)

completer = FuzzyWordCompleter(command_list)


def get_user_input():
    return prompt("Enter a command: ", completer=completer, style=custom_style).lower()


def show_access_granted():
    clear_screen()

    typewriter_with_glitch("MATRIX: SECURITY SYSTEM", 0.03)
    typewriter_with_glitch("........................", 0.05)
    time.sleep(0.5)

    typewriter_with_glitch("Scanning in progress...", 0.03)
    time.sleep(1)

    print(f"{Fore.CYAN}Biometric authentication: {ColoramaStyle.RESET_ALL}", end="")
    for _ in range(20):
        sys.stdout.write(choice(["▓", "▒", "░"]))
        sys.stdout.flush()
        time.sleep(0.1)
    print(f" {Fore.GREEN}[SUCCESS]{ColoramaStyle.RESET_ALL}")
    time.sleep(0.3)

    print(f"{Fore.CYAN}Access decryption: {ColoramaStyle.RESET_ALL}", end="")
    for i in range(10):
        progress = i * 10
        sys.stdout.write(
            f"\r{Fore.CYAN}Access decryption: {Fore.GREEN}{progress}%{ColoramaStyle.RESET_ALL}"
        )
        sys.stdout.flush()
        time.sleep(0.2)
    print(f"\r{Fore.CYAN}Access decryption: {Fore.GREEN}100%{ColoramaStyle.RESET_ALL}")

    time.sleep(0.5)
    print("\n" + "=" * 40)
    print(f"{Fore.GREEN}{ColoramaStyle.BRIGHT}ACCESS GRANTED{ColoramaStyle.RESET_ALL}")
    print(
        f"{Fore.GREEN}Welcome to project {Fore.WHITE}PRJCT_HLPR{ColoramaStyle.RESET_ALL}"
    )
    print("=" * 40)
    time.sleep(1.5)


def run_with_matrix_style():
    try:
        global ADDRESS_BOOK
        global NOTES_MANAGER
        handle_open()
        current_directory = os.getcwd()
        show_access_granted()
        handle_hello()

        while True:
            user_input = get_user_input()
            if user_input in ["good bye", "close", "exit"]:
                print(handle_save(current_directory))
                print(Fore.GREEN + "Good bye" + Fore.RESET)
                break
            for command in COMMANDS.keys():
                if user_input.startswith(command):
                    args = user_input[len(command) :].split()
                    res = COMMANDS[command](*args)
                    print(res) if res is not None else ...
                    break
            else:
                print("Unknown command. Please try again.")
    except KeyboardInterrupt:
        print(Fore.GREEN + "Good bye\n" + Fore.RESET)
        exit()


def run_with_simple_style():
    try:
        global ADDRESS_BOOK
        global NOTES_MANAGER
        handle_open()
        current_directory = os.getcwd()

        simple_style = PromptStyle.from_dict(
            {
                "prompt": "bg:darkgreen #ffffff",
                "completion-menu.completion": "bg:#708090 #ffffff",
                "completion-menu.completion.current": "bg:#ffffff #2E8B57",
                "completion-menu.border": "bg:#008000 #ffffff",
            }
        )

        simple_completer = FuzzyWordCompleter(command_list)

        def simple_get_user_input():
            return prompt(
                "Enter a command: ", completer=simple_completer, style=simple_style
            ).lower()

        print("How can I help you?")

        while True:
            user_input = simple_get_user_input()
            if user_input in ["good bye", "close", "exit"]:
                print(handle_save(current_directory))
                print("Good bye!")
                break
            for command in COMMANDS.keys():
                if user_input.startswith(command):
                    args = user_input[len(command) :].split()
                    res = COMMANDS[command](*args)
                    print(res) if res is not None else ...
                    break
            else:
                print("Unknown command. Please try again.")
    except KeyboardInterrupt:
        print("Good bye!")
        exit()


def main():
    parser = argparse.ArgumentParser(description="Assistant Application")
    parser.add_argument("--matrix", action="store_true", help="Run with Matrix style")

    if len(sys.argv) > 1:
        args = parser.parse_args()
        if args.matrix:
            run_with_matrix_style()
        else:
            run_with_simple_style()
    else:

        if "matrix" in sys.argv[0].lower():
            run_with_matrix_style()
        else:
            run_with_simple_style()


if __name__ == "__main__":
    main()
