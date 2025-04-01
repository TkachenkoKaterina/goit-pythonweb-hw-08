from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.database.db import get_db
from src.schemas.contact import ContactCreate, ContactUpdate, ContactResponse
from src.repository import contacts as repo

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ContactResponse)
async def create(contact: ContactCreate, db: AsyncSession = Depends(get_db)):
    return await repo.create_contact(contact, db)


@router.get("/", response_model=List[ContactResponse])
async def read_all(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    return await repo.get_contacts(skip, limit, db)


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_one(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await repo.get_contact(contact_id, db)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update(
    contact_id: int,
    contact_data: ContactUpdate,
    db: AsyncSession = Depends(get_db),
):
    contact = await repo.update_contact(contact_id, contact_data, db)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.delete("/{contact_id}")
async def delete(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await repo.delete_contact(contact_id, db)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted"}


@router.get("/search/", response_model=List[ContactResponse])
async def search(
    query: str = Query(..., min_length=1), db: AsyncSession = Depends(get_db)
):
    return await repo.search_contacts(query, db)


@router.get("/upcoming_birthdays/", response_model=List[ContactResponse])
async def upcoming(db: AsyncSession = Depends(get_db)):
    return await repo.upcoming_birthdays(db)
