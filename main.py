# venv\scripts\activate
# pip install fastapi[all]
# python.exe -m pip install --upgrade pip
# requirements.txt
# uvicorn main:app --reload


from enum import Enum
#import uuid
from fastapi import FastAPI, Body,HTTPException# status
#from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class DogType(str, Enum):
    bulldog = "bulldog"
    terrier = "terrier"
    dalmatian = "dalmatian"

class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType

class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}



post_db = [
    Timestamp(id=0, timestamp=1.0),
    Timestamp(id=1, timestamp=2.0)
]


# 2. Реализован путь / – 1 балл
@app.get('/')
def root():
    return "Привет пользователь"


# 3. Реализован путь /post – 1 балла
@app.post('/post', response_model = Timestamp, summary='Get Post')
def post_add(data = Body()):
    timestamp_n = Timestamp(id = data["id"],
                            timestamp = data["timestamp"])
    return timestamp_n


# 4. Реализована запись собак – 1 балл
@app.post("/dog", summary='Create Dog')
def create_dog(data = Body()):
    if dogs_db.get(data["pk"]) is not None:
        raise HTTPException(status_code=409,
                            detail='The specified PK already exists.')
    else:
        new_dog = Dog(name = data["name"],
                      pk = len(dogs_db),
                      kind = data['kind'])
        dogs_db[len(dogs_db)] = new_dog
    return new_dog#, dogs_db


# 5. Реализовано получение списка собак – 1 балл
@app.get('/dog', summary='Get Dogs')
async def get_dogs_list():
    return dogs_db


# 6. Реализовано получение собаки по id – 1 балл
@app.get('/dog/{pk}', summary='Get Dog By Pk')
async def get_dogs_pk(pk: int):
    lr = []
    for dog in dogs_db.values():
        if dog.__dict__['pk'] == pk:
            lr.append(dog.__dict__)
    return lr


# 7. Реализовано получение собак по типу – 1 балл
@app.get('/dog_kind/{i}', summary='Get Dog By Kind')
async def get_dogs_kind(i: str):
    lr = []
    for dog in dogs_db.values():
        if dog.__dict__['kind'] == i:
            lr.append(dog.__dict__)
    return lr


# 8. Реализовано обновление собаки по id – 1 балл
@app.patch('/dog/{pk}', summary='Update Dog')
async def update_dog(pk: int, dog: Dog):
    if pk in dogs_db:
        dogs_db[pk] = dog
        return {"message": "Dog updated successfully"}, dogs_db
    else:
        return {"message": "Dog not found"}, dogs_db