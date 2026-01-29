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
    def model_to_entity(cls, model: UserModel) -> UserEntity:
        return UserEntity(
            id=model.id,
            username=model.username,
            email=model.email,
            password_hash=model.password_hash,
            is_verified=model.is_verified,
            last_login=model.last_login,
            last_password_change=model.last_password_change,
            created_at=model.created_at,
            updated_at=model.updated_at,
            is_active=model.is_active,
        )
