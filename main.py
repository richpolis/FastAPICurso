# Python
from enum import Enum
from lib2to3.pgen2.token import TILDE
from typing import Optional

# Pydantic
from pydantic import BaseModel, Field 

# FastAPI 
from fastapi import FastAPI 
from fastapi import Body, Query, Path

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


class Person(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., gt=0, le=115)
    hair_color: Optional[HairColors] = Field(default=None) 
    is_married: Optional[bool] = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Facundo", 
                "last_name": "García Martoni", 
                "age": 21, 
                "hair_color": "blonde", 
                "is_married": False
            }
        }



@app.get("/")
def home():
    return {"Hello": "World"}


# Request and response body
@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person


# Validaciones: Query Parameters 
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
            None, min_length=1, max_length=50, 
            title="This is the person name. It's between 1 and 50 characters"
        ), 
    age: str = Query(
            ...,
            title="This is the person age. It's required"
        )
    ):
    return {'name': name, 'age': age}


# Validaciones: Path Parameters 
@app.get("/person/detail/{person_id}")
def show_person(
        person_id: int = Path(..., gt=0)
    ):
    return { person_id: "It exists!" }


# Validaciones: Request Body 
@app.put("/person/{person_id}")
def update_person(
        person_id: int = Path(
            ...,
            title="Person ID", 
            description="This is the person ID", 
            gt=0 
            ),
        person: Person = Body(...), 
        # location: Location = Body(...)
    ):
    
    #results = person.dict()
    #results.update(location.dict())
    #return results
    return person