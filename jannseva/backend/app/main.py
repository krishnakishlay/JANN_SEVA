from fastapi import FastAPI
from app.database import engine
from app.database import Base
from app.routes.auth import router as auth_router
from app.routes.admin import router as admin_router
from app.routes import complaint

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    auth_router
)
app.include_router(
    admin_router
)
app.include_router(
    complaint.router
)

@app.get("/")
def root():
    return {"message": "API Running"}