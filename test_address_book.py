import unittest

from main import AddressBook, Field, Name, Phone, Record


class TestFieldAndSubclasses(unittest.TestCase):
    def test_field_str_and_value(self):
        field = Field("test")
        self.assertEqual(field.value, "test")
        self.assertEqual(str(field), "test")

    def test_name_valid(self):
        name = Name("John")
        self.assertEqual(name.value, "John")
        self.assertEqual(str(name), "John")

    def test_name_invalid_raises(self):
        for invalid in ("", "   ", None, 123):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    Name(invalid)

    def test_phone_valid(self):
        phone = Phone("1234567890")
        self.assertEqual(phone.value, "1234567890")
        self.assertEqual(str(phone), "1234567890")

    def test_phone_invalid_raises(self):
        invalid_numbers = [
            "123456789",       # 9 digits
            "12345678901",     # 11 digits
            "12345abcde",      # letters
            "+380123456",      # symbols
            "",                # empty
            "123456789²",      # non-ASCII superscript digit
            1234567890,        # int instead of str
        ]
        for invalid in invalid_numbers:
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    Phone(invalid)

    def test_phone_setter_validates(self):
        phone = Phone("1234567890")
        with self.assertRaises(ValueError):
            phone.value = "123"
        self.assertEqual(phone.value, "1234567890")


class TestRecord(unittest.TestCase):
    def test_record_creation(self):
        record = Record("John")
        self.assertIsInstance(record.name, Name)
        self.assertEqual(record.name.value, "John")
        self.assertEqual(record.phones, [])

    def test_add_and_find_phone(self):
        record = Record("John")
        record.add_phone("1234567890")
        record.add_phone("5555555555")
        record.add_phone("1234567890")  # duplicate ignored

        self.assertEqual(len(record.phones), 2)
        found = record.find_phone("5555555555")
        self.assertIsInstance(found, Phone)
        self.assertEqual(found.value, "5555555555")
        self.assertIsNone(record.find_phone("0000000000"))

    def test_edit_phone(self):
        record = Record("John")
        record.add_phone("1234567890")
        record.add_phone("5555555555")

        record.edit_phone("1234567890", "1112223333")
        self.assertEqual([p.value for p in record.phones], ["1112223333", "5555555555"])

        with self.assertRaises(ValueError):
            record.edit_phone("9999999999", "1112223333")

        with self.assertRaises(ValueError):
            record.edit_phone("1112223333", "invalid")
        self.assertEqual([p.value for p in record.phones], ["1112223333", "5555555555"])

    def test_remove_phone(self):
        record = Record("John")
        record.add_phone("1234567890")
        record.add_phone("5555555555")

        record.remove_phone("1234567890")
        self.assertEqual([p.value for p in record.phones], ["5555555555"])

        with self.assertRaises(ValueError):
            record.remove_phone("1234567890")

    def test_str(self):
        record = Record("John")
        record.add_phone("1112223333")
        record.add_phone("5555555555")
        self.assertEqual(
            str(record),
            "Contact name: John, phones: 1112223333; 5555555555",
        )


class TestAddressBook(unittest.TestCase):
    def test_add_find_delete_record(self):
        book = AddressBook()
        john = Record("John")
        john.add_phone("1234567890")
        jane = Record("Jane")
        jane.add_phone("9876543210")

        book.add_record(john)
        book.add_record(jane)

        self.assertIs(book.find("John"), john)
        self.assertIs(book.find("Jane"), jane)
        self.assertIsNone(book.find("Missing"))

        book.delete("Jane")
        self.assertIsNone(book.find("Jane"))
        book.delete("Jane")  # deleting missing record should not raise

    def test_add_non_record_raises(self):
        book = AddressBook()
        with self.assertRaises(TypeError):
            book.add_record("Not a Record")


if __name__ == "__main__":
    unittest.main()
