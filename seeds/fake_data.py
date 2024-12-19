from abc import ABC, abstractmethod
from faker import Faker
from random import choice, randint, uniform


fake = Faker('uk-UA')
UNI_SUBJECTS = [
    "Математика",
    "Фізика",
    "Програмування",
    "Англійська мова",
    "Алгоритми та структури даних",
    "Економіка",
    "Інформатика",
    "Філософія",
    "Історія",
    "Правознавство",
    "Мережі комп'ютерів",
    "Бази даних",
    "Операційні системи",
    "Системи штучного інтелекту",
    "Кібербезпека"
    ]


class DataGenerator(ABC):
    @abstractmethod
    def generate_fake_data(self) -> list:
        pass


class StudentDataGenerator(DataGenerator):
    def generate_fake_data(self) -> list:
        """Generate fake data for a student."""
        return [
            fake.first_name(),
            fake.last_name(),
            fake.date_of_birth(minimum_age=17, maximum_age=23),
        ]


class GroupDataGenerator(DataGenerator):
    def generate_fake_data(self) -> list:
        return [fake.unique.bothify(text=f"Group-{randint(1, 10):02}"),]


class TeacherDataGenerator(DataGenerator):
    def generate_fake_data(self) -> list:
        return [fake.first_name(), fake.last_name()]


class SubjectDataGenerator(DataGenerator):
    def __init__(self) -> None:
        self.subjects = UNI_SUBJECTS.copy()
    def generate_fake_data(self) -> list:
        if not self.subjects:
            raise IndexError("All subjects have been used.")
        return [self.subjects.pop(),]


class GradeDataGenerator(DataGenerator):
    def generate_fake_data(self) -> list:
        return [uniform(60.00, 100.00), fake.date_this_year(),]


class DataGeneratorFactory:
    @staticmethod
    def create_data_generator(generator_type: str) -> DataGenerator:
        mapping = {
            "student": StudentDataGenerator(),
            "group": GroupDataGenerator(),
            "teacher": TeacherDataGenerator(),
            "subject": SubjectDataGenerator(),
            "grade": GradeDataGenerator()
        }
        if generator_type not in mapping:
            raise ValueError(f"Unknown data generator type: {generator_type}")
        return mapping[generator_type]