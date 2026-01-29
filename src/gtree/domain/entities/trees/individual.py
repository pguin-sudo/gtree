from dataclasses import dataclass

from gtree.domain.entities.base import ObjectBaseEntity


@dataclass(kw_only=True, slots=True)
class IndividualEntity(ObjectBaseEntity): ...
