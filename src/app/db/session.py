from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app.core.config import settings

engine = AsyncEngine(create_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True))
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
