from typing import List, Tuple

from .databases import RequirementDatabase  # type: ignore
from ..exceptions import RequirementAuditorException
from ..handlers import get_latest_version
from ..models import PythonRequirement
from ..utils import convert_version_to_tuples


def update_requirements(database: RequirementDatabase,
                        stable_only: bool = True,
                        requirement_names: List[str] | None = None):
    requirements = database.all()
    updated_requirements = list()
    for requirement in requirements:
        updated_requirement, updated = update_single_requirement(requirement, stable_only=stable_only)
        if updated:
            updated_requirements.append(updated_requirement)
    return updated_requirements


def update_single_requirement(requirement: PythonRequirement,
                              stable_only: bool = True,
                              fields: List[str] | None = None) -> Tuple[PythonRequirement, bool]:
    updated = False
    version = get_latest_version(requirement.name, stable_only=stable_only)
    version_tuple = convert_version_to_tuples(version)
    new_requirement = None

    if version_tuple > requirement.latest_version_info:
        new_requirement = requirement.copy()
        new_requirement.latest_version = version
        updated = True
    if fields is not None:
        raise RequirementAuditorException('Not implemented')

    if updated:
        return new_requirement, updated
    return requirement, updated
