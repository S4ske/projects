from uuid import UUID, uuid4
from sqlalchemy import Column
from sqlalchemy.orm import declarative_base, Relationship, Mapped
from pydantic import EmailStr

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = Column(default_factory=uuid4, primary_key=True)
    hashed_password: Mapped[str] = Column()
    projects: Mapped[list['Project']] = Relationship(back_populates='members')
    email: Mapped[EmailStr] = Column(unique=True, index=True, max_length=255)
    is_active: Mapped[bool] = True
    is_superuser: Mapped[bool] = False
    username: Mapped[str] | None = Column(default=None, max_length=255)


class Project(Base):
    __tablename__ = "project"

    id: Mapped[UUID] = Column(default_factory=uuid4, primary_key=True)
    tasks: Mapped[list['Task']] = Relationship(back_populates='project')
    members: Mapped[list[User]] = Relationship(back_populates='projects')


class Task(Base):
    __tablename__ = "task"

    id: Mapped[UUID] = Column(default_factory=uuid4, primary_key=True)
    project: Mapped['Project'] = Relationship(back_populates='tasks')
    members: Mapped[list[User]] = Relationship()
