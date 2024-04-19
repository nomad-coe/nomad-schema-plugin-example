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

from chemnlp.data.reprs import *

from nomad import utils
from nomad.units import ureg
from nomad.metainfo import Package
from nomad.datamodel import EntryArchive

from .schema import Simulation, Program, ModelSystem, ModelMethod, ModelData, Outputs
from .properties import (
    TotalEnergy,
    ElectronicEnergy,
    RepulsiveEnergy,
    IonizationPotential,
    GapEnergy,
    HeatOfFormation,
    MultipoleMoment,
)

# Defining paths to the file
current_dir = os.path.dirname(os.path.abspath(__file__))  # go to directory
test_file = '../../tests/data/testing_two_molecules.json'  # inputfile - open file to parse - from Pipeline Pilot JSON Writer
dirname = os.path.dirname(test_file)  # determine directory from filename
basename = os.path.basename(test_file).strip(
    '.json'
)  # determine filename without extension
nomad_file = f'{dirname}/{basename}_NOMAD.archive.json'  # create a new filename for nomad json file. put in same directory as input file
nomad_schema_file = f'{dirname}/{basename}_NOMADschema.archive.yaml'  # create new file for nomad yaml file. append "_NOMADschema.archive." and extention ".yaml" to file
filepath = os.path.normpath(
    os.path.join(current_dir, test_file)
)  # inputfile - combine absolute path with relative path and then remove redundant separators
nomad_filepath = os.path.normpath(
    os.path.join(current_dir, nomad_file)
)  # do same as previous command for nomad yaml file
nomad_schema_filepath = os.path.normpath(os.path.join(current_dir, nomad_schema_file))

# Logger to print warnings (disregard this)
logger = utils.get_logger(__name__)


# Creating the NOMAD schema YAML file
def create_schema():  # function
    return EntryArchive(
        definitions=Package(
            sections=[Program.m_def, ModelSystem.m_def, Simulation.m_def]
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
molecule_data = data[0]

# And parsing into NOMAD archive
archive = EntryArchive()
simulation = Simulation(
    program=Program(
        name='BIOVIA Materials Studio',
        version='2022',
    ),
    model_method=ModelMethod(
        methods='Semi-Empirical Molecular Orbital Package - VAMP',
    ),
)
archive.m_add_sub_section(EntryArchive.data, simulation)

# Parsing `ModelSystem` as SMILES and other additional strings (using ChemNLP functionalities)
smiles_id = molecule_data.get('Smiles', '')
model_system = ModelSystem(smiles=smiles_id)
simulation.model_system.append(model_system)
model_system.normalize(archive, logger)

# Parsing `Outputs` and the properties inside there
outputs = Outputs(
    total_energy=TotalEnergy(value=molecule_data.get('MSVAMP_TotalEnergy') * ureg.eV),
    electronic_energy=ElectronicEnergy(
        value=molecule_data.get('MSVAMP_ElectronicEnergy') * ureg.eV
    ),
    repulsive_energy=RepulsiveEnergy(
        value=molecule_data.get('MSVAMP_RepulsiveEnergy') * ureg.eV
    ),
    ionization_potential=IonizationPotential(
        value=molecule_data.get('MSVAMP_IonizationPotential') * ureg.eV
    ),
    gap_energy=GapEnergy(
        value_homo=molecule_data.get('MSVAMP_HOMOEnergy') * ureg.eV,
        value_lumo=molecule_data.get('MSVAMP_LUMOEnergy') * ureg.eV,
    ),
    heat_of_formation=HeatOfFormation(
        value=molecule_data.get('MSVAMP_HeatOfFormation')
    ),
    multipole_moment=MultipoleMoment(
        value=molecule_data.get('MSVAMP_TotalDipole'),
        value_dipole=molecule_data.get('MSVAMP_DipoleMoment'),
        # value_quadrupole=molecule_data.get('MSVAMP_QuadrupoleMoment'),
        # value_octupole=molecule_data.get('MSVAMP_OctupoleMoment'),
    ),
)
outputs.gap_energy.extract_gap()  # we extract the diff HOMO - LUMO if is positive
simulation.outputs.append(outputs)
outputs.normalize(archive, logger)


# Enthalpy
data1 = ModelData(enthalpy=data[0].get('MSVAMP_Enthalpy', ''))  #
simulation.model_system.append(data1)
archive.m_add_sub_section(EntryArchive.data, simulation)
# Entropy
data1 = ModelData(entropy=data[0].get('MSVAMP_Entropy', ''))  #
simulation.model_system.append(data1)
archive.m_add_sub_section(EntryArchive.data, simulation)
# Heat Capacity
data1 = ModelData(heatcapacity=data[0].get('MSVAMP_HeatCapacity', ''))  #
simulation.model_system.append(data1)
archive.m_add_sub_section(EntryArchive.data, simulation)
# Zero Point Energy
data1 = ModelData(zeropoint=data[0].get('MSVAMP_ZeroPointEnergy', ''))  #
simulation.model_system.append(data1)
archive.m_add_sub_section(EntryArchive.data, simulation)


# Vibrational Frequencies
archive.m_add_sub_section(EntryArchive.data, simulation)
data1 = ModelData(vibrationalfreq=data[0].get('MSVAMP_VibrationalFrequency'))  #
simulation.model_system.append(data1)
# Vibrational Reduced Mass
archive.m_add_sub_section(EntryArchive.data, simulation)
data1 = ModelData(vibrationalmass=data[0].get('MSVAMP_VibrationalReducedMass'))  #
simulation.model_system.append(data1)

# Vibrational Stength Frequency
archive.m_add_sub_section(EntryArchive.data, simulation)
data1 = ModelData(
    vibrationalintensityfreq=data[0].get('MSVAMP_VibrationalIntensity_Frequency')
)  #
simulation.model_system.append(data1)
# Vibrational Strength
archive.m_add_sub_section(EntryArchive.data, simulation)
data1 = ModelData(
    vibrationalintensity=data[0].get('MSVAMP_VibrationalIntensity_Strength')
)  #
simulation.model_system.append(data1)

# UV-VIS Data -  Electronic Levels
archive.m_add_sub_section(EntryArchive.data, simulation)
data1 = ModelData(
    electroniclevels=data[0].get('MSVAMP_ElectronicLevels').split('\n')
)  #
simulation.model_system.append(data1)

# # Patch
json_archive = archive.m_to_dict()
# Replace the schema reference
json_archive['data']['m_def'] = (
    f'../upload/raw/{os.path.basename(nomad_schema_file)}#/definitions/section_definitions/Simulation'
)

# And saving it to the JSON that we need to upload
with open(nomad_filepath, 'wt') as outfile:
    outfile.write(json.dumps(json_archive, indent=2))
