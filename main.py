import pickle
from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Incorrect phone number format")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Incorrect date_of_birth format")
        super().__init__(value)

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        if birthday:
            self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            self.remove_phone(old_phone)
            self.add_phone(new_phone)
        else:
            raise ValueError("Phone number not found")

    def find_phone(self, phone):
        phone = Phone(phone)
        for phone_obj in self.phones:
            if phone_obj == phone:
                return str(phone_obj)
        return None

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now()
            birthday_date = datetime.strptime(self.birthday.get_value(), "%Y-%m-%d").replace(year=today.year)
            if today > birthday_date:
                birthday_date = birthday_date.replace(year=today.year + 1)
            return (birthday_date - today).days
        return None

    def __str__(self):
        phone_str = "; ".join(str(p) for p in self.phones)
        birthday_str = f", Birthday: {self.birthday.get_value()}" if self.birthday else ""
        return f"Contact name: {self.name.get_value()}, phones: {phone_str}{birthday_str}"

class AddressBook(UserDict):
    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name
        self.load()  # Data is loaded during initialization

    def load(self):
        try:
            with open(self.file_name, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            self.data = {}

    def save(self):
        with open(self.file_name, 'wb') as file:
            pickle.dump(self.data, file)

    def add_record(self, record):
        self.data[record.name.get_value()] = record
        self.save()  # Save changes after adding a record

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            self.save()  # Save changes after deleting an entry

    def search(self, query):
        results = []
        for record in self.data.values():
            if query in record.name.get_value() or any(query in str(phone) for phone in record.phones):
                results.append(record)
        return results

    def iterator(self, page_size):
        records = list(self.data.values())
        total_records = len(records)
        current_page = 0
        while current_page * page_size < total_records:
            yield records[current_page * page_size:(current_page + 1) * page_size]
            current_page += 1
