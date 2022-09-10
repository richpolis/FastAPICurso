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
    status_code=status.HTTP_200_OK
)
def home():
    return {"Hello": "World"}


# Request and response body
@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
)
def create_person(person: Person = Body(...)):
    return person


# Validaciones: Query Parameters 
@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK
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
    return {'name': name, 'age': age}


# Validaciones: Path Parameters

persons_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_202_ACCEPTED
)
def show_person(
        person_id: int = Path(..., gt=0, example=127)
):
    if person_id not in persons_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesn't exists"
        )

    return {person_id: "It exists!"}


# Validaciones: Request Body 
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_202_ACCEPTED
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
    # results = person.dict()
    # results.update(location.dict())
    # return results
    return person


# Forms
# Login 
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)


# Cookies and Headers Parameters
@app.post(
    path="/contact",
    status_code=status.HTTP_201_CREATED
)
def contact(
        first_name: str = Form(..., max_length=50, min_length=1),
        last_name: str = Form(..., max_length=50, min_length=1),
        email: EmailStr = Form(..., ),
        message: str = Form(..., min_length=20),
        user_agent: Optional[str] = Header(default=None),
        ads: Optional[str] = Cookie(default=None)
):
    return user_agent


# Files

@app.post(
    path="/post-image"
)
def post_image(image: UploadFile = File(...)):
    return {
        "filename": image.filename,
        "format": image.content_type,
        "size(kb)": round(len(image.file.read()) / 1024, ndigits=2)
    }
