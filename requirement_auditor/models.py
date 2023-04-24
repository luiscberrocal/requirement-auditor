from datetime import datetime
from typing import Optional, TypeVar

from pydantic import BaseModel, Field, HttpUrl

from requirement_auditor.exceptions import ParsingError
from requirement_auditor.utils import convert_version_to_tuples

import logging

logger = logging.getLogger(__name__)


def convert_datetime_to_iso_8601_with_z_suffix(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')


class PinnedRequirement(BaseModel):
    name: str
    version: str
    comment: Optional[str] = Field(default=None)


class PythonRequirement(BaseModel):
    name: str
    latest_version: str
    approved_version: str
    group: Optional[str]
    environment: Optional[str]
    last_updated: Optional[datetime] = Field(default=datetime.now())
    home_page: Optional[HttpUrl]
    license: Optional[str]

    def to_req_line(self) -> str:
        if self.home_page is None:
            line = f'{self.name}=={self.approved_version}'
        else:
            line = f'{self.name}=={self.approved_version} # {self.home_page}'
        return line

    class Config:
        json_encoders = {
            datetime: convert_datetime_to_iso_8601_with_z_suffix
        }

    @property
    def latest_version_info(self):
        version_info = tuple(
            [
                int(num) if num.isdigit() else num
                for num in self.latest_version.replace("-", ".", 1).split(".")
            ]
        )
        return version_info

    @property
    def approved_version_info(self):
        version_info = tuple(
            [
                int(num) if num.isdigit() else num
                for num in self.approved_version.replace("-", ".", 1).split(".")
            ]
        )
        return version_info


class ParsedLine(BaseModel):
    line_number: int
    raw: str
    pinned: PinnedRequirement = Field(default=None)
    db_requirement: Optional[PythonRequirement] = Field(default=None)


TVersionNumber = TypeVar("TVersionNumber", bound="VersionNumber")


class VersionNumber(BaseModel):
    major: int
    minor: int
    patch: Optional[int | str]

    @staticmethod
    def parse(version: str, raise_on_error: bool = False) -> TVersionNumber | None:
        try:
            version_tuple = convert_version_to_tuples(version)
            if len(version_tuple) == 2:
                patch = 0
            else:
                patch = version_tuple[2]
            major = version_tuple[0]
            minor = version_tuple[1]
            return VersionNumber(major=major, minor=minor, patch=patch)
        except ValueError as e:
            msg = f'Could not parse version {version}. Error {e}'
            logger.error(msg)
            if raise_on_error:
                raise ParsingError(msg)
            return None

    def __str__(self):
        if self.patch is None:
            return f'{self.major}.{self.minor}'
        else:
            return f'{self.major}.{self.minor}.{self.patch}'

    def __ge__(self, other):
        if type(other.patch) == type(self.patch):
            return convert_version_to_tuples(str(self)) >= convert_version_to_tuples(str(other))
        else:
            condition1 = (self.major, self.minor) >= (other.major, other.minor)
            if condition1 and isinstance(self.patch, str):
                return True
            else:
                return False

    def __gt__(self, other):
        if type(other.patch) == type(self.patch):
            return convert_version_to_tuples(str(self)) > convert_version_to_tuples(str(other))
        else:
            condition1 = (self.major, self.minor) > (other.major, other.minor)
            if condition1 and isinstance(self.patch, str):
                return True
            else:
                return False

    def __le__(self, other):
        if type(other.patch) == type(self.patch):
            return convert_version_to_tuples(str(self)) <= convert_version_to_tuples(str(other))
        else:
            condition1 = (self.major, self.minor) <= (other.major, other.minor)
            if condition1 and isinstance(other.patch, str):
                return True
            else:
                return False

    def __lt__(self, other):
        if type(other.patch) == type(self.patch):
            return convert_version_to_tuples(str(self)) < convert_version_to_tuples(str(other))
        else:
            condition1 = (self.major, self.minor) < (other.major, other.minor)
            if condition1 and isinstance(other.patch, str):
                return True
            else:
                return False
