from collections import UserDict
from datetime import datetime


def convert_to_date(birthday: str = ""):
    try:
        birthday = datetime.strptime(birthday, '%m.%d.%Y')
    except ValueError:
        try:
            birthday = datetime.strptime(birthday, '%m.%d')
            birthday = birthday.replace(year=2)
        except ValueError:
            birthday = None
    finally:
        return birthday


class Field:
    def __init__(self):
        self.__value = None


class Name(Field):
    def __init__(self, name: str):
        super().__init__()
        self.value = name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, name: str = ""):
        if name:
            self.__value = name


class Phone(Field):
    def __init__(self, phone_number=None):
        super().__init__()
        self.__value = None
        self.value = phone_number

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone_number: str = ""):
        if phone_number:
            phone_number = phone_number.strip().replace(" ", "").replace("(", "").replace(")", "").replace("-", "")
            if phone_number.startswith("+"):
                if len(phone_number[1:]) == 12 and phone_number[1:].isdigit():
                    self.__value = phone_number
            else:
                if phone_number.isdigit and (len(phone_number) == 12 or
                                             len(phone_number) == 10 or len(phone_number) == 7):
                    self.__value = phone_number


class Birthday(Field):
    def __init__(self, birthday=""):
        super().__init__()
        self.value = convert_to_date(birthday)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, birthday: datetime):
        if birthday.year > 1:
            self.__value = birthday


class Record:
    def __init__(self, name: Name, phones: list[Phone] = [], birthday: Birthday = None) -> None:
        self.name = name
        self.phones = phones
        self.birthday = birthday

    def __repr__(self):
        string = ""
        string += f"{self.name.value}:"
        if self.phones:
            string += f"\n\tPhone numbers: {', '.join([x.value for x in self.phones])}"
        if self.birthday:
            birthday = self.birthday.value
            if birthday.year > 2:
                string += f"\n\tBirthday: {birthday.strftime('%d %B %Y')}"
            else:
                string += f"\n\tBirthday: {birthday.strftime('%d %B')}"
            when_to_congratulate = self.days_to_birthday()
            if when_to_congratulate == 0:
                string += f"\n\tToday is {self.name.value}'s birthday."
            elif when_to_congratulate == 1:
                string += f"\n\t{self.name.value} has birthday tomorrow."
            else:
                string += f"\n\t{self.name.value}'s birthday is in {when_to_congratulate} days."
        string += "\n"
        return string

    def add_number(self, number: Phone):
        self.phones.append(number)

    def del_number(self, number: Phone):
        for x in self.phones:
            if x.value == number.value:
                self.phones.remove(x)

    def set_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def days_to_birthday(self):
        next_birthday = self.birthday.value.replace(year=datetime.now().year)
        next_birthday = next_birthday.replace(hour=0, minute=0, second=0, microsecond=0)
        current_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if next_birthday < current_day:
            next_birthday = next_birthday.replace(year=datetime.now().year+1)
        return (next_birthday-current_day).days


class AddressBook(UserDict):

    def __init__(self):
        super().__init__(self)
        self.showing_records = False  # when True 'enter' shows next N contacts
        self.show = None

    def add_record(self, record: Record):
        self.data[record.name.value] = record
        self.reset_iterator(2)

    def reset_iterator(self, n: int):
        self.show = self.iterator(n)

    def delete_record(self, name: str):
        self.data.pop(name)

    def iterator(self, n: int):
        string = ""
        for i, contact in enumerate(self.data.keys()):
            if not i % n:
                string = ""
            string += str(self.data.get(contact))
            if not (i+1) % n or i == len(self.data.keys())-1:
                yield string
