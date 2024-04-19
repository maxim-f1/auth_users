from typing import Generator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.config.postgres import POSTGRES_CONFIG


engine = create_async_engine(POSTGRES_CONFIG.connection_url(), poolclass=NullPool, echo=False)
Session = async_sessionmaker(engine)


async def get_session_generator() -> Generator[AsyncSession, None, None]:
    session = None
    try:
        session = Session()
        async with session.begin():
            yield session
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()
