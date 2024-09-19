from uuid import UUID, uuid4
from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column

Base = declarative_base()


users_to_projects = Table(
    "users_to_projects",
    Base.metadata,
    Column('user_id', ForeignKey("user.id"), primary_key=True),
    Column('project_id', ForeignKey("project.id"), primary_key=True),
)

users_to_tasks = Table(
    "users_to_tasks",
    Base.metadata,
    Column('user_id', ForeignKey("user.id"), primary_key=True),
    Column('task_id', ForeignKey("task.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    hashed_password: Mapped[str] = mapped_column()
    email = mapped_column(String(255), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    username = mapped_column(String(255), default=None)
    is_confirmed: Mapped[bool] = mapped_column(default=False)

    projects: Mapped[list['Project']] = relationship(back_populates='members', secondary=users_to_projects)
    tasks: Mapped[list['Task']] = relationship(back_populates='members', secondary=users_to_tasks)


class Project(Base):
    __tablename__ = "project"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)

    tasks: Mapped[list['Task']] = relationship(back_populates='project')
    members: Mapped[list[User]] = relationship(back_populates='projects', secondary=users_to_projects)


class Task(Base):
    __tablename__ = "task"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    project_id: Mapped[UUID] = mapped_column(ForeignKey('project.id'))

    project: Mapped['Project'] = relationship(back_populates='tasks')
    members: Mapped[list[User]] = relationship(back_populates='tasks', secondary=users_to_tasks)
