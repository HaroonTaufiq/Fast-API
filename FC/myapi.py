# install Fast API
# python -m pip install fastapi

# run file on the web Server
# pip install uvicorn 

# Import 
# import fastapi

# create an instance of fast API
from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel  # for body parameters (POST)

# GET - Get info
# POST - Create info
# PUT - Update info
# DELETE - Delete info

# variable app = instance of FastAPI
app = FastAPI()

Students = {
    1: {
        'name': 'John',
        'age': 17,
        'class': 'year 12'
    },
    2: {
        'name': 'Jane',
        'age': 18,
        'class': 'year 13'
    }
}

class Student(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

# Path parameters (in URL)
@app.get('/get-student/{student_id}')
def get_student(student_id: int = Path(..., description='The ID of the student you want to view', gt=0)): 
    return Students[student_id]

# gt - greater than
# lt - less than
# gte - greater than or equal to
# lte - less than or equal to

# Query parameters (in function)
@app.get('/get-by-name')
def get_student(*,name: Optional[str] = None, test: int):   # = None for not required and also do Optional to it
    for student_id in Students:
        if Students[student_id]['name'] == name:
            return Students[student_id]
    return {'Data': 'Not found'}

# both query and path params
@app.get('/get-by-name/{student_id}')
def get_student(*,student_id: int,name: Optional[str] = None, test: int):   # = None for not required and also do Optional to it
    for student_id in Students:
        if Students[student_id]['name'] == name:
            return Students[student_id]
    return {'Data': 'Not found'}

# create a route = new api
@app.get('/')
def index():
    return {'data': {'name': 'John'}}

# to run the file
# uvicorn myapi:app --reload  # myapi = file name, app = variable name

# got to /docs to see the api documentation

@app.post('/create-student/{student_id}')
def create_student(student_id: int, student: Student):
    if student_id in Students:
        return {'Error': 'Student exists'}
    
    Students[student_id] = student.dict()
    return Students[student_id]

@app.put('/update-student/{student_id}')
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in Students:
        return {'Error': "Student doesn't exist."}
        
    if student.name is not None:
        Students[student_id]['name'] = student.name
    if student.age is not None:
        Students[student_id]['age'] = student.age
    if student.year is not None:
        Students[student_id]['class'] = student.year

    return Students[student_id]

@app.delete('/delete-student/{student_id}')
def delete_student(student_id: int):
    if student_id not in Students:
        return {'Error': "Student doesn't exist."}

    del Students[student_id]
    return {'Message': 'Student deleted successfully'}