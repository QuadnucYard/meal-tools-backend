import sys
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

sys.path[0] = str(Path(__file__).parents[2])


from app.db.session import async_sessionmaker, engine
from app.main import app

TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
async def db():
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
