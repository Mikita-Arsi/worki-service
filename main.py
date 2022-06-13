from fastapi import FastAPI
from user.api import user_router
from link.api import link_router
from db import db, metadata, engine


app = FastAPI()


metadata.create_all(engine)
app.state.database = db


@app.on_event("startup")
async def startup() -> None:
    db_ = app.state.database
    if not db_.is_connected:
        await db_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    db_ = app.state.database
    if db_.is_connected:
        await db_.disconnect()


app.include_router(user_router)
app.include_router(link_router)