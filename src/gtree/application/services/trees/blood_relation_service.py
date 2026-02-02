from uuid import UUID

from gtree.api.v1.schemas.trees.blood_relation import (
    BloodRelationCreateRequestSchema,
)
from gtree.application.authorization.tree_access import access_to_tree
from gtree.application.exceptions.individual import UnknownIndividualForTreeException
from gtree.domain.entities._value_objects.tree_access_level import TreeAccessLevel
from gtree.domain.entities.trees.individual import IndividualEntity
from gtree.infrastructure.db.repositories.trees.individual import IndividualRepository
from gtree.infrastructure.db.repositories.trees.tree_access import TreeAccessRepository


class BloodRelationService:
    def __init__(
        self,
        blood_relation_repository: BloodRelationRepository,
        individual_repository: IndividualRepository,
        tree_access_repository: TreeAccessRepository,
    ):
        self.blood_relation_repository = blood_relation_repository
        self.individual_repository = individual_repository
        self.tree_access_repository = tree_access_repository

    @access_to_tree(TreeAccessLevel.VIEWER)
    async def get_blood_relations_for_tree(
        self,
        user_id: UUID,  # noqa: ARG002
        tree_id: UUID,
    ) -> list[BloodRelationEntity]:
        return await self.blood_relation_repository.get_by_tree_id(tree_id)

    @access_to_tree(TreeAccessLevel.VIEWER)
    async def get_blood_relation_by_id(
        self,
        user_id: UUID,  # noqa: ARG002
        tree_id: UUID,
        parent_id: UUID,
        child_id: UUID,
    ) -> BloodRelationEntity:
        parent = await self.individual_repository.get_by_id(parent_id)
        if parent.tree_id != tree_id:
            raise UnknownIndividualForTreeException
        child = await self.individual_repository.get_by_id(child_id)
        if child.tree_id != tree_id:
            raise UnknownIndividualForTreeException

        return await self.blood_relation_repository.get_by_id(parent_id, child_id)

    @access_to_tree(TreeAccessLevel.EDITOR)
    async def create_individual(
        self,
        user_id: UUID,  # noqa: ARG002
        tree_id: UUID,
        parent_id: UUID,
        child_id: UUID,
    ) -> IndividualEntity:
        parent = await self.individual_repository.get_by_id(parent_id)
        if parent.tree_id != tree_id:
            raise UnknownIndividualForTreeException
        child = await self.individual_repository.get_by_id(child_id)
        if child.tree_id != tree_id:
            raise UnknownIndividualForTreeException

        return await self.individual_repository.create(individual)

    @access_to_tree(TreeAccessLevel.EDITOR)
    async def update_individual(
        self,
        user_id: UUID,  # noqa: ARG002
        tree_id: UUID,
        individual_id: UUID,
        # TODO: Remove schema from service
        individual_schema: IndividualUpdateRequestSchema,
    ) -> IndividualEntity:
        individual = await self.individual_repository.get_by_id(individual_id)
        if individual.tree_id != tree_id:
            raise UnknownIndividualForTreeException
        individual.update_individual(**individual_schema.model_dump())
        return await self.individual_repository.update(individual)

    @access_to_tree(TreeAccessLevel.EDITOR)
    async def delete_individual(
        self,
        user_id: UUID,  # noqa: ARG002
        tree_id: UUID,
        individual_id: UUID,
    ) -> None:
        individual = await self.individual_repository.get_by_id(individual_id)
        if individual.tree_id != tree_id:
            raise UnknownIndividualForTreeException
        return await self.individual_repository.delete(individual_id)
