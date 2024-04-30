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

import os
import json
import codecs
import yaml

from nomad import utils
from nomad.units import ureg
from nomad.metainfo import Package
from nomad.datamodel import EntryArchive

from nomad_ML_smiles_reader.schema import (
    Simulation,
    Program,
    ModelSystem,
    ModelMethod,
    Outputs,
)
from nomad_ML_smiles_reader.properties import (
    PhysicalProperty,
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

# Defining paths to the file
current_dir = os.path.dirname(os.path.abspath(__file__))  # go to directory
# test_file = '../../tests/data/testing_two_molecules.json'  # inputfile - open file to parse - from Pipeline Pilot JSON Writer
test_file = '../../tests/data/original_data_smile_strings_48_finish.json'  # inputfile - open file to parse - from Pipeline Pilot JSON Writer
dirname = os.path.dirname(test_file)  # determine directory from filename
basename = os.path.basename(test_file).strip(
    '.json'
)  # determine filename without extension
nomad_schema_file = f'{dirname}/original_data_NOMADschema.archive.yaml'  # create new file for nomad yaml file. append "_NOMADschema.archive." and extention ".yaml" to file
filepath = os.path.normpath(
    os.path.join(current_dir, test_file)
)  # inputfile - combine absolute path with relative path and then remove redundant separators
nomad_schema_filepath = os.path.normpath(os.path.join(current_dir, nomad_schema_file))

# Logger to print warnings (disregard this)
logger = utils.get_logger(__name__)


# Creating the NOMAD schema YAML file
def create_schema():  # function
    return EntryArchive(
        definitions=Package(
            sections=[
                Program.m_def,
                ModelSystem.m_def,
                Simulation.m_def,
                Outputs.m_def,
                ModelMethod.m_def,
                PhysicalProperty.m_def,
                TotalEnergy.m_def,
                ElectronicEnergy.m_def,
                RepulsiveEnergy.m_def,
                IonizationPotential.m_def,
                GapEnergy.m_def,
                HeatOfFormation.m_def,
                MultipoleMoment.m_def,
                Enthalpy.m_def,
                Entropy.m_def,
                HeatCapacity.m_def,
                ZeroPointEnergy.m_def,
                ElectronicLevels.m_def,
                VibrationalModes.m_def,
                VibrationalSpectrum.m_def,
            ]
        )
    )


# And saving it to the YAML that we need to upload
yaml_schema = create_schema().m_to_dict(with_out_meta=True)
with open(
    nomad_schema_filepath, 'wt'
) as outfile:  # inputfilename_NOMADschema.archive.yaml
    outfile.write(yaml.dump(yaml_schema, indent=2))

# Loading JSON data from Input File
data = json.load(codecs.open(filepath, 'r', 'utf-8-sig'))  # inputfilename.json
for i, molecule_data in enumerate(data):
    # names defined from 01, 02, ..., 48 (different molecules)
    if i < 9:
        i_string = f'0{i+1}'
    else:
        i_string = str(i + 1)
    # new filename for NOMAD json file
    nomad_file = f'{dirname}/original_data_NOMAD_molecule{i_string}.archive.json'  # create a new filename for nomad json file. put in same directory as input file
    nomad_filepath = os.path.normpath(
        os.path.join(current_dir, nomad_file)
    )  # do same as previous command for nomad yaml file

    # And parsing into NOMAD archive
    archive = EntryArchive()
    simulation = Simulation(
        program=Program(
            name='BIOVIA Materials Studio',
            version='2022',
        ),
        model_method=ModelMethod(
            name='Semi-Empirical Molecular Orbital Package - VAMP',
        ),
    )
    archive.m_add_sub_section(EntryArchive.data, simulation)

    # Parsing `ModelSystem` as SMILES and other additional strings (using ChemNLP functionalities)
    smiles_id = molecule_data.get('Smiles', '')
    model_system = ModelSystem(smiles=smiles_id)
    simulation.model_system.append(model_system)
    model_system.normalize(archive, logger)

    # Parsing `Outputs` and the properties inside there
    outputs = Outputs()
    # energetics parsing
    energy_map = {
        'total_energy': TotalEnergy(),
        'electronic_energy': ElectronicEnergy(),
        'repulsive_energy': RepulsiveEnergy(),
        'ionization_potential': IonizationPotential(),
        'enthalpy': Enthalpy(),
        'entropy': Entropy(),
        'zero_point_energy': ZeroPointEnergy(),
    }
    for label, property in energy_map.items():
        energy = molecule_data.get(f'MSVAMP_{property.m_def.name}')
        if energy is not None:
            property.value = energy * ureg.eV
            setattr(outputs, label, property)
    # gap energy parsing
    homo = molecule_data.get('MSVAMP_HOMOEnergy')
    lumo = molecule_data.get('MSVAMP_LUMOEnergy')
    if homo is not None or lumo is not None:
        gap_energy = GapEnergy()
        gap_energy.value_homo = homo * ureg.eV if homo is not None else None
        gap_energy.value_lumo = lumo * ureg.eV if lumo is not None else None
        gap_energy.extract_gap()  # we extract the diff HOMO - LUMO if is positive
        outputs.gap_energy = gap_energy
    # heat capacities parsing
    capacity_map = {
        'heat_of_formation': HeatOfFormation(),
        'heat_capacity': HeatCapacity(),
    }
    for label, property in capacity_map.items():
        capacity = molecule_data.get(f'MSVAMP_{property.m_def.name}')
        if capacity is not None:
            property.value = capacity * ureg('kcal/mol')
            setattr(outputs, label, property)
    # multipoles parsing
    total_dipole = molecule_data.get('MSVAMP_TotalDipole')
    if total_dipole is not None:
        multipole_moment = MultipoleMoment(value=total_dipole * ureg('dimensionless'))
        multipole_moment.value_dipole = (
            molecule_data.get('MSVAMP_DipoleMoment') * ureg('dimensionless')
            if molecule_data.get('MSVAMP_DipoleMoment') is not None
            else None
        )
        # multipole_moment.value_quadrupole = (
        #     molecule_data.get('MSVAMP_QuadrupoleMoment') * ureg('dimensionless')
        #     if molecule_data.get('MSVAMP_QuadrupoleMoment') is not None
        #     else None
        # )
        # multipole_moment.value_octupole = (
        #     molecule_data.get('MSVAMP_OctupoleMoment') * ureg('dimensionless')
        #     if molecule_data.get('MSVAMP_OctupoleMoment') is not None
        #     else None
        # )
        outputs.multipole_moment = multipole_moment
    # electronic levels parsing
    electronic_levels = molecule_data.get('MSVAMP_ElectronicLevels')
    if electronic_levels is not None:
        levels = [level.split() for level in electronic_levels.split('\n')]
        section = ElectronicLevels(type='UV-VIS', n_levels=len(levels))
        excited_state = [int(level[0]) for level in levels]
        value = [float(level[1]) for level in levels]
        value_wavelength = [float(level[2]) for level in levels]
        oscillator_strength = [float(level[3]) for level in levels]
        transition_type = [int(level[-1]) for level in levels]
        section.excited_state = excited_state
        section.value = value * ureg('eV')
        section.value_wavelength = value_wavelength * ureg('nm')
        section.oscillator_strength = oscillator_strength * ureg('dimensionless')
        section.transition_type = transition_type
        outputs.electronic_levels = section
    # vibrational modes parsing
    vibrational_modes = molecule_data.get('MSVAMP_VibrationalMode')
    if vibrational_modes is not None:
        section = VibrationalModes(
            n_modes=len(vibrational_modes),
            value=vibrational_modes,
            frequency=molecule_data.get('MSVAMP_VibrationalFrequency') * ureg('THz')
            if molecule_data.get('MSVAMP_VibrationalFrequency') is not None
            else None,
            reduced_mass=molecule_data.get('MSVAMP_VibrationalReducedMass')
            * ureg('dimensionless')
            if molecule_data.get('MSVAMP_VibrationalReducedMass') is not None
            else None,
            raman_intensity=molecule_data.get('MSVAMP_VibrationalRamanIntensity')
            * ureg('dimensionless')
            if molecule_data.get('MSVAMP_VibrationalRamanIntensity') is not None
            else None,
        )
        outputs.vibrational_modes = section
    # vibrational spectrum parsing
    vibrational_spectrum_intensities = molecule_data.get(
        'MSVAMP_VibrationalIntensity_Strength'
    )
    if vibrational_spectrum_intensities is not None:
        section = VibrationalSpectrum(
            n_frequencies=len(vibrational_spectrum_intensities),
            value=vibrational_spectrum_intensities * ureg('km / mol'),
        )
        wavenumber = molecule_data.get('MSVAMP_VibrationalIntensity_Frequency') * ureg(
            '1/cm'
        )
        section.frequency = (ureg.speed_of_light * wavenumber).to('Hz')
        outputs.vibrational_spectrum = section

    simulation.outputs.append(outputs)
    outputs.normalize(archive, logger)

    # # Patch
    json_archive = archive.m_to_dict()
    # Replace the schema reference
    json_archive['data']['m_def'] = (
        f'../upload/raw/{os.path.basename(nomad_schema_file)}#/definitions/section_definitions/Simulation'
    )

    # And saving it to the JSON that we need to upload
    with open(nomad_filepath, 'wt') as outfile:
        outfile.write(json.dumps(json_archive, indent=2))
