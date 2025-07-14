import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from app.models import Base
from contextlib import asynccontextmanager

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./orders.db")

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Dependency
def get_session() -> AsyncSession:
    session = async_session()
    try:
        yield session
    finally:
        await session.close()
