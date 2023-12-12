# Copyright 2023 Canonical Ltd.
# All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Written by:
#        Omar Selo <omar.selo@canonical.com>


from enum import Enum
from typing import Annotated

from pydantic import (
    AliasPath,
    BaseModel,
    Field,
    HttpUrl,
    field_serializer,
    field_validator,
    model_validator,
)

from test_observer.data_access.models_enums import (
    FamilyName,
    TestExecutionStatus,
    TestResultStatus,
)


class StartTestExecutionRequest(BaseModel):
    family: FamilyName
    name: str
    version: str
    revision: int | None = None
    track: str | None = None
    store: str | None = None
    series: str | None = None
    repo: str | None = None
    arch: str
    execution_stage: str
    environment: str
    ci_link: Annotated[str, HttpUrl]

    @field_serializer("family")
    def serialize_dt(self, family: FamilyName):
        return family.value

    @field_validator("version")
    @classmethod
    def validate_version(cls: type["StartTestExecutionRequest"], version: str) -> str:
        if version in ("", "null"):
            raise ValueError(f"Invalid version value '{version}'")
        return version

    @model_validator(mode="after")
    def validate_required_fields(self) -> "StartTestExecutionRequest":
        required_fields = {
            FamilyName.SNAP: ("store", "track", "revision"),
            FamilyName.DEB: ("series", "repo"),
        }
        family = self.family

        for required_field in required_fields[family]:
            if getattr(self, required_field) is None:
                raise ValueError(f"{required_field} is required for {family} family")

        return self


class C3TestResultStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"


class C3TestResult(BaseModel):
    id: int
    name: str
    status: C3TestResultStatus
    category: str
    comment: str
    io_log: str


class EndTestExecutionRequest(BaseModel):
    id: int
    ci_link: Annotated[str, HttpUrl]
    test_results: list[C3TestResult]


class TestExecutionsPatchRequest(BaseModel):
    c3_link: HttpUrl | None = None
    ci_link: HttpUrl | None = None
    status: TestExecutionStatus | None = None


class TestResultDTO(BaseModel):
    id: int
    name: str = Field(validation_alias=AliasPath("test_case", "name"))
    category: str = Field(validation_alias=AliasPath("test_case", "category"))
    status: TestResultStatus
    comment: str
    io_log: str
