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

    selfies = Quantity(
        type=str,
        description="""
        Notation for the structure of molecules following the SELF-referencing embedded string
        (SELFIES) , https://www.sciencedirect.com/science/article/pii/S2666389922002069.
        """,
    )

    deepsmiles = Quantity(
        type=str,
        description="""
        Notation for the structure of molecules following the DeepSMILES, https://chemrxiv.org/engage/chemrxiv/article-details/60c73ed6567dfe7e5fec388d.
        """,
    )

    canonical = Quantity(
        type=str,
        description="""
        Notation for the structure of molecules following the canonical SMILES, https://pubs.acs.org/doi/abs/10.1021/ci00062a008.
        """,
    )

    inchi = Quantity(
        type=str,
        description="""
        Notation for the structure of molecules following the IUPAC International Chemical Identifier,
        (InChI), https://iupac.org/who-we-are/divisions/division-details/inchi/
        """,
    )

    safe = Quantity(
        type=str,
        description="""
        Notation for the structure of molecules following the Sequential Attachment-based Fragment
        Embedding (SAFE), https://arxiv.org/abs/2310.10773.
        """,
    )

    iupac = Quantity(
        type=str,
        description="""
        Notation for the structure of molecules following the International Union Pure and Applied
        Chemistry (IUPAC), https://iupac.org/what-we-do/.
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
        unit='eV', #TODO: Check if this is the correct unit
        description="""
        Total energy from semiempirical calculation. This value is dependent on the basis selected and should not be used as an absolute value.
        """,
    )
    electronicenergy = Quantity(
        type=np.float64,
        unit='eV', #TODO: Check if this is the correct unit
        description="""
        Valance electron energy from semiempirical calculation.""",
    )

    repulsiveenergy = Quantity(
        type=np.float64,
        unit='eV', #TODO: Check if this is the correct unit
        description="""
        Repulsive Energy.
        """, #FIXME: Add description
    )

    ionizationpotential = Quantity(
        type=np.float64,
        unit='eV', #TODO: Check if this is the correct unit
        description="""
        Ionization Potential.
        """, #FIXME: Add description
    )

    homoenergy = Quantity(
        type=np.float64,
        unit='eV', #TODO: Check if this is the correct unit
        description="""
        HOMO Energy.
        """, #FIXME: Add description
    )
    lumoenergy = Quantity(
        type=np.float64,
        unit='eV', #TODO: Check if this is the correct unit
        description="""
        LUMO Energy.
        """, #FIXME: Add description
    )
    heatofformation = Quantity(
        type=np.float64,
        unit='kcal/mol', #TODO: Check if this is the correct unit
        description="""
        Heat of Formation.
        """, #FIXME: Add description
    )
    totaldipole = Quantity(
        type=np.float64,
        unit='', #TODO: Check if this is the correct unit
        description="""
        Total Dipole Moment.
        """, #FIXME: Add description
    )
    enthalpy = Quantity(
        type=np.float64,
        unit='eV', #TODO: Check if this is the correct unit
        description="""
        Enthalpy.
        """, #FIXME: Add description
    )
    entropy = Quantity(
        type=np.float64,
        unit='eV', #TODO: Check if this is the correct unit
        description="""
        Entropy.
        """, #FIXME: Add description
    )
    heatcapacity = Quantity(
        type=np.float64,
        unit='kcal/mol', #TODO: Check if this is the correct unit
        description="""
        Heat Capacity.
        """, #FIXME: Add description
    )

    zeropoint = Quantity(
        type=np.float64,
        unit='eV', #TODO: Check if this is the correct unit
        description="""
        Zero Points Energy.
        """, #FIXME: Add description
    )

    dipolemoment = Quantity(
        type=np.float64,
        shape=[1, 3],
        description="""
        Dipole Moment in three directions.
        """, #FIXME: Add description
    )

    qudrupolemoment = Quantity(
        type=np.float64,
        shape=[1, 6],
        description="""
        Qudrupole Moment.
        """, #FIXME: Add description
    )
    octupolemoment = Quantity(
        type=np.float64,
        shape=[1, 10],
        description="""
        Octupole Moment.
        """, #FIXME: Add description
    )

    vibrationalfreq = Quantity(
        type=np.float64,
        unit='THz', #TODO: Check if this is the correct unit
        shape=[1,'*'],
        description="""
        Vibrational Frequencies associated with Reduced Mass.
        """, #FIXME: Add description
    )

    vibrationalmass= Quantity(
        type=np.float64,
        shape=[1,'*'],
        description="""
        Reduced Mass as a function of Vibrational Frequency
        """, #FIXME: Add description
    )

    vibrationalintensityfreq = Quantity(
        type=np.float64,
        unit='THz', #TODO: Check if this is the correct unit
        shape=[1,'*'],
        description="""
        Frequencies associated with Vibrational Strength.
        """, #FIXME: Add description
    )
    vibrationalintensity = Quantity(
        type=np.float64,
        shape=[1,'*'],
        description="""
        Vibrational Strength as a function of Vibrational Frequency.
        """, #FIXME: Add description
    )

    electroniclevels = Quantity(
        #type={type_kind: uvis, type_data: [int, np.float64, np.float64, np.float64, int]},
        type = str,
        #shape=[5,'*'],
        description="""
        UV-VIS Data. Columns: Excited State Number, Frequency THz, Wavelength nm, Oscillator Strength, Transition Type.
        """, #FIXME: Add description
    )

class Simulation(Activity, EntryData):
    program = SubSection(section=Program.m_def)

    model_method = SubSection(section=BaseMethod.m_def)

    model_system = SubSection(section=ModelSystem.m_def, repeats=True)

    model_output = SubSection(section=ModelData.m_def)

m_package.__init_metainfo__()
