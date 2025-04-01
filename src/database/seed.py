import asyncio
from db import sessionmanager
from src.entity.models import Contact
import sys
import os

base_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')
)
sys.path.append(base_path)


async def seed():
    contacts = [
        Contact(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="1234567890",
            birthday="1990-01-01",
            additional_info="Test contact"
        ),
        Contact(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            phone_number="0987654321",
            birthday="1992-03-15",
            additional_info="Another test"
        ),
    ]

    async with sessionmanager.session() as session:
        session.add_all(contacts)
        await session.commit()
        print("✅ Seed data inserted!")


if __name__ == "__main__":
    asyncio.run(seed())
