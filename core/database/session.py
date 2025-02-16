from contextvars import ContextVar, Token
from typing import Union, Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql.expression import Delete, Insert, Update

from core.config import config

session_context: ContextVar[str] = ContextVar("session_context")

def get_session_context() -> str:
    return session_context.get()

def set_session_context(session_id: str) -> Optional[Token]:
    return session_context.set(session_id)
    
def reset_session_context(context: Token) -> None:
    session_context.reset(context)
    
engines = {
    "writer": create_async_engine(config.DATABASE_URL, pool_recycle=3600),
    "reader": create_async_engine(config.DATABASE_URL, pool_recycle=3600),
}

class RoutingSession(AsyncSession):
    def get_bind(self, mapper=None, clause=None, **kwargs):
        if self.in_transaction() or isinstance(clause, (Update, Delete, Insert)):
            return engines["writer"]
        return engines["reader"]


async_session_factory = sessionmaker(
    class_=AsyncSession,
    expire_on_commit=False,
)

session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=get_session_context,
)


async def get_session():
    """
    Get the database session.
    This can be used for dependency injection.

    :return: The database session.
    """
    async with session() as s:
        yield s


Base = declarative_base()