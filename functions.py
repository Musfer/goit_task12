from classes import *
import re


phone_pattern = "\s\+?[-\s]?(?:\d{2,3})?[-\s]?(?:\([-\s]?\d{2,3}[-\s]?\)|\d{2,3})?[-\s]?\d{2,3}[-\s]?\d{2,3}[-\s]?\d{2,3}\s"
no_number = "Sorry, I can't identify a phone number."
no_name = "Sorry, I can't identify a contact's name."


def save_to_file(book: AddressBook, text: str = ""):
    text = text.strip()
    return book.write_to_file(text)


def read_from_file(book: AddressBook, text: str = ""):
    text = text.strip()
    return book.read_from_file(text)


def clear(book: AddressBook, *_):
    if confirm(f"Do you want to delete all contacts from your Address book? Type 'yes'/'no'.\n"):
        book.clear()
        return f"Done!"
    else:
        return f"Glad you changed your mind."


def confirm(question):
    while True:
        string = input(question)
        if string.strip().lower() in ("y", "yes"):
            return True
        if string.strip().lower() in ("n", "no"):
            return False


def find_name_number(text: str):  # return tuple of name and number
    text += " "
    pattern = re.compile(phone_pattern)
    only_name = text
    if not pattern.findall(text):
        return find_name(text), ""
    for x in pattern.findall(text):
        only_name = only_name[:only_name.find(x)]
    return find_name(only_name), str(pattern.findall(text)[0]).strip().replace(" ", "").replace("", ""),


def find_name(text: str):  # converts text into name. Should be used only after the numer has been extracted.
    return text.strip().lower().title()


def find(book: AddressBook, text: str):
    contacts = book.search_in_names(text)  # list of names
    numbers = book.search_in_phones(text)  # list of tuples (name, number)
    result = ""
    if not (contacts or numbers):
        return "No matches found"
    else:
        if contacts:
            result += f"Matches in names:\n"
            for name in contacts:
                result += f"\t{name}\n"
        if numbers:
            result += f"Matches in phone numbers:\n"
            for pair in numbers:
                result += f"\t{pair[0]}: {pair[1]}\n"
        return result


def name_birthday(book: AddressBook, text: str):
    for contact in book.data.keys():
        if contact.lower() in text.lower():
            return contact, text.lower().replace(contact.lower(), "").strip()
    return 0


def add_contact(book: AddressBook, data: str):
    name, number = find_name_number(data)
    if not name:
        return no_name
    elif name in book.data.keys():
        return f"Contact '{name}' already exists"
    else:
        phone_number = Phone(number)
        if phone_number.value:
            record = Record(Name(name), [phone_number])
            book.add_record(record)
            return f"Created contact '{name}': '{number}'"
        else:
            record = Record(Name(name), [])
            book.add_record(record)
            return f"Created contact '{name}' with no phone numbers."


def show_contact(book: AddressBook, data: str):
    name = find_name(data)
    if not name:
        return "Sorry, I can't identify a contact's name"
    if name not in book.data.keys():
        return f"Contact '{name}' is not in your contacts"
    else:
        return str(book.data.get(name))


def empty(book: AddressBook, *_):
    if not book.showing_records:
        return "Sorry I can't understand you. Try 'help' command to see what I can."
    else:
        return show_all(book)


def reset(book: AddressBook, text: str = "2"):
    try:
        n = int(text.strip())
    except ValueError:
        n = 2
    book.reset_iterator(n)
    return "Done!"


def show_all(book: AddressBook, text: str = ""):
    try:
        n = int(text.strip())
    except ValueError:
        n = 10
    if not book.data:
        return "Your phone book is empty."
    else:
        if not book.showing_records:
            book.showing_records = True
            book.reset_iterator(n)
        try:
            return next(book.show) + f"Press 'Enter' to show next '{n}' contacts or 'reset' to go to the start"
        except StopIteration:
            book.showing_records = False
            book.reset_iterator(n)
            return "End of address book"


def phone(book: AddressBook, data: str):
    name = find_name(data)
    if not name:
        return "Sorry, I can't identify a contact's name"
    if name not in book.data.keys():
        return f"Contact '{name}' is not in your contacts"
    else:
        return f"{name}: {', '.join([x.value for x in book.data.get(name).phones])}"


def add_number(book: AddressBook, data: str):
    name, number = find_name_number(data)
    if not name:
        return no_name
    elif not number:
        return no_number
    elif name not in book.data.keys():
        add_contact(book, data)
        return f"Created a new contact '{name}' with number '{number}'"
    else:
        phone_number = Phone(number)
        if phone_number.value:
            book.data[name].add_number(phone_number)
            return f"Number '{number}' has been added to contact '{name}'"
        else:
            return f"Invalid phone number"


def delete_number(book: AddressBook, data: str):
    name, number = find_name_number(data)
    if name and not number:
        if name in book.data.keys():
            if confirm(f"Do you want to delete all numbers from contact '{name}'? Type 'yes'/'no'.\n"):
                book.data[name] = Record(Name(name))
                return f"Done!"
            else:
                return f"Glad you changed your mind."
        else:
            return f"Contact {name} does not exist."
    elif name and number:
        if name in book.data.keys():
            if number in [x.value for x in book.data.get(name).phones]:
                book.data.get(name).del_number(Phone(number))
                return f"Number '{number}' has been deleted from contact '{name}'"
            else:
                return f"Contact '{name}' has no phone number '{number}'."
    else:
        return no_name


def delete_contact(book: AddressBook, data: str):
    name, number = find_name_number(data)
    if not name:
        return no_name
    elif name in book.data.keys():
        if confirm(f"Contact '{name}' will be deleted from your phone book. Are you sure? Type 'yes' or 'no'.\n"):
            book.delete_record(name)
            return "Done!"
        else:
            return f"Glad you changed your mind."


def set_birthday(book: AddressBook, data: str):
    if not name_birthday(book, data):
        return "Contact does not exist"
    else:
        name, birthday = name_birthday(book, data)
        book.data.get(name).set_birthday(Birthday(birthday))
        return "Done"


def delete_birthday(book: AddressBook, data: str):
    if not name_birthday(book, data):
        return "Contact does not exist"
    else:
        name, birthday = name_birthday(book, data)
        book.data.get(name).set_birthday(None)
        return "Done"


def help_me(*_):
    return "Hi! Here is the list of known commands:\n" + \
           "\tshow all: shows all your contacts by '2' on page\n" + \
           "\t\tor try:\tshow all 'n': to show all your contacts by 'n' on page\n" + \
           "\treset 'n': return to the start of the contacts, sets showed number of contacts on page to 'n'\n" + \
           "\tshow contact 'name': shows information about contact\n" + \
           "\tphone 'name': shows all phone numbers of the contact\n" + \
           "\tadd contact 'name' 'phone number': creates a new contact\n" + \
           "\tset birthday 'name' 'birthday': sets contacts birthday\n" +\
           "\t\t 'birthday' should be in forman 'mm.dd' or 'mm.dd.year'\n" +\
           "\tdelete birthday 'name': deletes birthday from the contact\n" +\
           "\tdelete contact 'name': deletes contact 'name'\n" + \
           "\tadd phone 'name' 'phone numer': adds the phone number to the existing contact or creates a new one\n" + \
           "\t\tphone number should be 7 digits long + optional 3 digits of city code\n" + \
           "\t\t+ optional 2 digits of country code + optional '+' sight\n" + \
           "\tdelete phone 'name' 'phone number': deletes the phone number from contact\n" + \
           "\tsave 'file name': saves you Address book to 'file name'\n" + \
           "\tload 'file name': loads existing Address book from 'file name'\n" + \
           "\tfind 'string': searches 'string' in names and phone numbers" +\
           "\tclear: clears your Address book\n" + \
           "\texit: close the assistant\n"
