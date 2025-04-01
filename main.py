import uvicorn
from fastapi import FastAPI

from src.api import contacts
from src.entity.models import Base
from src.database.db import sessionmanager


app = FastAPI(title="Contacts API")

app.include_router(contacts.router)


@app.on_event("startup")
async def on_startup():
    async with sessionmanager.session() as session:
        async with session.bind.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
