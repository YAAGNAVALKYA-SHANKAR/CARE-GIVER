from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from general.database import init_db
from routes import care_giver_routes,patient_routes,visit_routes
app=FastAPI()
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)
app.include_router(care_giver_routes.router,prefix="/Home-Care/Caregivers",tags=["Caregivers"])
app.include_router(patient_routes.router,prefix="/Home-Care/Patients",tags=["Patients"])
app.include_router(visit_routes.router,prefix="/Home-Care/Visitations",tags=["Visits"])
app.get("/")
def read_root():return {"message": "CORS enabled!"}
@app.on_event("startup")
async def startup():await init_db()