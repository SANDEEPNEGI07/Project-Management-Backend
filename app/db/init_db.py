from app.db.base import Base
from app.db.session import engine

# Import all models so they are registered with Base.metadata
from app.models import (  # noqa: F401
    users, user_profiles, organizations, projects, tasks,
)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
