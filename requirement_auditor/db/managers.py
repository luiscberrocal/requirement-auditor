from typing import List, Tuple

from .databases import RequirementDatabase  # type: ignore
from ..exceptions import RequirementAuditorException
from ..handlers import get_latest_version
from ..models import PythonRequirement
from ..utils import convert_version_to_tuples


def update_requirements(database: RequirementDatabase, requirement_names: List[str] | None):
    pass


def update_single_requirement(requirement: PythonRequirement,
                              stable_only: bool = True,
                              fields: List[str] | None = None) -> Tuple[PythonRequirement, bool]:
    version = get_latest_version(requirement.name, stable_only=stable_only)
    version_tuple = convert_version_to_tuples(version)
    updated = False
    if version_tuple > requirement.latest_version:
        requirement.latest_version = version
        updated = True
    if fields is not None:
        raise RequirementAuditorException('Not implemented')

    return requirement, updated
