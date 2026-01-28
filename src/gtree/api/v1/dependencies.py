from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

# from gtree.application.services.trees.individual_service import IndividualService
from gtree.application.services.trees.tree_service import TreeService
from gtree.application.services.user_service import UserService
from gtree.domain.entities.user import UserEntity

# from gtree.infrastructure.db.repositories.trees.individual import IndividualRepository
from gtree.infrastructure.db.repositories.trees.tree import TreeRepository
from gtree.infrastructure.db.repositories.trees.tree_access import TreeAccessRepository
from gtree.infrastructure.db.repositories.user import UserRepository
from gtree.infrastructure.db.session import get_db

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# Services
def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))


def get_tree_service(db: AsyncSession = Depends(get_db)) -> TreeService:
    return TreeService(TreeRepository(db), TreeAccessRepository(db))


# def get_individual_service(db: AsyncSession = Depends(get_db)) -> IndividualService:
#    return IndividualService(IndividualRepository(db))


# Entities
async def get_current_active_user(
    token: str = Depends(oauth2_schema),
    user_service: UserService = Depends(get_user_service),
) -> UserEntity:
    return await user_service.get_current_active_auth_user(token)
