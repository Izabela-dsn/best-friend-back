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



# @app.get("users/pets/medicines-vaccines")

@app.get("users/pets/medicines-vaccines")
async def get_medicines_vaccines_for_all_pets():
    try:
        logger.info("starting query for medicines and vaccines for all pets")
        medicines_vaccines_query = session.query(MedicineVaccine)
        medicines_vaccines = medicines_vaccines_query.all()

        if not medicines_vaccines:
            raise HTTPException(status_code=404, detail="Medicines and vaccines not found")
        
        return {
            "STATUS": "success",
            "data": medicines_vaccines
        }
    
    except Exception as e:
        logger.error(f"Is not possible to get medicines and vaccines: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed, {str(e)}")


# @app.post("/medicines-vaccines")
@app.post("/medicines-vaccines")
async def post_medicine_vaccine(request_medicine_vaccine: Request_MedicineVaccine):
    try:
        logger.info("Creating medicine or vaccine")
        class_type = 'medVacc'
        medicine_vaccine_json = request_medicine_vaccine

        medicine_vaccine = {
            "type_of": medicine_vaccine_json.type_of,
            "name": medicine_vaccine_json.name,
            "date": medicine_vaccine_json.date,
            "pet_id": medicine_vaccine_json.pet_id
        }

        send_payload_medicineVaccine(medicine_vaccine)
        send_db(class_type)

        return {
            "status": 'success',
            "data": medicine_vaccine_json
        }
    
    except Exception as e:
        logger.error(f"Failed to create medicine or vaccine: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed, {str(e)}")


# @app.put("/pets/{pet_id}")
@app.put("/pets/{pet_id}")
async def update_pet(pet_id: int, request_pet: Request_Pets):
    try:
        logger.info(f"Updating pet with ID: {pet_id}")
        class_type = 'pets'
        pet_json = request_pet

        pet = {
            "user_id": pet_json.user_id,
            "name": pet_json.name,
            "years_old": pet_json.years_old,
            "weight": pet_json.weight
        }

        
        pet = session.query(Pets).filter(Pets.id == pet_id).first()    #query
        if not pet:  #query
            logger.error("Pet not found")
            raise HTTPException(status_code=404, detail=f"Pet with ID {pet_id} not found")

        pet.owner_id = pet_json.user_id
        pet.name = pet_json.name
        pet.years = pet_json.years_old
        pet.weight = pet_json.weight

        session.add(pet)
        session.commit()
 
        
        return {
            "status": 'success',
            "data": pet_json
        }
    
    except Exception as e:
        logger.error(f"Failed to update pet: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to updating, {str(e)}")
        

# @app.put("/exams/{exam_id}")
@app.put("/exams/{exam_id}")
async def update_exam(exam_id: int, request_exam: Request_Exams):
    try:
        logger.info(f"Updating exam with ID: {exam_id}")
        class_type = 'exams'
        exam_json = request_exam

        exam = {
            "pet_id": exam_json.pet_id,
            "place": exam_json.place,
            "name_exam": exam_json.name_exam,
            "date": exam_json.date
        }


        exam = session.query(Exams).filter(Exams.id == exam_id).first()
        if not exam:
            logger.error("Exam not found")
            raise HTTPException(status_code=404, detail=f"Exam with ID {exam_id} not found")

        exam.place = exam_json.place
        exam.name_exam = exam_json.name_exam
        exam.date = exam_json.date

        session.add(Exams)
        session.commit()

        return {
            "status": 'success',
            "data": exam_json
        }
    
    except Exception as e:
        logger.error(f"Failed to update exam: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed, {str(e)}")
        

@app.put("/medicines-vaccines/{medicine_vaccine_id}")
async def update_medicine_vaccine(medicine_vaccine_id: int, request_medicine_vaccine: Request_MedicineVaccine):
    try:
        logger.info(f"Updating medicine or vaccine with ID: {medicine_vaccine_id}")
        class_type = 'medicine-vaccine'
        medicine_vaccine_json = request_medicine_vaccine

        medicine_vaccine = {
            "type_of": medicine_vaccine_json.type_of,
            "name": medicine_vaccine_json.name,
            "date": medicine_vaccine_json.date,
            "pet_id": medicine_vaccine_json.pet_id
        }

        medicine_vaccine = session.query(medicine_vaccine)
        medicine_vaccine = session.query(medicine_vaccine).filter(Exams.id == medicine_vaccine_id).first()
        if not medicine_vaccine:
            logger.error("medicine or vaccine not found")
            raise HTTPException(status_code=404, detail=f"medicine or vaccine {medicine_vaccine_id} not found")

        medicine_vaccine.place = medicine_vaccine_json.place
        medicine_vaccine.name_exam = medicine_vaccine_json.name_exam
        medicine_vaccine.date = medicine_vaccine_json.date

        session.add(medicine_vaccine)
        session.commit()

        return {
            "status": 'success',
            "data": medicine_vaccine_json
        }
    
    except Exception as e:
        logger.error(f"Failed to update medicine or vaccine: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed, {str(e)}")


# @app.delete("/pets/{pet_id}")
@app.delete("/pets/{pet_id}")
async def delete_pet(pet_id: int):
    try:
        logger.info(f"Deleting pet with ID: {pet_id}")
        class_type = 'pets'

        pet_query = session.query(delete_pet).filter(User.id == pet_id).first()
        if not pet_query:
            logger.error("Pet not found")
            raise HTTPException(status_code=404, detail="pet not found")
              
        session.delete(pet_id)    
        session.commit()

        return {
            "status": 'success',
            "data": f"Pet with ID {pet_id} deleted successfully"
        }
    
    except Exception as e:
        logger.error(f"Failed to delete pet: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed, {str(e)}")


# @app.delete("/exams/{exam_id}")
@app.delete("/exams/{exam_id}")
async def delete_exam(exam_id: int):
    try:
        logger.info(f"Deleting exam with ID: {exam_id}")
        class_type = 'exams'

        exam_query = session.query(delete_exam).filter(Exams.id == exam_id).first()
        if not exam_query:
            logger.error("Exam not found")
            raise HTTPException(status_code=404, detail="exam not found")
              
        session.delete(exam_id)    
        session.commit()

        return {
            "status": 'success',
            "data": f"Exam with ID {exam_id} deleted successfully"
        }
    
    except Exception as e:
        logger.error(f"Failed to delete exam: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed, {str(e)}")
    

# @app.delete("/medicines-vaccines/{protocol_id}")
@app.delete("/medicines-vaccines/{medicine_vaccine_id}")
async def delete_medicine_vaccine(medicine_vaccine_id: int):
    try:
        logger.info(f"Deleting medicine or vaccine with ID: {medicine_vaccine_id}")
        class_type = 'medicine-vaccine'

        medicine_vaccine_query = session.query(delete_medicine_vaccine).filter(delete_medicine_vaccine.id == medicine_vaccine_id).first() ##
        if not medicine_vaccine_query:
            logger.error("Exam not found")
            raise HTTPException(status_code=404, detail="exam not found")
              
        session.delete(medicine_vaccine_id)    
        session.commit()

        return {
            "status": 'success',
            "data": f"Medicine or vaccine with ID {medicine_vaccine_id} deleted successfully"
        }
    
    except Exception as e:
        logger.error(f"Failed to delete medicine or vaccine: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed, {str(e)}")

