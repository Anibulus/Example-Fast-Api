#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel

#FastAPI
from fastapi import FastAPI, Body, Query, Path

app = FastAPI()

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
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