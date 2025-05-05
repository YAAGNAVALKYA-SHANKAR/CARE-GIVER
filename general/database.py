import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
load_dotenv()
MONGO_URI=os.getenv("MONGO_URI")
DATABASE=os.getenv("DATABASE")
CAREGIVER_MASTERTABLE=os.getenv("CAREGIVER_MASTER")
PATIENTS_MASTERTABLE=os.getenv("PATIENT_MASTER")
VISITATION_RECORDS=os.getenv("VISITATIONS")
DOCTOR_ESCALATIONS=os.getenv("ESCALATIONS")
VITAL_READINGS=os.getenv("VITALS_READING")
LOGS=os.getenv("LOGS")
USERS=os.getenv("USERS")
client=AsyncIOMotorClient(MONGO_URI)
db=client[DATABASE]
caregivers=db[CAREGIVER_MASTERTABLE]
patients=db[PATIENTS_MASTERTABLE]
visitations=db[VISITATION_RECORDS]
escalations=db[DOCTOR_ESCALATIONS]
vitals=db[VITAL_READINGS]
logs=db[LOGS]
users=db[USERS]
async def init_db():
    existing_collections=await db.list_collection_names()
    async def create_collection(collection_name):
        if collection_name not in existing_collections:
            await db.create_collection(collection_name)
            await db[collection_name].insert_one({"function":"ID_counter","count":1})
    await create_collection(CAREGIVER_MASTERTABLE)
    await create_collection(PATIENTS_MASTERTABLE)
    await create_collection(VISITATION_RECORDS)
    await create_collection(DOCTOR_ESCALATIONS)
    await create_collection(VITAL_READINGS)
    await create_collection(LOGS)
    await create_collection(USERS)
    await caregivers.create_index([("caregiver_id",ASCENDING)],unique=True)
    await patients.create_index([("patient_id",ASCENDING)],unique=True)
    await visitations.create_index([("visit_id",ASCENDING)],unique=True)
    await escalations.create_index([("escalation_id",ASCENDING)],unique=True)
    await vitals.create_index([("vitals_id",ASCENDING)],unique=True)
    await logs.create_index([("transaction_id",ASCENDING)],unique=True)
    await users.create_index([("user_id",ASCENDING)],unique=True)