from fastapi import FastAPI, HTTPException
from classes import Request_User, Request_Pets, Request_Exams, Request_MedicineVaccine
from models import User, Pets, Exams, MedicineVaccine, session
from send import send_payload_user, send_payload_pets, send_payload_exams, send_payload_medicineVaccine
from receiver import send_db

import logging 
from logging.config import dictConfig
from log_config import log_config

dictConfig(log_config)

app = FastAPI()
logger = logging.getLogger('foo-logger')

@app.get("/")
async def root():
    return {
        "status":"Success",
        "data": "Welcome to the bestfriend API"
    }

@app.get("/users")
async def get_all_users():
    try:
        logger.info("Starting query for users")
        users_query  = session.query(User)
        users = users_query.all()

        if not users:
            raise HTTPException(status_code=404, detail="users not found")
        return {
            "STATUS": "success",
            "data": users
        }
    
    except Exception as e:
        logger.error(f"Is not possible to get Alunos: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed, try again")

@app.get("/pets")
async def get_all_pets():
    try:
        logger.info("Starting query for pets")
        pets_query  = session.query(Pets)
        pets = pets_query.all()

        if not pets:
            raise HTTPException(status_code=404, detail="pets not found")
        return {
            "STATUS": "success",
            "data": pets
        }
    
    except Exception as e:
        logger.error(f"Is not possible to get all pets: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed, try again")

@app.get("/users/{user_id}/pets/")
async def get_pets_by_owner(user_id: int):
    try:
        logger.info("starting query for pets per owner")
        query = session.query(Pets).filter(
            Pets.user_id == user_id
        )
        pet = query.first()
        if not pet:
            raise HTTPException(status_code=404, detail=f"pets of owner with id:{user_id} not found")
        return {
            "STATUS": "success",
            "data": pet
        }
    except Exception as e:
        logger.error(f"Is not possible to get pet: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed, {str(e)}")

@app.post("/users")
async def post_user(request_user: Request_User):
    try:
        logger.info("creating user")
        class_type = 'users'
        user_json = request_user

        user = {
            "name": user_json.name,
            "email": user_json.email,
            "password": user_json.password
        }

        send_payload_user(user)
        send_db(class_type)

        return{
            "status": 'success',
            "data": user_json
        }
    
    except Exception as e:
        logger.error(f"Is not possible to create user: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed, {str(e)}")

@app.post("/pets")
async def post_pet(request_pet: Request_Pets):
    try:
        logger.info("creating pet")
        class_type = 'pets'

        pet_json = request_pet

        pet = {
            "user_id": pet_json.user_id,
            "name": pet_json.name,
            "years_old": pet_json.years_old,
            "weight": pet_json.weight
        }

        send_payload_pets(pet)
        send_db(class_type)

        return{
            "status": 'success',
            "data": pet_json
        }
    
    except Exception as e:
        logger.error(f"Is not possible to create pet: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed, {str(e)}")

@app.post("/exams")
async def post_exams(request_exams: Request_Exams):
    try:
        logger.info("adding exams")
        class_type = 'exams'

        exams_json = request_exams

        exam = {
            "pet_id": exams_json.pet_id,
            "place": exams_json.place,
            "name_exam": exams_json.name_exam,
            "date": exams_json.date
        }

        send_payload_exams(exam)
        send_db(class_type)

        return{
            "status": 'success',
            "data": exams_json
        }
    
    except Exception as e:
        logger.error(f"Is not possible to add exam: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed, {str(e)}")

@app.put("/users/{user_id}")
async def modify_user(user_id: int, request_user: Request_User):
    try:
        class_type = 'users'
        user_json = request_user
        query = session.query(User).filter(
            User.id == user_id
        ).first()
        if not query:
            logger.error("User not found")
            raise HTTPException(status_code=404, detail="user not found")
        
        query.name: user_json.name
        query.email: user_json.email
        query.password: user_json.password
        
        session.add(query)
        session.commit()
        
        return {
			"status": "SUCESS",
			"data": user_json
		}
    except Exception as e:
        logger.error(f"Error upadating Aluno: {str(e)}")
        raise HTTPException(status_code=500, detail="Error upadating user")

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    
    user_query = session.query(User).filter(User.id == user_id).first()
    if not user_query:
        logger.error("User not found")
        raise HTTPException(status_code=404, detail="user not found")
    
    session.delete(user_query)    
    session.commit()


"""
@app.get("users/pets/medicines-vaccines")

@app.post("/medicines-vaccines")

@app.put("/pets/{pet_id}")
@app.put("/exams/{exam_id}")
@app.put("/medicines-vaccines/{protocol_id}")

@app.delete("/pets/{pet_id}")
@app.delete("/exams/{exam_id}")
@app.delete("/medicines-vaccines/{protocol_id}")
"""
