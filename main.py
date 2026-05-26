from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, field_validator
from typing import List

app = FastAPI()


HTML_CONTENT = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Пример страницы html</title>
</head>
<body>
    —
</body>
</html>"""


feedbacks: List[dict] = []


class User(BaseModel):
    name: str
    id: int

class UserAge(BaseModel):
    name: str
    age: int

class Feedback(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    message: str = Field(..., min_length=10, max_length=500)

    @field_validator('message', mode='before')
    @classmethod
    def check_forbidden_words(cls, v: str) -> str:
        forbidden = ['кринж', 'рофл', 'вайб']
        for word in forbidden:
            if word in v.lower():
                raise ValueError('Использование недопустимых слов')
        return v

@app.get("/")
def root():
    return {"message": "Добро пожаловать в моё приложение FastAPI!"}

@app.get("/page")
def html_page():
    return HTMLResponse(content=HTML_CONTENT, status_code=200)

@app.post("/calculate")
def calculate(num1: float, num2: float):
    return {"result": num1 + num2}

@app.get("/users")
def get_user():
    return User(name="Ваше Имя и Фамилия", id=1).model_dump()

@app.post("/user")
def check_adult(user: UserAge):
    data = user.model_dump()
    data["is_adult"] = user.age >= 18
    return data

@app.post("/feedback")
def submit_feedback(fb: Feedback):
    feedbacks.append(fb.model_dump())
    return {"message": f"Спасибо, {fb.name}! Ваш отзыв сохранён."}
