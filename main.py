#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel, Field

#FastAPI
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()

class HairColor(Enum):
    white= 'white'
    brown= 'brown'
    red= 'red'


class Location(BaseModel):
    pass

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=0,
        le=100
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = None

#Path Operator  Decorator
@app.get('/') #Home
def home():
    return {"Hello":"World"}

#Request and response body
@app.post('/person/new')
def create_person(person: Person = Body(...)): #Cuando se encuentra "= Body(...) quiere decir que es obligatorioem el Body"
    return person

@app.get('/person/details')
def get_person(
    name: Optional[str] = Query(
        default=None, 
        min_length=1, 
        max_length=50, 
        regex="^[A-z]*$", 
        title="ID del usuario", 
        description="El ID se consigue entrando a las configuraciones del perfil"),
    age: int = Query(
        ...,
        ge=0,
        title='Age of the user',
        description='Age of the user')
    ):
    #Cuando se encuentra Query(...) es un queryparameter obligatorio
    """
    [int]
    ge : (greater or equal than ≥) Para especificar que el valor debe ser mayor o igual.
    le : (less or equal than ≤) Para especificar que el valor debe ser menor o igual.
    gt : (greater than >) Para especificar que el valor debe ser mayor.
    lt : (less than <) Para especificar que el valor debe ser menor.
    """
    return {name: age}

@app.get('/person/details/{person_id}')
def get_person(
    person_id: int = Path(
        ...,
        ge=0,
        title='Person ID',
        description= 'And ID value that references a person'
        )
    ):
    return {person_id: "It exists"}

#More than one body
@app.put('/person/{person_id}')
def update_person(
    person_id: int = Path(
        ...,
        ge=1,
        title='Person id',
        description='Id of the person you want to update'
        ),
    person: Person = Body(...),
    location: Location = Body(...)
    ):
    result = dict(person)
    result.update(dict(location))
    return person