# venv\scripts\activate
# pip install fastapi[all]
# python.exe -m pip install --upgrade pip
# requirements.txt
# uvicorn main:app --reload


from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datetime




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

dog_list = [dog_type.value for dog_type in DogType]


'''
Важное упущение: структура dogs_db это словарь, где значением является объект класса Dog.
В свою очередь принимаем, что ключ в словаре dogs_db и значение pk из класса должны совпадать.
'''

# 2. Реализован путь / – 1 балл
@app.get('/')
def root():
    return "Привет пользователь"


# 3. Реализован путь /post – 1 балла
@app.post('/post', response_model = Timestamp, summary='Get Post')
def post_add():
    current_time_utc = datetime.datetime.utcnow()
    moscow_offset = datetime.timedelta(hours=3)
    current_time_moscow = current_time_utc + moscow_offset
    ts_cur = int(current_time_moscow.timestamp())
    timestamp_n = Timestamp(id = post_db[-1].id + 1, timestamp = ts_cur)
    return timestamp_n


# 4. Реализована запись собак – 1 балл
@app.post("/dog", response_model=Dog, summary='Create Dog')
def create_dog(dog: Dog):
    if dogs_db.get(dog.pk) is not None:
        raise HTTPException(status_code=409,
                            detail='The specified PK already exists.')
    else:
        new_dog = dog
        dogs_db[dog.pk] = new_dog
    return new_dog



# 5. Реализовано получение списка собак – 1 балл
@app.get('/dog', summary='Get Dogs')
async def get_dogs_list():
    return dogs_db


# 6. Реализовано получение собаки по id – 1 балл
@app.get('/dog/{pk}', response_model=Dog, summary='Get Dog By Pk')
async def get_dogs_pk(pk: int):
    if dogs_db.get(pk) is None:
        raise HTTPException(status_code=409,
                            detail='The specified PK not exists.')
    else:
        return dogs_db.get(pk)


# 7. Реализовано получение собак по типу – 1 балл
@app.get('/dog_kind/{i}', response_model=list[Dog], summary='Get Dog By Kind')
async def get_dogs_kind(i: str):
    list_kind_dog = []
    if i in dog_list:
        for dog in dogs_db.keys():
            if dogs_db[dog].kind == i:
                list_kind_dog.append(dogs_db[dog])
        return list_kind_dog
    else:
        raise HTTPException(status_code=409,
                            detail='The kind of dog not found.')



# 8. Реализовано обновление собаки по id – 1 балл
@app.patch('/dog/{pk}', summary='Update Dog')
async def update_dog(pk: int, dog: Dog):
    if pk in dogs_db:
        dogs_db[pk] = dog
        return dogs_db[pk]
    else:
        raise HTTPException(status_code=409,
                            detail='The specified PK already exists.')