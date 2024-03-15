import re
import json
from collections import UserDict
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

class Email(Field):
    def __init__(self, value):
        if not self.validate_email(value):
            raise ValueError("Invalid email format.")
        super().__init__(value)

    def validate_email(self, email):
        # Регулярний вираз для перевірки формату e-mail
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email)

class Birthday:
    def __init__(self, birthday=None):
        self.birthday = None
        if birthday is not None:
            self.birthday = self.validate_birthday(birthday)

    def validate_birthday(self, birthday):
        if re.match(r"\d{2}.\d{2}.\d{4}", birthday):
            return datetime.strptime(birthday, "%d.%m.%Y")
        else:
            raise ValueError("Birthday must be in DD.MM.YYYY format")

class Address:
    def __init__(self, address):
        self.address = address
           
    def __str__(self):
        return str(self.address)
    
class Record:
    def __init__(self, name, address=None, email=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.notes = NoteBook()
        self.address = address
        self.email = None
        if email:
            self.add_email(email)

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
    
    
    def add_address(self, address):
        address_obj = Address(address)
        self.address =address_obj

    def edit_address(self, new_address):
        self.address = Address(new_address)
        return "Address updated."

    def show_address(self):
        return str(self.address) if self.address else "Address not found."
           
    def add_email(self, email):
        email_obj = Email(email)
        self.email = email_obj

    
    def edit_email(self, new_email):
        if new_email:
            self.email = Email(new_email)
            return "Email updated."
        else:
            return "Invalid email."
    
    def show_email(self):
        return str(self.email.value) if self.email else "Email not found."

    def find_email(self, email):
        for e in self.emails:
            if e.value == email:
                return e.value
        return None

    def add_note(self, content):
        return self.notes.create_note(content)

    def edit_note_by_id(self, note_id, new_content):
        return self.notes.edit_note(note_id, new_content)

    def delete_note_by_id(self, note_id):
        return self.notes.delete_note(note_id)

    def find_note_by_content(self, search_content):
        return self.notes.search(search_content)

    def add_tag_to_note_by_id(self, note_id, tag):
        return self.notes.add_tag_to_note(note_id, tag)

    def remove_tag_from_note_by_id(self, note_id, tag):
        return self.notes.remove_tag_from_note(note_id, tag)

    def find_notes_by_tags(self, tags):
        return self.notes.find_note_by_tags(tags)

    #def __str__(self):
        #return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"
    def __str__(self):
        phones_str = '; '.join([str(phone.value) for phone in self.phones])
        email_str = ', '.join([str(email.value) for email in self.emails])
        birthday_str = f", Birthday: {self.birthday.value}" if hasattr(self, 'birthday') and self.birthday and self.birthday.value else ""
        address_str = str(self.address) if self.address else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}, email: {email_str}{birthday_str}, address: {address_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]

    def get_birthdays_per_week(self):
        return get_birthdays_per_week(dict(self.data))
    
    def find_by_email(self, email):
        for record in self.data.values():
            if record.email and record.email.value == email:
                return record
        return None

    def find_by_phone(self, phone_number):
        for record in self.data.values():
            for phone in record.phones:
                if str(phone.value) == phone_number:
                    return record
        return None
    

# Notes
class Note:
    note_id = 0

    def __init__(self, content):
        self.content = " ".join(content) if type(content) == list else content
        self.id = Note.note_id
        self.tags = []
        Note.note_id += 1

    def edit(self, new_content):
        self.content = " ".join(new_content)

    def add_tag(self, tags):
        self.tags.extend(tags)

    def remove_tag(self, tag):
        self.tags = [t for t in self.tags if t != tag]

    def __str__(self):
        tags_str = ", ".join(self.tags)
        return f"[{self.id}]: {self.content} \n\n Tags: {tags_str}"

    def __repr__(self):
        tags_str = ", ".join(self.tags)
        return f"[{self.id}]: {self.content} \n\n Tags: {tags_str}"

    def __dict__(self):
        return {"id": self.id, "content": self.content}


class NoteBook:
    def __init__(self):
        self.notes = []

    # Notes
    def create_note(self, content):
        new_note = Note(content)
        self.notes.append(new_note)
        return new_note

    def edit_note(self, note_id, new_content):
        note = self.find_note_by_id(note_id)

        if note:
            note.edit(new_content)
            return "Note edited."
        return "Note not found."

    def delete_note(self, note_id):
        for i, note in enumerate(self.notes):
            if int(note.id) == int(note_id):
                del self.notes[i]
                return "Note deleted."
        return "Note not found."

    def find_note_by_id(self, note_id):
        for note in self.notes:
            if int(note.id) == int(note_id):
                return note
        return None

    def search(self, search_string):
        found_notes = [
            note for note in self.notes if search_string.lower() in note.content.lower()
        ]

        return (
            "\n".join(str(note) for note in found_notes)
            if found_notes
            else "No notes found."
        )

    # Tags
    def add_tag_to_note(self, note_id, tag):
        note = self.find_note_by_id(note_id)
        if note:
            note.add_tag(tag)
            return "Tag added."
        return "Note not found."

    def remove_tag_from_note(self, note_id, tag):
        note = self.find_note_by_id(note_id)
        if note:
            note.remove_tag(tag)
            return "Tag removed."
        return "Note not found."

    def find_note_by_tags(self, tags):
        found_notes = [note for note in self.notes if set(tags).issubset(note.tags)]
        return (
            "\n".join(str(note) for note in found_notes)
            if found_notes
            else "No notes found."
        )

    # Dumping to JSON
    def to_json(self):
        return json.dumps({"notes": [note.__dict__() for note in self.notes]})

    # Reading from JSON
    def from_json(self, path):
        with open(path, "r") as file:
            data = json.load(file)

            for record in data.get("records"):
                for note_data in record.get("notes"):
                    new_note = self.create_note(note_data.get("content"))
                    self.add_tag_to_note(new_note.id, note_data.get("tags"))

    def __str__(self):
        return "\n".join(str(note) for note in self.notes)

