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

from nomad.metainfo import Package, Quantity, SubSection
from nomad.datamodel.data import ArchiveSection, EntryData
from nomad.datamodel.metainfo.basesections import System, Activity, Entity

from nomad_ML_smiles_reader.properties import (
    TotalEnergy,
    ElectronicEnergy,
    RepulsiveEnergy,
    IonizationPotential,
    GapEnergy,
    HeatOfFormation,
    MultipoleMoment,
    Enthalpy,
    Entropy,
    HeatCapacity,
    ZeroPointEnergy,
    ElectronicLevels,
    VibrationalModes,
    VibrationalSpectrum,
)


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

    name = Quantity(
        type=str,
        description="""
        Details on the simulation method used to generate data, https://www.3ds.com/assets/invest/2023-10/biovia-material-studio-vamp.pdf.
        """,
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

    enthalpy = SubSection(sub_section=Enthalpy.m_def)

    entropy = SubSection(sub_section=Entropy.m_def)

    heat_capacity = SubSection(sub_section=HeatCapacity.m_def)

    zero_point_energy = SubSection(sub_section=ZeroPointEnergy.m_def)

    electronic_levels = SubSection(sub_section=ElectronicLevels.m_def)

    vibrational_modes = SubSection(sub_section=VibrationalModes.m_def)

    vibrational_spectrum = SubSection(sub_section=VibrationalSpectrum.m_def)

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
