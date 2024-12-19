import asyncio
from faker import Faker
from random import choice, sample, randint

from conf.connection import session
from conf.models import Teacher, Student, Group, Subject, Grade


fake = Faker("uk-UA")

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
    "Кібербезпека",
]

NUMBER_GROUPS = 3
NUMBER_STUDENTS = 50
NUMBER_SUBJECTS = 8
NUMBER_TEACHERS = 5
NUMBER_GRADES = 20


def insert_fake_data():
    groups = []
    unique_numbers = sample(range(1, 11), NUMBER_GROUPS)
    for num in unique_numbers:
        group_name = f"Group-{num:02}"
        group = Group(name=group_name)
        groups.append(group)
        session.add(group)

    teachers = []
    for _ in range(NUMBER_TEACHERS):
        first_name, last_name = fake.first_name(), fake.last_name()
        teacher = Teacher(first_name=first_name, last_name=last_name)
        teachers.append(teacher)
        session.add(teacher)

    students = []
    for _ in range(NUMBER_STUDENTS):
        first_name, last_name = fake.first_name(), fake.last_name()
        birthday = fake.date_of_birth(minimum_age=17, maximum_age=23)
        student = Student(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=birthday,
            group=choice(groups),
        )
        students.append(student)
        session.add(student)

    subjects = []
    subject_list = UNI_SUBJECTS.copy()
    for _ in range(NUMBER_SUBJECTS):
        if not subject_list:
            raise IndexError("All subjects have been used.")
        name = subject_list.pop()
        subject = Subject(name=name, teacher=choice(teachers))
        subjects.append(subject)
        session.add(subject)

    for _ in range(NUMBER_GRADES * NUMBER_STUDENTS * NUMBER_SUBJECTS):
        mark = randint(60, 100)
        date_of_grade = fake.date_this_year()
        grade = Grade(
            mark=mark,
            date_of_grade=date_of_grade,
            student=choice(students),
            subject=choice(subjects),
        )
        session.add(grade)


async def main():
    async with session:
        try:
            async with session.begin():
                insert_fake_data()
        except Exception as e:
            await session.rollback()


if __name__ == "__main__":
    asyncio.run(main())
