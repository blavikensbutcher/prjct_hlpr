import csv
import re
from collections import UserDict
from datetime import date, datetime

from prettytable import PrettyTable


class Field:
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if self.is_valid_format(value):
            self.__value = value
        else:
            raise ValueError

    def __str__(self):
        return str(self.value)


class Name(Field):
    def is_valid_format(self, value):
        return True


class Phone(Field):
    def is_valid_format(self, value):
        if len(value) == 10 and value.isdigit():
            return True
        else:
            return False


class Birthday(Field):
    def is_valid_format(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            return False


class Email(Field):
    def is_valid_format(self, value):
        pattern = r"^[a-zA-Z]+[\w.-]+[@][a-zA-Z]+[.][a-zA-Z][a-zA-Z]+$"
        return re.match(pattern, value) is not None


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def set_birthday(self, birthday):
        if self.birthday is not None:
            raise IndexError
        else:
            self.birthday = Birthday(birthday)

    def set_email(self, email):
        if self.email is not None:
            raise IndexError
        else:
            self.email = Email(email)

    def remove_phone(self, phone):
        if len(self.phones) > 1:
            for ph in self.phones:
                if ph.value == phone:
                    self.phones.remove(ph)
                    break
                elif ph not in self.phones:
                    raise ValueError
        else:
            raise IndexError

    def remove_birthday(self):
        self.birthday = None

    def change_birthday(self, bir):
        self.birthday = Birthday(bir)

    def remove_email(self):
        self.email = None

    def change_email(self, email):
        self.email = Email(email)

    def edit_phone(self, old_phone, new_phone):
        if any(p.value == old_phone for p in self.phones):
            self.add_phone(new_phone)
            self.remove_phone(old_phone)
        else:
            raise ValueError

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def days_to_birthday(self):
        if self.birthday is not None:
            today = date.today()
            birth_date = datetime.strptime(f"{self.birthday}", "%d.%m.%Y").date()
            new_b = birth_date.replace(year=today.year)
            if today > new_b:
                new_b = new_b.replace(year=today.year + 1)
            delta = new_b - today
            return delta
        else:
            return None

    def __str__(self):
        phones_str = "; ".join(str(phone) for phone in self.phones)
        return f"Contact name: {self.name}, phones: {phones_str}, birthday: {self.birthday}, email: {self.email}"



class AddressBook(UserDict):
    def __init__(self, csv_file=None):
        super().__init__()
        self.csv_file = csv_file
        self.records = []
        if csv_file is not None:
            self.read_from_file()

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def search(self, query):
        results = []
        for name, record in self.data.items():
            if query.lower() in name.lower():
                results.append(record)
                continue
            # Пошук за номерами телефону
            for phone in record.phones:
                if query.lower() in phone.value.lower():
                    results.append(record)
                    break
                # Пошук за днем народження
                if record.birthday is not None:
                    birthday_str = str(record.birthday)
                    if query.lower() in birthday_str.lower():
                        results.append(record)
        table = PrettyTable(["name", "phones", "birthday", "email"])
        table.align = "l"
        for data in results:
            phones = ""
            for phone in data.phones:
                if phone == data.phones[-1]:
                    phones += str(phone)
                else:
                    phones += str(phone) + "\n"
            table.add_row([data.name, phones, data.birthday, data.email])
        return table

    def delete(self, name):
        if name in self.data:
            self.data.pop(name)

    def iterator(self, page_size):
        records = list(self.data.values())
        total_records = len(records)
        start = 0
        page_number = 1

        while start < total_records:
            page = records[start : start + page_size]
            yield f"Page {page_number}:\n" + "\n".join(str(record) for record in page)
            start += page_size
            page_number += 1

    def save_to_disk(self):
        with open(self.csv_file, "w", newline="") as file:
            field = ["Name", "Phones", "Birthday", "Email"]
            writer = csv.DictWriter(file, fieldnames=field)
            writer.writeheader()
            # Записуємо дані
            for name, record in self.data.items():
                phones_str = ";".join(str(phone) for phone in record.phones)
                writer.writerow(
                    {
                        "Name": name,
                        "Phones": phones_str,
                        "Birthday": str(record.birthday) if record.birthday else "None",
                        "Email": str(record.email) if record.email else "None",
                    }
                )

    def read_from_file(self):
        with open(self.csv_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                record = Record(row["Name"])
                phones = row["Phones"].split(";")
                for phone in phones:
                    record.add_phone(phone)
                if row["Birthday"] != "None":
                    record.set_birthday(row["Birthday"])
                if row["Email"] != "None":
                    record.set_email(row["Email"])
                self.add_record(record)
