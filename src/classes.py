from collections import UserDict
import re
from datetime import datetime
from utils import get_birthdays_per_week

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not self.validate_name(value):
            raise ValueError("Invalid name")
        super().__init__(value)

    def validate_name(self, value):
        return len(value) > 1

class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number")
        super().__init__(value)

    def validate_phone(self, value):
        return len(str(value)) == 10 and str(value).isdigit()
    
    def __repr__(self):
        return self.value

class Birthday:
    def __init__(self, birthday=None):
        self.birthday = None
        if birthday is not None:
            self.birthday = self.validate_birthday(birthday)

    def validate_birthday(self, birthday):
        if re.match(r'\d{2}.\d{2}.\d{4}', birthday):
            return datetime.strptime(birthday, '%d.%m.%Y')
        else:
            raise ValueError("Birthday must be in DD.MM.YYYY format")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != str(phone)]

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if str(phone) == str(old_phone):
                self.phones[i] = Phone(new_phone)
                break

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == str(phone):
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]

    def get_birthdays_per_week(self):
        return get_birthdays_per_week(dict(self.data))
