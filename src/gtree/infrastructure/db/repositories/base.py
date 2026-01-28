from sqlalchemy.ext.asyncio import AsyncSession


class RepositoryObjectBase:
    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db
