from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from general.database import init_db
from routes import care_giver_routes,patient_routes,visit_routes,login_routes,escalation_routes,general_routes
app=FastAPI()

"""
This module initializes the FastAPI application and includes the following components:
- Middleware: CORS middleware to allow cross-origin requests.
- OpenAPI: Custom OpenAPI schema to include JWT authentication.
- Routers: Includes routers for different modules such as Caregivers, Patients, Visitations, Login, and Nursing.
"""

def custom_openapi():
    """
    Custom OpenAPI schema to include JWT authentication.
    :return: The OpenAPI schema with JWT authentication.
    """
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

"""
Include routers for different modules.
"""
app.include_router(care_giver_routes.router,prefix="/Home-Care/Caregivers",tags=["Caregivers"])
app.include_router(patient_routes.router,prefix="/Home-Care/Patients",tags=["Patients"])
app.include_router(visit_routes.router,prefix="/Home-Care/Visitations",tags=["Visits"])
app.include_router(login_routes.router,prefix="/Home-Care/Login",tags=["Login"])
app.include_router(escalation_routes.router,prefix="/Home-Care/Escalations",tags=["Escalations"])
app.include_router(general_routes.router,prefix="/Home-Care/General",tags=["General"])

app.get("/")
def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "CORS enabled!"}

@app.on_event("startup")
async def startup():
    """
    Startup event to initialize the database connection.
    """
    await init_db()