from typing import Any, List, Optional

from pydantic import BaseModel, Field


class Downloads(BaseModel):
    last_day: int
    last_month: int
    last_week: int


class ProjectUrls(BaseModel):
    documentation: str = Field(..., alias='Documentation')
    funding: str = Field(..., alias='Funding')
    homepage: str = Field(..., alias='Homepage')
    release_notes: str = Field(..., alias='Release notes')
    source: str = Field(..., alias='Source')
    tracker: str = Field(..., alias='Tracker')


class Info(BaseModel):
    author: str
    author_email: str
    bugtrack_url: Any
    classifiers: List[str]
    description: str
    description_content_type: str
    docs_url: Any
    download_url: str
    downloads: Downloads
    home_page: str
    keywords: str
    license: str
    maintainer: str
    maintainer_email: str
    name: str
    package_url: str
    platform: Any
    project_url: str
    project_urls: ProjectUrls
    release_url: str
    requires_dist: List[str]
    requires_python: str
    summary: str
    version: str
    yanked: bool
    yanked_reason: Any


class Digests(BaseModel):
    blake2b_256: str
    md5: str
    sha256: str


class Url(BaseModel):
    comment_text: str
    digests: Digests
    downloads: int
    filename: str
    has_sig: bool
    md5_digest: str
    packagetype: str
    python_version: str
    requires_python: str
    size: int
    upload_time: str
    upload_time_iso_8601: str
    url: str
    yanked: bool
    yanked_reason: Any


class PyPiResponse(BaseModel):
    info: Optional[Info] = None
    last_serial: Optional[int] = None
    urls: Optional[List[Url]] = None
    vulnerabilities: Optional[List] = None
