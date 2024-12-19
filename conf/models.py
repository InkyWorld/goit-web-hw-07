from typing import List, Optional
from sqlalchemy import Date, SmallInteger, String, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr,
    relationship,
)
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)


class Student(Base):
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    date_of_birth: Mapped[date] = mapped_column(Date)
    group_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("groups.id", ondelete="SET NULL")
    )

    group: Mapped[Optional["Group"]] = relationship("Group", back_populates="students")
    grades: Mapped[List["Grade"]] = relationship(
        "Grade", back_populates="student", cascade="all, delete-orphan"
    )

    @hybrid_property
    def fullname(self):
        return self.first_name + " " + self.last_name


class Group(Base):
    name: Mapped[str] = mapped_column(String(50), unique=True)

    students: Mapped[List["Student"]] = relationship("Student", back_populates="group")


class Teacher(Base):
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))

    subjects: Mapped[List["Subject"]] = relationship(
        "Subject", back_populates="teacher"
    )

    @hybrid_property
    def fullname(self):
        return self.first_name + " " + self.last_name


class Subject(Base):
    name: Mapped[str] = mapped_column(String(100), unique=True)
    teacher_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("teachers.id", ondelete="SET NULL")
    )

    teacher: Mapped[Optional["Teacher"]] = relationship(
        "Teacher", back_populates="subjects"
    )


class Grade(Base):
    mark: Mapped[int] = mapped_column(SmallInteger)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE")
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id", ondelete="CASCADE")
    )
    date_of_grade: Mapped[date] = mapped_column(Date)

    student: Mapped["Student"] = relationship("Student", back_populates="grades")
    subject: Mapped["Subject"] = relationship("Subject")
