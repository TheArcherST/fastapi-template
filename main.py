from fastapi import FastAPI

from infrastructure.database import on_startup as on_database_startup

from api.routers import router


app = FastAPI()

app.include_router(router)


@app.on_event("startup")
async def on_app_startup():
    await on_database_startup()
