import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
load_dotenv()

"""
This module handles the connection to the MongoDB database and initializes the necessary collections.
It also creates indexes for unique fields in the collections.
"""

MONGO_URI=os.getenv("MONGO_URI")
DATABASE=os.getenv("DATABASE")
CAREGIVER_MASTERTABLE=os.getenv("CAREGIVER_MASTER")
PATIENTS_MASTERTABLE=os.getenv("PATIENT_MASTER")
VISITATION_RECORDS=os.getenv("VISITATIONS")
DOCTOR_ESCALATIONS=os.getenv("ESCALATIONS")
VITAL_READINGS=os.getenv("VITALS_READING")
LOGS=os.getenv("LOGS")
USERS=os.getenv("USERS")
NURSING=os.getenv("NURSING_CARE")
client=AsyncIOMotorClient(MONGO_URI)
db=client[DATABASE]
caregivers=db[CAREGIVER_MASTERTABLE]
patients=db[PATIENTS_MASTERTABLE]
visitations=db[VISITATION_RECORDS]
escalations=db[DOCTOR_ESCALATIONS]
vitals=db[VITAL_READINGS]
logs=db[LOGS]
registered_users=db[USERS]
nursing=db[NURSING]
async def init_db():
    existing_collections=await db.list_collection_names()
    async def create_collection(collection_name):
        """
        Create a collection if it doesn't exist.
        """
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
    await create_collection(NURSING)

    """
    Create indexes for unique fields.
    """
    await caregivers.create_index([("caregiver_id",ASCENDING)],unique=True)
    await patients.create_index([("patient_id",ASCENDING)],unique=True)
    await visitations.create_index([("visit_id",ASCENDING)],unique=True)
    await escalations.create_index([("escalation_id",ASCENDING)],unique=True)
    await vitals.create_index([("vitals_id",ASCENDING)],unique=True)
    await logs.create_index([("transaction_id",ASCENDING)],unique=True)
    await registered_users.create_index([("email",ASCENDING)],unique=True)