import subprocess

from sqlalchemy import func, and_, select
from sqlalchemy.exc import SQLAlchemyError
import asyncio
from tabulate import tabulate


from conf.connection import session
from conf.models import Teacher, Student, Group, Subject, Grade


async def tabulate_print(headers, data):
    print(tabulate(data, headers=headers, tablefmt="grid"))


async def select_1():
    # Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    async with session:
        result = await session.execute(
            select(Student.fullname, func.round(func.avg(Grade.mark), 2).label("avg"))
            .join(Grade)
            .group_by(Student.id)
            .order_by(func.avg(Grade.mark).desc())
            .limit(5)
        )
        return result


async def select_2():
    # Знайти студента із найвищим середнім балом з певного предмета.
    async with session:
        result = await session.execute(
            select(
                Student.fullname,
                Subject.name,
                func.round(func.avg(Grade.mark), 2).label("avg"),
            )
            .select_from(Student)
            .join(Grade)
            .join(Subject)
            .filter(Subject.name == "Кібербезпека")
            .group_by(Student.id, Subject.name)
            .order_by(func.avg(Grade.mark).desc())
            .limit(1)
        )
        return result


async def select_3():
    # Знайти середній бал у групах з певного предмета.
    async with session:
        result = await session.execute(
            select(
                Group.name,
                func.round(func.avg(Grade.mark), 2).label("avg"),
            )
            .select_from(Group)
            .join(Student)
            .join(Grade)
            .join(Subject)
            .filter(Subject.name == "Кібербезпека")
            .group_by(Group.name)
            .order_by(func.avg(Grade.mark).desc())
        )
        return result


async def select_4():
    # Знайти середній бал на потоці (по всій таблиці оцінок).
    async with session:
        result = await session.execute(
            select(
                func.round(func.avg(Grade.mark), 2).label("avg"),
            )
        )
        return result


async def select_5():
    # Знайти які курси читає певний викладач.
    async with session:
        result = await session.execute(
            select(
                Subject.name,
            )
            .join(Teacher)
            .filter(Teacher.fullname == "Єлисавета Саєнко")
            .order_by(Subject.name)
        )
        return result


async def select_6():
    # Знайти список студентів у певній групі.
    async with session:
        result = await session.execute(
            select(Student.fullname)
            .join(Group)
            .filter(Group.name == "Group-01")
            .order_by(Student.fullname)
        )
        return result


async def select_7():
    # Знайти оцінки студентів у окремій групі з певного предмета.
    async with session:
        result = await session.execute(
            select(Student.fullname, Grade.mark, Grade.date_of_grade)
            .join(Group)
            .join(Grade)
            .join(Subject)
            .filter(Subject.name == "Кібербезпека", Group.name == "Group-01")
            .order_by(Student.fullname.desc())
        )
        return result


async def select_8():
    # Знайти середній бал, який ставить певний викладач зі своїх предметів.
    async with session:
        result = await session.execute(
            select(func.round(func.avg(Grade.mark), 2).label("avg"))
            .join(Subject)
            .join(Teacher)
            .filter(
                Teacher.fullname == "Єлисавета Саєнко",
            )
        )
        return result


async def select_9():
    # Знайти список курсів, які відвідує певний студент.
    async with session:
        result = await session.execute(
            select(Subject.name)
            .join(Grade)
            .join(Student)
            .filter(Student.fullname == "Максим Романчук")
            .distinct()
        )
        return result


async def select_10():
    # Список курсів, які певному студенту читає певний викладач.
    async with session:
        result = await session.execute(
            select(Subject.name)
            .join(Grade)
            .join(Student)
            .join(Teacher)
            .filter(
                and_(
                    Student.fullname == "Максим Романчук",
                    Teacher.fullname == "Єлисавета Саєнко",
                )
            )
            .distinct()
        )
        return result


async def select_11():
    # Середній бал, який певний викладач ставить певному студентові.
    async with session:
        result = await session.execute(
            select(
                func.round(func.avg(Grade.mark), 2).label("avg"),
            )
            .join(Student)
            .join(Subject)
            .join(Teacher)
            .filter(
                and_(
                    Student.fullname == "Максим Романчук",
                    Teacher.fullname == "Єлисавета Саєнко",
                )
            )
        )
        return result


async def select_12():
    # Оцінки студентів у певній групі з певного предмета на останньому занятті.
    async with session:
        subquery = (
            select(func.max(Grade.date_of_grade))
            .join(Student)
            .join(Subject)
            .join(Group)
            .filter(and_(Subject.name == "Кібербезпека", Group.name == "Group-06"))
        ).as_scalar()

        result = await session.execute(
            select(Student.fullname, Grade.mark)
            .select_from(Grade)
            .join(Student)
            .join(Subject)
            .join(Group)
            .filter(
                and_(
                    Subject.name == "Кібербезпека",
                    Group.name == "Group-06",
                    Grade.date_of_grade == subquery,
                )
            )
        )
        return result


async def main():
    try:
        results = []
        # results.append(await select_1())
        # results.append(await select_2())
        # results.append(await select_3())
        # results.append(await select_4())
        # results.append(await select_5())
        # results.append(await select_6())
        # results.append(await select_7())
        # results.append(await select_8())
        # results.append(await select_9())
        # results.append(await select_10())
        # results.append(await select_11())
        results.append(await select_12())
        for result in results:
            await tabulate_print(result.keys(), result.all())
            # print(result.all())
    except SQLAlchemyError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
