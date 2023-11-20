from pydantic import BaseModel

class Request_User(BaseModel):
    id: int
    name: str
    email: str
    password: str

class Request_Pets(BaseModel):
    id: int
    user_id: int
    name: str
    years_old: str 
    weight: str

class Request_Exams(BaseModel):
    id: int
    pet_id: int
    place: str
    name_exam: str
    date: str

class Request_MedicineVaccine(BaseModel):
    id: int
    pet_id: int
    type_of: str
    name: str
    date: str
