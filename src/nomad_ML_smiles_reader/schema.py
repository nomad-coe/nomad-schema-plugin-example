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

from typing import Optional

from nomad.metainfo import Package, Section, Quantity, SubSection
from nomad.datamodel.data import ArchiveSection, EntryData
from nomad.datamodel.metainfo.basesections import System, Activity

from .properties import *


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


class ModelSystem(System):
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

    def resolve_chemical_ids(self) -> None:
        """
        Resolve the chemical IDs from the SMILES string.
        """
        # We extract information from the SMILES string
        for label_id in ['selfies', 'deepsmiles', 'canonical', 'inchi']:
            try:
                conversion_funct = globals()[f'smiles_to_{label_id}']
                result = conversion_funct(smiles=self.smiles)
            except Exception:
                result = ''
            setattr(self, f'{label_id}_id', result)

    def normalize(self, archive, logger) -> None:
        super().normalize(archive, logger)

        # We extract information from the SMILES string
        self.resolve_chemical_ids()


class ModelMethod(ArchiveSection):
    """
    A base section used to specify the method solver information used for simulations.
    """

    method_name = Quantity(
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
        unit='eV',  # TODO: Check if this is the correct unit
        description="""
        Total energy from semiempirical calculation. This value is dependent on the basis selected and should not be used as an absolute value.
        """,
    )
    electronicenergy = Quantity(
        type=np.float64,
        unit='eV',  # TODO: Check if this is the correct unit
        description="""
        Valance electron energy from semiempirical calculation.""",
    )

    repulsiveenergy = Quantity(
        type=np.float64,
        unit='eV',  # TODO: Check if this is the correct unit
        description="""
        Repulsive Energy.
        """,  # FIXME: Add description
    )

    ionizationpotential = Quantity(
        type=np.float64,
        unit='eV',  # TODO: Check if this is the correct unit
        description="""
        Ionization Potential.
        """,  # FIXME: Add description
    )

    homoenergy = Quantity(
        type=np.float64,
        unit='eV',  # TODO: Check if this is the correct unit
        description="""
        HOMO Energy.
        """,  # FIXME: Add description
    )
    lumoenergy = Quantity(
        type=np.float64,
        unit='eV',  # TODO: Check if this is the correct unit
        description="""
        LUMO Energy.
        """,  # FIXME: Add description
    )
    heatofformation = Quantity(
        type=np.float64,
        unit='kcal/mol',  # TODO: Check if this is the correct unit
        description="""
        Heat of Formation.
        """,  # FIXME: Add description
    )
    totaldipole = Quantity(
        type=np.float64,
        unit='',  # TODO: Check if this is the correct unit
        description="""
        Total Dipole Moment.
        """,  # FIXME: Add description
    )
    enthalpy = Quantity(
        type=np.float64,
        unit='eV',  # TODO: Check if this is the correct unit
        description="""
        Enthalpy.
        """,  # FIXME: Add description
    )
    entropy = Quantity(
        type=np.float64,
        unit='eV',  # TODO: Check if this is the correct unit
        description="""
        Entropy.
        """,  # FIXME: Add description
    )
    heatcapacity = Quantity(
        type=np.float64,
        unit='kcal/mol',  # TODO: Check if this is the correct unit
        description="""
        Heat Capacity.
        """,  # FIXME: Add description
    )

    zeropoint = Quantity(
        type=np.float64,
        unit='eV',  # TODO: Check if this is the correct unit
        description="""
        Zero Points Energy.
        """,  # FIXME: Add description
    )

    dipolemoment = Quantity(
        type=np.float64,
        shape=[1, 3],
        description="""
        Dipole Moment in three directions.
        """,  # FIXME: Add description
    )

    qudrupolemoment = Quantity(
        type=np.float64,
        shape=[1, 6],
        description="""
        Qudrupole Moment.
        """,  # FIXME: Add description
    )
    octupolemoment = Quantity(
        type=np.float64,
        shape=[1, 10],
        description="""
        Octupole Moment.
        """,  # FIXME: Add description
    )

    vibrationalfreq = Quantity(
        type=np.float64,
        unit='THz',  # TODO: Check if this is the correct unit
        shape=[1, '*'],
        description="""
        Vibrational Frequencies associated with Reduced Mass.
        """,  # FIXME: Add description
    )

    vibrationalmass = Quantity(
        type=np.float64,
        shape=[1, '*'],
        description="""
        Reduced Mass as a function of Vibrational Frequency
        """,  # FIXME: Add description
    )

    vibrationalintensityfreq = Quantity(
        type=np.float64,
        unit='THz',  # TODO: Check if this is the correct unit
        shape=[1, '*'],
        description="""
        Frequencies associated with Vibrational Strength.
        """,  # FIXME: Add description
    )
    vibrationalintensity = Quantity(
        type=np.float64,
        shape=[1, '*'],
        description="""
        Vibrational Strength as a function of Vibrational Frequency.
        """,  # FIXME: Add description
    )

    electroniclevels = Quantity(
        # type={type_kind: uvis, type_data: [int, np.float64, np.float64, np.float64, int]},
        type=str,
        # shape=[5,'*'],
        description="""
        UV-VIS Data. Columns: Excited State Number, Frequency THz, Wavelength nm, Oscillator Strength, Transition Type.
        """,  # FIXME: Add description
    )


class Outputs(ArchiveSection):
    """
    Output properties of a simulation. This base class can be used for inheritance in any of the output properties
    defined in this schema.
    """

    model_system_ref = Quantity(
        type=ModelSystem,
        description="""
        Reference to the `ModelSystem` section to which the output property references to and on
        on which the simulation is performed.
        """,
    )

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # List of properties
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    total_energy = SubSection(sub_section=TotalEnergy.m_def)

    electronic_energy = SubSection(sub_section=ElectronicEnergy.m_def)

    repulsive_energy = SubSection(sub_section=RepulsiveEnergy.m_def)

    ionization_potential = SubSection(sub_section=IonizationPotential.m_def)

    gap_energy = SubSection(sub_section=GapEnergy.m_def)

    heat_of_formation = SubSection(sub_section=HeatOfFormation.m_def)

    multipole_moment = SubSection(sub_section=MultipoleMoment.m_def)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def set_model_system_ref(self) -> Optional[ModelSystem]:
        """
        Set the reference to the last ModelSystem if this is not set in the output. This is only
        valid if there is only one ModelSystem in the parent section.

        Returns:
            (Optional[ModelSystem]): The reference to the last ModelSystem.
        """
        if self.m_parent is not None:
            model_systems = self.m_parent.model_system
            if model_systems is not None and len(model_systems) == 1:
                return model_systems[-1]
        return None

    def normalize(self, archive, logger) -> None:
        super().normalize(archive, logger)

        # Set ref to the last ModelSystem if this is not set in the output
        if self.model_system_ref is None:
            self.model_system_ref = self.set_model_system_ref()


class Simulation(Activity, EntryData):
    program = SubSection(section=Program.m_def)

    model_system = SubSection(section=ModelSystem.m_def, repeats=True)

    model_method = SubSection(section=ModelMethod.m_def, repeats=False)

    outputs = SubSection(section=Outputs.m_def, repeats=True)

    def normalize(self, archive, logger) -> None:
        super().normalize(archive, logger)


m_package.__init_metainfo__()
