from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from general.database import init_db
from routes import care_giver_routes,patient_routes,visit_routes,login_routes,nursing_routes
app=FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Home-Care API",
        version="1.0.0",
        description="API docs with JWT Auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)
app.include_router(care_giver_routes.router,prefix="/Home-Care/Caregivers",tags=["Caregivers"])
app.include_router(patient_routes.router,prefix="/Home-Care/Patients",tags=["Patients"])
app.include_router(visit_routes.router,prefix="/Home-Care/Visitations",tags=["Visits"])
app.include_router(login_routes.router,prefix="/Home-Care/Login",tags=["Login"])
app.include_router(nursing_routes.router,prefix="/Home-Care/Nursing",tags=["Nursing"])
app.get("/")
def read_root():return {"message": "CORS enabled!"}
@app.on_event("startup")
async def startup():await init_db()