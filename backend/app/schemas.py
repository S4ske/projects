from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class UserBase(BaseModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    username: str | None = Field(default=None, max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(BaseModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    username: str | None = Field(default=None, max_length=255)


class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(BaseModel):
    username: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UserPublic(UserBase):
    id: UUID

    class Config:
        orm_mode = True


class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int


class UserInDB(UserBase):
    id: UUID
    hashes_password: str

    class Config:
        orm_mode = True


class ProjectBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)


class ProjectPublic(ProjectBase):
    id: UUID


class ProjectsPublic(BaseModel):
    data: list[ProjectPublic]
    count: int


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)


class TaskPublic(TaskBase):
    id: UUID


class TasksPublic(BaseModel):
    data: list[ProjectPublic]
    count: int


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str | None = None


class UpdatePassword(BaseModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


class NewPassword(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
