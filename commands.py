import sys
from functions import add_contact, show_all, phone, add_number, help_me, delete_number, delete_contact, set_birthday
from functions import show_contact, empty, reset, delete_birthday, find, save_to_file, read_from_file


commands = {
    "hello": lambda *_: "How can I help you?",
    "bye": lambda *_: "Good bye!",
    "add_contact": add_contact,
    "add_number": add_number,
    "find": find,
    "delete_contact": delete_contact,
    "delete_number": delete_number,
    "phone": phone,
    "show": show_contact,
    "show_all": show_all,
    "help_me": help_me,
    "set_birthday": set_birthday,
    "empty": empty,
    "reset": reset,
    "save": save_to_file,
    "load": read_from_file,
    "delete_birthday": delete_birthday,
    0: lambda *_: "Sorry I can't understand you. Try 'help' command to see what I can.",
}


def def_mod(string: str):
    try:
        mods = {
            # ".": "exit",
            "hello": "hello",
            "good bye": "bye",
            "close": "bye",
            "exit": "bye",
            "save": "save",
            "load": "load",
            "add contact": "add_contact",
            "add phone number": "add_number",
            "add phone": "add_number",
            "add number": "add_number",
            "find": "find",
            # "add": "add_contact",
            "delete contact": "delete_contact",
            "delete phone number": "delete_number",
            "delete phone": "delete_number",
            "delete number": "delete_number",
            "delete birthday": "delete_birthday",
            "phone": "phone",
            "show contact": "show",
            "show all": "show_all",
            "reset": "reset",
            "set birthday": "set_birthday",
            "help": "help_me",
        }
        if not string:
            return "empty", ""
        for key_word in mods.keys():
            if key_word in string.lower():
                return mods[key_word], string.replace(key_word, "")
        return 0, ""
    except Exception as err:
        return err
