# Домашнее задание по теме "Модели данных Pydantic"
# Цель: научиться описывать и использовать Pydantic модель

from fastapi import FastAPI, Path, status, Body, HTTPException
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get("/users")
async def get_all_list():
    return users


@app.post("/user/{username}/{age}")
async def create_user(
        username: Annotated[str, Path(min_length=5, max_length=20, description="Введите имя пользователя")],
        age: Annotated[int, Path(ge=18, le=120, description="Введите возраст")]):
    if not users:  # Если список users пустой
        user_id = 1
    else:
        user_id = users[-1].id + 1  # Увеличиваем ID последнего пользователя на 1,
        # индекс -1 означает обращение к последнему элементу этого списка
    user = User(id=user_id, username=username, age=age)
    users.append(user)  # Добавляем нового пользователя в список users
    return user  # Возвращаем созданного пользователя


@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
        user_id: Annotated[int, Path()],
        username: Annotated[str, Path(min_length=5, max_length=20, description="Введите имя пользователя")],
        age: Annotated[int, Path(ge=18, le=120, description="Введите возраст")]):
    for user in users:  # перебираем список users
        if user.id == user_id:
            user.username = username
            user.age = age
            return user  # Возвращаем обновленного пользователя
    raise HTTPException(status_code=404, detail="User was not found")  # Если пользователя нет, выбрасываем исключение


@app.delete("/user/{user_id}")
async def delete_user(user_id: Annotated[int, Path()]):
    for ind, user in enumerate(users):  # проходим по каждому элементу списка users и возвращаем пару:
        # индекс как номер текущего элемента в списке и user как сам элемент списка (в нашем случае объект User)
        if user.id == user_id:
            deleted_user = users.pop(ind)
            return deleted_user
            # del users[ind]  # Удаляем пользователя из списка users
            # return f"Пользователь {user_id} был удален"  # Возвращаем сообщение об удалении
    raise HTTPException(status_code=404, detail="User was not found")  # Если пользователя нет, выбрасываем исключение
