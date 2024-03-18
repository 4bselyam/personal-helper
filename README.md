# Personal helper by group #6


## Installation
### Setup Instructions

```bash
git clone https://github.com/4bselyam/personal-helper.git
cd personal-helper

# Install requirements
pip install -r requirements.txt
```

## Execution

```bash
cd src/
python main.py
```

## Available commands

`hello` - Display a welcome message

`add` <name> <phone> - Add a new contact with a phone number

`change` <name> <phone> - Change the phone number of an existing contact

`phone` <name> - Show the phone number of a contact

`find-phone` <phone> - Find a contact by phone number

`all` - Show all contacts

`add-address` <name> <address> - Add an address to a contact

`edit-address` <name> <new_address> - Edit the address of a contact

`show-address` <name> - Show the address of a contact

`edit-email` <name> <new_email> - Edit the email of a contact

`show-email` <name> - Show the email of a contact

`find-email` <email> - Find a contact by email

`add-birthday` <name> <birthday> - Add a birthday to a contact

`show-birthday` <name> - Show the birthday of a contact

`birthdays` - Show upcoming birthdays

`add-note` <name> <note> - Add a note to a contact

`edit-note` <name> <note_id> <new_content> - Edit a note of a contact by ID

`delete-note` <name> <note_id> - Delete a note of a contact by ID

`find-note` <name> <search_content> - Find a note of a contact by content

`show-all-notes` <name> - Show all notes of a contact

`add-tag` <name> <note_id> <tags> - Add tags to a note of a contact

`delete-tag` <name> <note_id> <tag> - Delete a tag from a note of a contact

`find-note-by-tags` <name> <tags> - Find notes of a contact by tags

`close/exit` - Close the application

*Note: All commands are case insensitive
