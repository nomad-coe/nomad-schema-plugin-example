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

    methods = Quantity(
        type=str,
        description="""
        Details on the simulation method used to generate data, https://www.3ds.com/assets/invest/2023-10/biovia-material-studio-vamp.pdf.
        """,
    )

class ModelData(Entity):
    """
    A base section used to specify the system solver information used for simulations.
    """

    totalenergy = Quantity(
        type=np.float64,
        description="""
        Total energy from semiempirical calculation. This value is dependent on the basis selected and should not be used as an absolute value.
        """,
    )
    electronicenergy = Quantity(
        type=np.float64,
        description="""
        Valance electron energy from semiempirical calculation.""",
    )

    repulsiveenergy = Quantity(
        type=np.float64,
        description="""
        Repulsive Energy.
        """, #FIXME: Add description
    )

    ionizationpotential = Quantity(
        type=np.float64,
        description="""
        Ionization Potential.
        """, #FIXME: Add description
    )

    homoenergy = Quantity(
        type=np.float64,
        description="""
        HOMO Energy.
        """, #FIXME: Add description
    )
    lumoenergy = Quantity(
        type=np.float64,
        description="""
        LUMO Energy.
        """, #FIXME: Add description
    )
    heatofformation = Quantity(
        type=np.float64,
        description="""
        Heat of Formation.
        """, #FIXME: Add description
    )
    totaldipole = Quantity(
        type=np.float64,
        description="""
        Total Dipole Moment.
        """, #FIXME: Add description
    )
    enthalpy = Quantity(
        type=np.float64,
        description="""
        Enthalpy.
        """, #FIXME: Add description
    )
    entropy = Quantity(
        type=np.float64,
        description="""
        Entropy.
        """, #FIXME: Add description
    )
    heatcapacity = Quantity(
        type=np.float64,
        description="""
        Heat Capacity.
        """, #FIXME: Add description
    )
class Simulation(Activity, EntryData):
    program = SubSection(section=Program.m_def)

    model_method = SubSection(section=BaseMethod.m_def)

    model_system = SubSection(section=ModelSystem.m_def, repeats=True)

    model_output = SubSection(section=ModelData.m_def)


m_package.__init_metainfo__()
