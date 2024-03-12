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

from nomad.metainfo import Package
from nomad.datamodel import EntryArchive

from nomad_ML_smiles_reader.schema import Program, ModelSystem, Simulation


# Defining paths to the file
current_dir = os.path.dirname(os.path.abspath(__file__))
test_file = '../../tests/data/testing_two_molecules.json'
dirname = os.path.dirname(test_file)
basename = os.path.basename(test_file).strip('.json')
nomad_file = f'{dirname}/{basename}_NOMAD.archive.json'
nomad_schema_file = f'{dirname}/{basename}_NOMADschema.archive.yaml'
filepath = os.path.normpath(os.path.join(current_dir, test_file))
nomad_filepath = os.path.normpath(os.path.join(current_dir, nomad_file))
nomad_schema_filepath = os.path.normpath(os.path.join(current_dir, nomad_schema_file))


# Creating the NOMAD schema YAML file
def create_schema():
    return EntryArchive(
        definitions=Package(
            sections=[Program.m_def, ModelSystem.m_def, Simulation.m_def]
        )
    )


# And saving it to the YAML that we need to upload
yaml_schema = create_schema().m_to_dict(with_out_meta=True)
with open(nomad_schema_filepath, 'wt') as outfile:
    outfile.write(yaml.dump(yaml_schema, indent=2))

# Loading JSON data
data = json.load(codecs.open(filepath, 'r', 'utf-8-sig'))

# And parsing into NOMAD archive
archive = EntryArchive()
simulation = Simulation(
    program=Program(
        name='name for your ML sub-program? Or perhaps the name of the software used?',
        version='leave empty if not needed',
    )
)
system = ModelSystem(smiles=data[0].get('Smiles', ''))
simulation.model_system.append(system)
archive.m_add_sub_section(EntryArchive.data, simulation)

# # Patch
json_archive = archive.m_to_dict()
# Replace the schema reference
json_archive['data']['m_def'] = (
    f'../upload/raw/{os.path.basename(nomad_schema_file)}#/definitions/section_definitions/Simulation'
)

# And saving it to the JSON that we need to upload
with open(nomad_filepath, 'wt') as outfile:
    outfile.write(json.dumps(json_archive, indent=2))
