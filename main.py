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
    black= 'black'
    brown= 'brown'
    red= 'red'


class Location(BaseModel):
    city: str
    state: str
    country: str

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        #example='Luis'
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

    class Config:
        schema_extra={
            "example":{ #Tiene que tener el nombre example (convención) para aparecer en la documentacion
                "first_name": "Luis",
                "last_name": "Preza",
                "age": 22,
                "hair_color": "black",
                "is_married": True
            }
        }

class Person(PersonBase):
    password: str = Field(
        ...,
        min_length=8
    )

class PersonOut(PersonBase):
    pass

#Path Operator  Decorator
@app.get('/') #Home
def home():
    return {"Hello":"World"}

#Request and response body
@app.post('/person/new', response_model=PersonOut, response_model_exclude={"age"})
def create_person(person: Person = Body(...)): #Cuando se encuentra "= Body(...) quiere decir que es obligatorioem el Body"
    return person

@app.get('/person/details')
def list_person(
    name: Optional[str] = Query(
        default=None, 
        min_length=1, 
        max_length=50, 
        regex="^[A-z]*$", 
        title="ID del usuario", 
        description="El ID se consigue entrando a las configuraciones del perfil",
        example="Lalo lalito"),
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
        description= 'And ID value that references a person',
        example=1
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