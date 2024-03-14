from datetime import datetime, timedelta
from classes import AddressBook, Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError) as e:
            print(e)
            return "Give me name and phone please."
        except KeyError as e:
            print(e)
            return "Enter user name."

    return inner


def input_error_birthday(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError) as e:
            print(e)
            return "Give correct date please."

    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Contact added."


@input_error
def change_contact(args, book):
    name, phone = args
    record = book.find(name)
    if record:
        record.edit_phone(record.phones[0], phone)
        return "Contact updated."
    else:
        return "Contact not found."


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    return record.phones[0] if record else "Contact not found."


@input_error_birthday
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        return "Contact not found."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    return (
        record.birthday.birthday.strftime("%d.%m.%Y")
        if record and record.birthday
        else "Contact and birthday not found."
    )


@input_error
def add_note(args, book):
    name, *note = args
    record = book.find(name)
    if record:
        record.add_note(note)
        return "Note added."
    else:
        return "Contact not found."


@input_error
def edit_note_by_id(args, book):
    name, note_id, *new_content = args
    record = book.find(name)
    if record:
        return record.edit_note_by_id(note_id, new_content)
    else:
        return "Contact not found."


@input_error
def delete_note_by_id(args, book):
    name, note_id = args
    record = book.find(name)
    if record:
        return record.delete_note_by_id(note_id)
    else:
        return "Contact not found."


@input_error
def find_note_by_content(args, book):
    name, search_content = args
    record = book.find(name)
    if record:
        return record.find_note_by_content(search_content)
    else:
        return "Contact not found."


@input_error
def show_all_notes(args, book):
    name = args[0]
    record = book.find(name)
    return record.notes if record else "Contact not found."


@input_error
def add_tag_to_note(args, book):
    name, note_id, *tags = args
    record = book.find(name)
    if record:
        return record.add_tag_to_note_by_id(note_id, tags)
    else:
        return "Contact not found."


@input_error
def delete_tag_from_note(args, book):
    name, note_id, tag = args
    record = book.find(name)
    if record:
        return record.remove_tag_from_note_by_id(note_id, tag)
    else:
        return "Contact not found."


def birthdays(book):
    return book.get_birthdays_per_week()


def show_all(book):
    return "\n".join(
        f"{record.name}: {record.phones}" for name, record in book.data.items()
    )


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        elif command == "add-note":
            print(add_note(args, book))
        elif command == "edit-note":
            print(edit_note_by_id(args, book))
        elif command == "delete-note":
            print(delete_note_by_id(args, book))
        elif command == "find-note":
            print(find_note_by_content(args, book))
        elif command == "show-all-notes":
            print(show_all_notes(args, book))
        elif command == "add-tag":
            print(add_tag_to_note(args, book))
        elif command == "delete-tag":
            print(delete_tag_from_note(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
