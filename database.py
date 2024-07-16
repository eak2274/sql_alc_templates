from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine
from config import settings

engine = create_engine(
        url=settings.DB_URL_SYNC,
        echo=True
    )

async_engine = create_async_engine(
    url=settings.DB_URL_ASYNC
    )

session_factory = sessionmaker(bind=engine)

async_session_factory = async_sessionmaker(bind=async_engine)
