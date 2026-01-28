from gtree.domain.entities.user import UserEntity
from gtree.infrastructure.db.models.user import UserModel


class UserMapper:
    @classmethod
    def entity_to_model(cls, entity: UserEntity) -> UserModel:
        return UserModel(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            password_hash=entity.password_hash,
            is_verified=entity.is_verified,
            last_login=entity.last_login,
            last_password_change=entity.last_password_change,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_active=entity.is_active,
        )

    @classmethod
    def model_to_entity(cls, entity: UserModel) -> UserEntity:
        return UserEntity.model_validate(entity)
