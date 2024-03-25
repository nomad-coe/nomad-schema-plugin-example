#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import numpy as np

from nomad.metainfo import Package, Section, Quantity, SubSection

from nomad.datamodel.data import ArchiveSection, EntryData
from nomad.datamodel.metainfo.basesections import Entity, Activity


m_package = Package()


class Program(ArchiveSection):
    """
    A base section used to specify a well-defined program used for simulations.
    """

    name = Quantity(
        type=str,
        description="""
        The name of the program.
        """,
    )

    version = Quantity(
        type=str,
        description="""
        The version label of the program.
        """,
    )


class ModelSystem(Entity):
    """
    A base section used to specify the system information used for simulations.
    """

    smiles = Quantity(
        type=str,
        description="""
        Notation for the structure of molecules following the Simplified Molecular-Input Line-Entry
        System (SMILES), https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system.
        """,
    )

class BaseMethod(Entity):
    """
    A base section used to specify the system solver information used for simulations.
    """

    smiles = Quantity(
        type=str,
        description="""
        Details on the simulation method used to generate data, https://www.3ds.com/assets/invest/2023-10/biovia-material-studio-vamp.pdf.
        """,
    )

class Data(Entity):
    """
    A base section used to specify the system solver information used for simulations.
    """

    smiles = Quantity(
        type=np.float64,
        description="""
        Total energy from semiempirical calculation. This value is dependent on the basis selected and should not be used as an absolute value.
        """,
    )


class Simulation(Activity, EntryData):
    program = SubSection(section=Program.m_def)

    model_system = SubSection(section=ModelSystem.m_def, repeats=True)

    model_method = SubSection(section=BaseMethod.m_def, repeats=True)

    outputs = SubSection(section=Data.m_def)


m_package.__init_metainfo__()
