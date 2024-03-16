
from datetime import datetime, timedelta
from classes import AddressBook, Record, Address, Email
from cli import Autocompleter
import readline
import os

# Color formatting for better user experience
class Color:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError) as e:
            print(Color.RED + str(e) + Color.END)
            return Color.YELLOW + "Usage: command [arguments]\n" + Color.END
        except KeyError as e:
            print(Color.RED + str(e) + Color.END)
            return Color.YELLOW + "Enter user name.\n" + Color.END

    return inner


def input_error_birthday(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError) as e:
            print(Color.RED + str(e) + Color.END)
            return Color.YELLOW + "Give correct date please.\n" + Color.END

    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


def help_commands():
    return (Color.BOLD + "Available commands:\n" + Color.END +
            "hello" + " - " + "Display a welcome message.\n" +
            "add <name> <phone>" + " - " + "Add a new contact with a phone number.\n" +
            "change <name> <phone>" + " - " + "Change the phone number of an existing contact.\n" +
            "phone <name>" + " - " + "Show the phone number of a contact.\n" +
            "find-phone <phone>" + " - " + "Find a contact by phone number.\n" +
            "all" + " - " + "Show all contacts.\n" +
            "add-address <name> <address>" + " - " + "Add an address to a contact.\n" +
            "edit-address <name> <new_address>" + " - " + "Edit the address of a contact.\n" +
            "show-address <name>" + " - " + "Show the address of a contact.\n" +
            "add-email <name> <email>" + " - " + "Add an email to a contact.\n" +
            "edit-email <name> <new_email>" + " - " + "Edit the email of a contact.\n" +
            "show-email <name>" + " - " + "Show the email of a contact.\n" +
            "find-email <email>" + " - " + "Find a contact by email.\n" +
            "add-birthday <name> <birthday>" + " - " + "Add a birthday to a contact.\n" +
            "show-birthday <name>" + " - " + "Show the birthday of a contact.\n" +
            "birthdays" + " - " + "Show upcoming birthdays.\n" +
            "add-note <name> <note>" + " - " + "Add a note to a contact.\n" +
            "edit-note <name> <note_id> <new_content>" + " - " + "Edit a note of a contact by ID.\n" +
            "delete-note <name> <note_id>" + " - " + "Delete a note of a contact by ID.\n" +
            "find-note <name> <search_content>" + " - " + "Find a note of a contact by content.\n" +
            "show-all-notes <name>" + " - " + "Show all notes of a contact.\n" +
            "add-tag <name> <note_id> <tags>" + " - " + "Add tags to a note of a contact.\n" +
            "delete-tag <name> <note_id> <tag>" + " - " + "Delete a tag from a note of a contact.\n" +
            "find-note-by-tags <name> <tags>" + " - " + "Find notes of a contact by tags.\n" +
            "close/exit" + " - " + "Close the application.\n" +
            Color.BOLD + "Note: All commands are case insensitive.\n" + Color.END)


@input_error
def add_contact(args, book):
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return Color.GREEN + "Contact added.\n" + Color.END


@input_error
def change_contact(args, book):
    name, phone = args
    record = book.find(name)
    if record:
        record.edit_phone(record.phones[0], phone)
        return Color.GREEN + "Contact updated.\n" + Color.END
    else:
        return Color.RED + "Contact not found.\n" + Color.END


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    return record.phones[0] if record else Color.RED + "Contact not found.\n" + Color.END


@input_error
def find_contact_by_phone(args, book):
    phone = args[0]
    record = book.find_by_phone(phone)
    return record.name if record else Color.RED + "Contact not found.\n" + Color.END


@input_error_birthday
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return Color.GREEN + "Birthday added.\n" + Color.END
    else:
        return Color.RED + "Contact not found.\n" + Color.END


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
			
							 
    return (record.birthday.value if record and record.birthday
            else Color.RED + "Contact and birthday not found.\n" + Color.END)
	 


@input_error
def add_address(args, book):
    name, *address = args
    record = book.find(name)
    if record:
        address_str = " ".join(address)
        record.add_address(Address(address_str))
        return Color.GREEN + "Address added.\n" + Color.END
    else:
        return Color.RED + "Contact not found.\n" + Color.END


@input_error
def show_address(args, book):
    name = args[0]
    record = book.find(name)
    return (str(record.address) if record and record.address
            else Color.RED + "Address not found.\n" + Color.END)


@input_error
def change_address(args, book):
    name, new_address = args
    record = book.find(name)
    if record:
        record.edit_address(new_address)
        return Color.GREEN + "Address updated.\n" + Color.END
    else:
        return Color.RED + "Contact not found.\n" + Color.END


@input_error
def add_email(args, book):
    name, email = args
    record = book.find(name)
    if record:
        record.add_email(email)
        return Color.GREEN + "Email added.\n" + Color.END
    else:
        return Color.RED + "Contact not found.\n" + Color.END


@input_error
def change_email(args, book):
    name, new_email = args
    record = book.find(name)
    if record:
        record.edit_email(new_email)
        return Color.GREEN + "Email updated.\n" + Color.END
    else:
        return Color.RED + "Contact not found.\n" + Color.END


@input_error
def show_email(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return (str(record.email.value) if record.email
                else Color.RED + "Email not found.\n" + Color.END)
    else:
        return Color.RED + "Contact not found.\n" + Color.END


@input_error
def find_contact_by_email(args, book):
    email = args[0]
    record = book.find_by_email(email)
    return record.name if record else Color.RED + "Contact not found.\n" + Color.END


@input_error
def add_note(args, book):
    name, *note = args
    record = book.find(name)
    if record:
        record.add_note(note)
        return Color.GREEN + "Note added.\n" + Color.END
    else:
        return Color.RED + "Contact not found.\n" + Color.END


@input_error
def edit_note_by_id(args, book):
    name, note_id, *new_content = args
    record = book.find(name)
    if record:
        return record.edit_note_by_id(note_id, new_content)
    else:
        return Color.RED + "Contact not found.\n" + Color.END


@input_error
def delete_note_by_id(args, book):
    name, note_id = args
    record = book.find(name)
    if record:
        return record.delete_note_by_id(note_id)
    else:
        return Color.RED + "Contact not found.\n" + Color.END


@input_error
def find_note_by_content(args, book):
    name, search_content = args
    record = book.find(name)
    if record:
        return record.find_note_by_content(search_content)
    else:
        return Color.RED + "Contact not found.\n" + Color.END


@input_error
def show_all_notes(args, book):
    name = args[0]
    record = book.find(name)
    return record.notes if record else Color.RED + "Contact not found.\n" + Color.END


@input_error
def add_tag_to_note(args, book):
    name, note_id, *tags = args
    record = book.find(name)
    if record:
        return record.add_tag_to_note_by_id(note_id, tags)
    else:
        return Color.RED + "Contact not found.\n" + Color.END


@input_error
def delete_tag_from_note(args, book):
    name, note_id, tag = args
    record = book.find(name)
    if record:
        return record.remove_tag_from_note_by_id(note_id, tag)
    else:
        return Color.RED + "Contact not found.\n" + Color.END


def find_notes_by_tags(args, book):
    name, *tags = args
    record = book.find(name)
    if record:
        return record.find_notes_by_tags(tags)
    else:
        return Color.RED + "Contact not found.\n" + Color.END

					
def birthdays(book):
    return book.get_birthdays_per_week()


def show_all(book):
    return "\n\n".join(
        f"Name: {record.name}\nPhones: {record.phones}\nEmails: {record.email}\nAddress: {record.address}\nBirthday: {record.birthday}\nNotes: {record.notes}\n"
        for name, record in book.data.items()
    )


def main():
    commands = [
        "hello", "add", "change", "phone", "find-phone", "all", "add-address",
        "edit-address", "show-address", "add-email", "edit-email", "show-email", "find-email",
        "add-birthday", "show-birthday", "birthdays", "add-note", "edit-note", "delete-note",
        "find-note", "show-all-notes", "add-tag", "delete-tag", "find-note-by-tags", "close",
        "exit", "help"
    ]

    completer = Autocompleter(commands)
    readline.set_completer_delims(' \t\n;')
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')

    book = AddressBook()
    print("Welcome to the address book application!")
    book.from_json(os.getcwd() + "/src/book.json")

    try:
        while True:
            user_input = input("Enter a command: ")
            command, args = parse_input(user_input)

            if command in ["close", "exit"]:
                print(Color.YELLOW + "Goodbye!\n" + Color.END)
                book.to_json(os.getcwd() + "/src/book.json")
                break
            elif command == "help":
                print(help_commands())
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, book))
            elif command == "change":
                print(change_contact(args, book))
            elif command == "phone":
                print(show_phone(args, book))
            elif command == "find-phone" and len(args) == 1:
                print(find_contact_by_phone(args, book))
            elif command == "all":
                print(show_all(book))
            elif command == "add-address":
                print(add_address(args, book))
            elif command == "edit-address" and len(args) == 2:
                print(change_address(book, *args))
            elif command == "show-address" and len(args) == 1:
                print(show_address(args, book))
            elif command == "add-email":
                print(add_email(args, book))
            elif command == "edit-email" and len(args) == 2:
                print(change_email(args, book))
            elif command == "show-email" and len(args) == 1:
                print(show_email(args, book))
            elif command == "find-email" and len(args) == 1:
                print(find_contact_by_email(args, book))
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
            elif command == "find-note-by-tags":
                print(find_notes_by_tags(args, book))
            else:
                print(Color.RED + "Invalid command.\n" + Color.END)
    except KeyboardInterrupt:
        print(Color.YELLOW + "Goodbye!\n" + Color.END)
        book.to_json(os.getcwd() + "/src/book.json")

if __name__ == "__main__":
    main()
