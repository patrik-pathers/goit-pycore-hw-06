from collections import UserDict


class Field:
    """Base class for record fields."""

    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value!r})"


class Name(Field):
    """Contact name field (required, non-empty string)."""

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, new_value: str) -> None:
        if not isinstance(new_value, str) or not new_value.strip():
            raise ValueError("Name must be a non-empty string.")
        self._value = new_value.strip()


class Phone(Field):
    """Contact phone number field with 10-digit validation."""

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, new_value: str) -> None:
        if not isinstance(new_value, str) or not (
            len(new_value) == 10 and new_value.isascii() and new_value.isdigit()
        ):
            raise ValueError("Phone number must contain exactly 10 digits.")
        self._value = new_value


class Record:
    """Stores contact information including name and a list of phone numbers."""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []

    def add_phone(self, phone: str) -> None:
        """Add a validated phone number to the contact record."""
        validated_phone = Phone(phone)
        if self.find_phone(validated_phone.value) is None:
            self.phones.append(validated_phone)

    def remove_phone(self, phone: str) -> None:
        """Remove a phone number from the contact record."""
        target = self.find_phone(phone)
        if target is None:
            raise ValueError(f"Phone number '{phone}' not found.")
        self.phones.remove(target)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Replace an existing phone number with a new validated phone number."""
        for index, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[index] = Phone(new_phone)
                return
        raise ValueError(f"Phone number '{old_phone}' not found.")

    def find_phone(self, phone: str) -> Phone | None:
        """Find and return a Phone object by its value, or None if not found."""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    """Manages a collection of contact records keyed by contact name."""

    def add_record(self, record: Record) -> None:
        """Add a Record instance to the address book."""
        if not isinstance(record, Record):
            raise TypeError("Only Record instances can be added to AddressBook.")
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        """Find and return a Record by contact name, or None if not found."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Delete a Record from the address book by contact name."""
        self.data.pop(name, None)


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону в записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
