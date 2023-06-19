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
#        Nadzeya Hutsko <nadzeya.hutsko@canonical.com>
from pydantic import BaseModel


class EnvironmentDTO(BaseModel):
    id: int
    name: str
    architecture: str

    class Config:
        orm_mode = True


class TestExecutionDTO(BaseModel):
    id: int
    jenkins_link: str | None
    c3_link: str | None
    environment: EnvironmentDTO

    class Config:
        orm_mode = True


class ArtefactBuildDTO(BaseModel):
    id: int
    revision: int | None
    test_executions: list[TestExecutionDTO]

    class Config:
        orm_mode = True