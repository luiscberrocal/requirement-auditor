from typing import List, Tuple

from requirement_auditor.db.databases import RequirementDatabase
from requirement_auditor.handlers import get_latest_version
from requirement_auditor.models import PythonRequirement


def update_requirements(database: RequirementDatabase, requirement_names: List[str] | None):
    pass


def update_single_requirement(requirement: PythonRequirement,
                              stable_only: bool = True) -> Tuple[PythonRequirement, bool]:
    version = get_latest_version(requirement.name, stable_only=stable_only)
