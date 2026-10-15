from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

from app.database import init_db

from app.routes import router


app = FastAPI(

    title="FitBuddy - AI Fitness Plan Generator",

    description=(
        "AI-powered personalized fitness "
        "plan generator using Gemini."
    ),

    version="1.0.0"
)


# --------------------------------
# Static Files
# --------------------------------

app.mount(

    "/static",

    StaticFiles(
        directory="static"
    ),

    name="static"
)


# --------------------------------
# Routes
# --------------------------------

app.include_router(
    router
)


# --------------------------------
# Startup
# --------------------------------

@app.on_event("startup")
def startup_event():

    init_db()