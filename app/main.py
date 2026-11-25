
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.api.batch_routes import router as batch_router
from app.api.jd_routes import router as jd_router



app = FastAPI(
    title="AI Resume Matching & Ranking System",
    description="AI-powered resume matching and ranking application.",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from app.api.resume_routes import router as resume_router
app.include_router(jd_router)
app.include_router(resume_router)
app.include_router(batch_router)


@app.get("/")
def home():
    return {
        "message": "AI Resume Matching & Ranking System is running!",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "resume-matcher"
    }


def custom_openapi():
    from fastapi.openapi.utils import get_openapi

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    for schema in openapi_schema.get("components", {}).get("schemas", {}).values():
        for prop in schema.get("properties", {}).values():

            if prop.get("contentMediaType") == "application/octet-stream":
                prop.pop("contentMediaType", None)
                prop["format"] = "binary"

            items = prop.get("items", {})

            if items.get("contentMediaType") == "application/octet-stream":
                items.pop("contentMediaType", None)
                items["format"] = "binary"

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi