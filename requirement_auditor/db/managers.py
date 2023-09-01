import logging
from typing import List, Tuple

from .databases import RequirementDatabase  # type: ignore
from ..exceptions import RequirementAuditorException
from ..handlers import get_latest_version
from ..models import PythonRequirement
from ..utils import convert_version_to_tuples

logger = logging.getLogger(__name__)


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
    try:
        if version_tuple > requirement.latest_version_info:
            new_requirement = requirement.copy()
            new_requirement.latest_version = version
            updated = True
    except TypeError as e:
        error_message = f'{e}. Version {version_tuple} latest {requirement.latest_version}'
        logger.error(error_message)
    if fields is not None:
        raise RequirementAuditorException('Not implemented')

    if updated:
        return new_requirement, updated
    return requirement, updated
