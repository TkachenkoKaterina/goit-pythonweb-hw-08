from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from src.entity.models import Contact
from src.schemas.contact import ContactCreate, ContactUpdate


async def create_contact(contact: ContactCreate, db: AsyncSession):
    new_contact = Contact(**contact.dict())
    db.add(new_contact)
    await db.commit()
    await db.refresh(new_contact)
    return new_contact


async def get_contact(contact_id: int, db: AsyncSession):
    result = await db.execute(select(Contact).where(Contact.id == contact_id))
    return result.scalar_one_or_none()


async def get_contacts(skip: int, limit: int, db: AsyncSession):
    result = await db.execute(select(Contact).offset(skip).limit(limit))
    return result.scalars().all()


async def update_contact(
    contact_id: int, contact_data: ContactUpdate, db: AsyncSession
):
    contact = await get_contact(contact_id, db)
    if contact:
        for field, value in contact_data.dict().items():
            setattr(contact, field, value)
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession):
    contact = await get_contact(contact_id, db)
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def search_contacts(query: str, db: AsyncSession):
    stmt = select(Contact).where(
        or_(
            Contact.first_name.ilike(f"%{query}%"),
            Contact.last_name.ilike(f"%{query}%"),
            Contact.email.ilike(f"%{query}%"),
        )
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def upcoming_birthdays(db: AsyncSession):
    today = datetime.today().date()
    next_week = today + timedelta(days=7)

    stmt = select(Contact).where(
        func.date_part("doy", Contact.birthday).between(
            func.date_part("doy", today),
            func.date_part("doy", next_week),
        )
    )
    result = await db.execute(stmt)
    return result.scalars().all()
