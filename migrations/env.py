from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import AsyncEngine
# from sqlalchemy import pool

from src.database.db import sessionmanager
from src.entity.models import Base  # заміни на актуальний шлях до Base

# Alembic Config object
config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Для autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запуск міграцій в офлайн-режимі (без підключення до БД)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Виконує міграції в поточному середовищі."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запуск міграцій в онлайн-режимі (з підключенням до БД)."""
    connectable: AsyncEngine = sessionmanager._engine

    async with connectable.begin() as conn:
        await conn.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())
