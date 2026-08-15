from fastapi import FastAPI
from core.config import settings
from database.db import engine,Base
from routers.user import router as user_router
from routers.url import router as url_router,redirect_router
from models.user import User
from models.url import URL  
from middleware.logging import LoggingMiddleware
from middleware.request_id import RequestIDMiddleware
from core.exception_handler import register_exception_handlers
from core.redis import redis_client


app = FastAPI(title=settings.APP_NAME)

Base.metadata.create_all(engine)

app.include_router(user_router)
app.include_router(url_router)
app.include_router(redirect_router)

app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)
register_exception_handlers(app)


