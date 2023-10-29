from app.db.session import SessionLocal


async def get_db():
    """Get AsyncSession"""
    async with SessionLocal() as session:
        yield session
