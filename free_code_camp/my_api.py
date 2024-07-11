from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {
        "name" : "Haroon",
        "age" : 20,
        "year" : "5"
        },
}

class student(BaseModel):
    name: str
    age: int
    year: int

class updateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[int] = None

# Path Parameter
@app.get('/')
def index():
    return { 'hello': 'world' } 

@app.get("/get_students/{student_ID}")
def get_students(student_ID: int = Path(..., description="The ID of the student you want to get")):
    return students[student_ID] 

# Query Parameter
@app.get("/get-by-name")
def get_student(*, name : Optional[str] = None, test : int):
    for id in students:
        if students[id]["name"] == name:
            return students[id]
    return { "error" : "Student not found" }

# Combining path and Query Parameter
@app.get("/get-by-name/{student_ID}")
def get_student(*,student_ID : int,  name : Optional[str] = None, test : int):
    for id in students:
        if students[id]["name"] == name:
            return students[id]
    return { "error" : "Student not found" }

# POST Method
@app.post("/create-student/{student_ID}")
def create_student(student_ID: int, student: student):
    if student_ID in students:
        return { "Error" : "Student already exists" }
    students[student_ID] = student
    return students[student_ID] 

# PUT Method
@app.put("/update-student/{student_ID}")
def update_student(student_ID: int, student: updateStudent):
    if student_ID not in students:
        return { "Error" : "Student does not exist" }
    if student.name != None:
        students[student_ID].name = student.name
    if student.age != None:
        students[student_ID].age = student.age
    if student.year != None:
        students[student_ID].year = student.year
    return students[student_ID]

# DELETE Method
@app.delete("/delete-student/{student_ID}")
def delete_student(student_ID: int):
    if student_ID not in students:
        return { "Error" : "Student does not exist" }
    del students[student_ID]
    return { "Message" : "Student deleted successfully" }