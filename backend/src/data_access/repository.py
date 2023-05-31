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
#        Nadzeya Hutsko <nadzeya.hutsko@canonical.com>
"""Services for working with objects from DB"""

from sqlalchemy.orm import joinedload, Session
from .models import Family, Stage, Artefact


def get_stage_by_name(session: Session, stage_name: str, family: Family) -> Stage:
    """
    Get the stage object by its name

    :session: DB session
    :stage_name: name of the stage
    :family: the Family object where stages are located
    :return: Stage
    """
    stage = (
        session.query(Stage)
        .filter(Stage.name == stage_name, Stage.family == family)
        .first()
    )
    return stage


def get_artefacts_by_family_name(session: Session, family_name: str) -> list[Artefact]:
    """
    Get all the artefacts in a family

    :session: DB session
    :family_name: name of the family
    :return: list of Artefacts
    """
    artefacts = (
        session.query(Artefact)
        .join(Stage)
        .filter(Stage.family.has(Family.name == family_name))
        .options(joinedload(Artefact.stage))
        .all()
    )
    return artefacts