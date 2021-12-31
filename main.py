#Python
from typing import Optional
from enum import Enum
#Pydantic
from pydantic import BaseModel, Field, EmailStr

#FastAPI
from fastapi import FastAPI, Body, Query, Path, Form, File, UploadFile, Header, Cookie, status, HTTPException




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


class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example='anibulus')
    message: str = Field(default='Login Successfully!')

#Path Operator  Decorator
@app.get(
    path='/', 
    status_code=status.HTTP_200_OK,
    tags=['Home'],
    summary='Home Request'
    ) #Home
def home():
    """Home Request

    Returns:
        Json: Example response of a path operation
    """
    return {"Hello":"World"}


#Request and response body
@app.post(
    path='/person/new', 
    response_model=PersonOut, 
    response_model_exclude={"age"},
    status_code=status.HTTP_201_CREATED,
    tags=['Person'],
    summary='Create person in the app'
    )
def create_person(person: Person = Body(...)): #Cuando se encuentra "= Body(...) quiere decir que es obligatorioem el Body"
    """ Crear Nueva Persona

    Args:
        person (**Person**, optional): Person Object. Defaults to Body(...).

    Returns:
        **PersonOut**: Person saved on the database
    """
    return person


@app.get(
    path='/person/details',
    status_code=status.HTTP_200_OK,
    tags=['Person'],
    summary='Request validation on Query Parameters'
    )
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
    """Validations to calll the path operation function

    Args:
        name (Optional[str], optional): The person's name. Defaults to Query( default=None, min_length=1, max_length=50, regex="^[A-z]*$", title="ID del usuario", description="El ID se consigue entrando a las configuraciones del perfil", example="Lalo lalito").
        age (int, optional): Age of the person. Defaults to Query( ..., ge=0, title='Age of the user', description='Age of the user').

    Returns:
        Json: A merge of name and age of the person
    """
    #[int]
    #ge : (greater or equal than ≥) Para especificar que el valor debe ser mayor o igual.
    #le : (less or equal than ≤) Para especificar que el valor debe ser menor o igual.
    #gt : (greater than >) Para especificar que el valor debe ser mayor.
    #lt : (less than <) Para especificar que el valor debe ser menor.
    
    return {name: age}

people = [1,2,3,4,5]

@app.get(
    path='/person/details/{person_id}',
    status_code=status.HTTP_200_OK,
    tags=['Person'],
    summary='Get Person'
)
def get_person(
    person_id: int = Path(
        ...,
        ge=0,
        title='Person ID',
        description= 'And ID value that references a person',
        example=1
        )
    ):
    """Get Person from a list

    Args:
        person_id (ID, optional): ID of the person. Defaults to Path( ..., ge=0, title='Person ID', description= 'And ID value that references a person', example=1 ).

    Raises:
        HTTPException: Exception if the person is not found

    Returns:
        Json: A message that says if the person was found
    """
    if person_id not in people:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='This person doesn\'t exist'
        )
    return {person_id: "It exists"}


#More than one body
@app.put(path='/person/{person_id}', tags=['Person'], summary='Update person')
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
    """Update person

    Args:
        person_id (ID, optional): Person's ID. Defaults to Path( ..., ge=1, title='Person id', description='Id of the person you want to update' ).
        person (Person, optional): Person Object. Defaults to Body(...).
        location (Location, optional): Location Object. Defaults to Body(...).

    Returns:
        Person: Object Person merged with Location object
    """
    result = dict(person)
    result.update(dict(location))
    return person

#Forms
@app.post(
    path='/login',
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=['Session'],
    summary='Login'
    )
def login(username: str = Form(...), password: str = Form(...)):
    """Login

    Args:
        username (str, optional): username of the user. Defaults to Form(...).
        password (str, optional): secret key of the user. Defaults to Form(...).

    Returns:
        LoginOut: Object safety for the return
    """
    return LoginOut(username=username)

@app.post(
    path='/contact',
    status_code=status.HTTP_200_OK,
    tags=['Contact'],
    summary='Contact'
    )
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        min_length=1,
        max_length=20
    ),
    email: EmailStr = Form(
        ...,
    ),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    """Contact data

    Args:
        first_name (str, optional): Name. Defaults to Form( ..., max_length=20, min_length=1 ).
        last_name (str, optional): Last name. Defaults to Form( ..., min_length=1, max_length=20 ).
        email (EmailStr, optional): Email. Defaults to Form( ..., ).
        message (str, optional): Message. Defaults to Form( ..., min_length=20 ).
        user_agent (Optional[str], optional): Header. Defaults to Header(default=None).
        ads (Optional[str], optional): Cookies. Defaults to Cookie(default=None).

    Returns:
        Tupla: Header and Coockies sended as content
    """
    return (user_agent, ads)

#File
@app.post(
    path='/post-image',
    tags=['Upload'],
    status_code=status.HTTP_200_OK,
    summary='Post image'
)
def post_image(
    image: UploadFile = File(...)
):
    """Post image

    Args:
        image (UploadFile, optional): File. Defaults to File(...).

    Returns:
        Json: Basic information of the file
    """
    return {
        'Filename': image.filename,
        'Format': image.content_type,
        'Size(kn)': round(len(image.file.read())/1024,ndigits=2)
    }