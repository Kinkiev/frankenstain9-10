from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name, phone=None):
        self.name = Name(name)
        self.phones = []
        if phone is not None:
            self.add_phone(phone)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def change_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if str(phone) == str(old_phone):
                self.phones[i] = new_phone
                break

    def __str__(self):
        return f"Name: {self.name}, Phones: {', '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[str(record.name)] = record

    def remove_record(self, name):
        del self.data[str(name)]

    def search_by_name(self, name):
        results = []
        for record in self.data.values():
            if str(record.name) == name:
                results.append(record)
        return results

    def change_phone_by_name(self, name, new_phone):
        results = self.search_by_name(name)
        for result in results:
            result.change_phone(result.phones[0], Phone(new_phone))

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())


def help() -> str:
    return "Available commands:\n" \
           "- hello\n" \
           "- add [name] [phone]\n" \
           "- change [name] [phone]\n" \
           "- find [name]\n" \
           "- show_all\n" \
           "- help \n" \
           "- good bye, close, exit"


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return "contact not found"
        except ValueError:
            return "invalid input"
        except IndexError:
            return "Invalid input"
        except Exception:
            return help()

    return wrapper


ab = AddressBook()


@input_error
def add(name: str, phone: str) -> str:
    record = Record(Name(name), Phone(phone))
    ab.add_record(record)
    return "add success"


@input_error
def find(name: str) -> str:
    results = ab.search_by_name(name)
    if results:
        return str(results[0])
    else:
        raise KeyError("Contact not found")


@input_error
def change(name: str, new_phone: str) -> str:
    ab.change_phone_by_name(name, new_phone)
    return "phone number updated"


@input_error
def show_all() -> str:
    if len(ab) == 0:
        return "no contacts found"
    else:
        output = ""
        for record in ab.values():
            output += str(record) + "\n"
        return output.strip()


@input_error
def no_command(*args):
    return " - not valid command entered\n" \
           " - type 'help' for commands"


@input_error
def hello() -> str:
    return "How can I help you?"


@input_error
def close() -> str:
    return "Good bye!"


commands = {
    "hello": hello,
    "add": add,
    "change": change,
    "find": find,
    "show_all": show_all,
    "help": help,
    "good bye": close,
    "close": close,
    "exit": close
}


@input_error
def parser(text: str) -> tuple[callable, tuple[str]]:
    text_lower = text.lower()
    words = text_lower.split()

    if words[0] in commands:
        command = commands[words[0]]
        args = tuple(words[1:])
        return command, args

    return no_command, ()


def main():
    while True:
        user_input = input(">>>")
        command, data = parser(user_input)

        if command == close:
            break

        result = command(*data)
        print(result)


if __name__ == "__main__":
    main()
