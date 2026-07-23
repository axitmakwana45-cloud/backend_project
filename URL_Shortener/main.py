from fastapi import FastAPI
from core.config import settings
from database.db import engine,Base
from routers.user import router as user_router

app = FastAPI(title=settings.APP_NAME)

Base.metadata.create_all(engine)

app.include_router(user_router)

