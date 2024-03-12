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

from nomad.metainfo import Section, Quantity, SubSection

from nomad.datamodel import EntryArchive
from nomad.datamodel.data import EntryData
from nomad.datamodel.metainfo.basesections import Entity, Activity

from runschema.run import Program
from runschema.system import System as BaseSystem
from runschema.method import Method as BaseMethod
from runschema.calculation import BaseCalculation


class ModelSystem(BaseSystem):
    """
    Section used to extend the corrent `System` NOMAD base section. This is used because in the
    `System` section (see https://github.com/nomad-coe/nomad-schema-plugin-run/blob/develop/runschema/system.py#L698)
    a concept like `smiles` to describe molecules with strings is not defined.
    """

    m_def = Section()

    smiles = Quantity(
        type=str,
        description="""
        Notation for the structure of molecules following the Simplified Molecular-Input Line-Entry
        System (SMILES), https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system.
        """,
    )


class Simulation(Activity, EntryData):
    m_def = Section()

    program = SubSection(sub_Section=Program.m_def)

    model_system = SubSection(sub_section=ModelSystem.m_def, repeats=True)

    model_method = SubSection(sub_section=BaseMethod.m_def)

    outputs = SubSection(sub_section=BaseCalculation.m_def, repeats=True)


#### START OF THE SCRIPT ####
# Defining paths to the file
current_dir = os.path.dirname(os.path.abspath(__file__))
test_file = '../../tests/data/testing_two_molecules.json'
dirname = os.path.dirname(test_file)
basename = os.path.basename(test_file).strip('.json')
nomad_file = f'{dirname}/{basename}_NOMAD.archive.json'
filepath = os.path.normpath(os.path.join(current_dir, test_file))
nomad_filepath = os.path.normpath(os.path.join(current_dir, nomad_file))

# Loading JSON data
data = json.load(codecs.open(filepath, 'r', 'utf-8-sig'))


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

# Patch
json_archive = archive.m_to_dict()
json_archive['data']['m_def'] = str(Activity().m_def).split(':')[0]

with open(nomad_filepath, 'w') as outfile:
    json.dump(json_archive, outfile)
