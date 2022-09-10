# Python
from enum import Enum
from typing import Optional

# FastAPI
from fastapi import (
    FastAPI, status, HTTPException,
    Body, Query, Path, Form, Cookie, Header, UploadFile, File
)
# Pydantic
from pydantic import (
    BaseModel, Field, EmailStr
)

app = FastAPI()


# Models 
class HairColors(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blonde = 'blonde'
    red = 'red'


class Location(BaseModel):
    city: str
    state: str
    country: str


class PersonBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, example="Facundo")
    last_name: str = Field(..., min_length=1, max_length=50, example="García Martoni")
    age: int = Field(..., gt=0, le=115, example=21)
    hair_color: Optional[HairColors] = Field(default=None, example="blonde")
    is_married: Optional[bool] = Field(default=None, example=False)


class Person(PersonBase):
    password: str = Field(..., min_length=8, example="Patito$123")

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Facundo", 
    #             "last_name": "García Martoni", 
    #             "age": 21, 
    #             "hair_color": "blonde", 
    #             "is_married": False
    #         }
    #     }


class PersonOut(PersonBase):
    pass


class LoginOut(BaseModel):
    username: str = Field(..., max_length=150, example="facundo_21")
    message: str = Field(default='Login successfully!')


@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=["home"]
)
def home():
    """
    Home.

    Welcome app.

    Paramters:
    - Nothing.

    Returns hello world.
    """
    return {"Hello": "World"}


# Request and response body
@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["persons"],
    summary="Create a person in the app"
)
def create_person(person: Person = Body(...)):
    """
    Create Person.

    This path operation creates a person in the app and save the information in the database.

    Paramters:
    - Request body paramters:
        - **person: Person** -> A person model with first name, last name, age, hair color and marital status.

    Returns a person model with first name, last name, age, hair color and marital status.
    """
    return person


# Validaciones: Query Parameters 
@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["persons"],
    summary="Show person's detail",
    deprecated=True
)
def show_person(
        name: Optional[str] = Query(
            None, min_length=1, max_length=50,
            title="This is the person name. It's between 1 and 50 characters",
            example="Rocio"
        ),
        age: str = Query(
            ...,
            title="This is the person age. It's required",
            example=27
        )
):
    """
    Show detail person.

    This path operation show detail person from database.

    Paramters:
    - **name: str** -> Person name.
    - **age: int** -> Person age.

    Returns a person name and age.
    """
    return {'name': name, 'age': age}


# Validaciones: Path Parameters

persons_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["persons"],
    summary="Show person's details"
)
def show_person(
        person_id: int = Path(..., gt=0, example=127)
):
    """
    Show detail person.

    This path operation show detail person from database.

    Paramters:
    - **person_id: int** -> Person ID.

    Returns if person ID exists.
    """
    if person_id not in persons_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesn't exists"
        )

    return {person_id: "It exists!"}


# Validaciones: Request Body 
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["persons"],
    summary="Update a person in the app"
)
def update_person(
        person_id: int = Path(
            ...,
            title="Person ID",
            description="This is the person ID",
            gt=0,
            example=127
        ),
        person: Person = Body(...),
        # location: Location = Body(...)
):
    """
    Update person.

    This path operation update a person and save information in the database.

    Paramters:
    - **person_id: int** -> Person ID.
    - Request body paramters:
        - **person: Person** -> A person model with first name, last name, age, hair color and marital status.

    Returns a person model with first name, last name, age, hair color and marital status updated.
    """
    # results = person.dict()
    # results.update(location.dict())
    # return results
    return person


# Forms
# Login 
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["auth"],
    summary="Authetification the person in the app"
)
def login(username: str = Form(...), password: str = Form(...)):
    """
    Login.

    This path operation do login in the system.

    Paramters:
    - **username: str** -> Username.
    - **password: str** -> Password.

    Returns username if user exists.
    """
    return LoginOut(username=username)


# Cookies and Headers Parameters
@app.post(
    path="/contact",
    status_code=status.HTTP_201_CREATED,
    tags=["contacts"],
    summary="Create a contact in the app"
)
def contact(
        first_name: str = Form(..., max_length=50, min_length=1),
        last_name: str = Form(..., max_length=50, min_length=1),
        email: EmailStr = Form(..., ),
        message: str = Form(..., min_length=20),
        user_agent: Optional[str] = Header(default=None),
        ads: Optional[str] = Cookie(default=None)
):
    """
    Register contact.

    This path operation register a contact and save information in the database.

    Paramters:
    - **first_name: str** -> Contact first name.
    - **last_name: str** -> Contact last name.
    - **email: EmailStr** -> Contact email.
    - **message: Text** -> Contact message.
    - Optional:
        - **user_agent: str** -> Contact user agent.
        - **ads: str** -> Contact ads.

    Returns user_agent from origin.
    """
    return user_agent


# Files

@app.post(
    path="/post-image",
    status_code=status.HTTP_200_OK,
    tags=["files"],
    summary="Upload file in the app"
)
def post_image(image: UploadFile = File(...)):
    """
    Upload image.

    This path operation upload file and save in the storage files.

    Paramters:
    - Request form paramters:
        - **image: File** -> file to upload.

    Returns info from image o file upload.
    """
    return {
        "filename": image.filename,
        "format": image.content_type,
        "size(kb)": round(len(image.file.read()) / 1024, ndigits=2)
    }
