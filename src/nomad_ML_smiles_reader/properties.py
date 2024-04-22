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

from nomad.metainfo import Quantity, Package
from nomad.metainfo.metainfo import _placeholder_quantity
from nomad.datamodel.data import ArchiveSection


m_package = Package()


class PhysicalProperty(ArchiveSection):
    """
    A base section used to define the physical properties obtained in a simulation, experiment, or in a post-processing
    analysis. The main quantity of the `PhysicalProperty` is `value`, whose instantiation has to be overwritten in the derived classes
    when inheriting from `PhysicalProperty`. It also contains `rank`, to define the tensor rank of the physical property, and
    `variables`, to define the variables over which the physical property varies (see variables.py). This class can also store several
    string identifiers and quantities for referencing and establishing the character of a physical property.
    """

    # * `value` must be overwritten in the derived classes defining its type, unit, and description
    value: Quantity = _placeholder_quantity


class TotalEnergy(PhysicalProperty):
    """ """

    value = Quantity(
        type=np.float64,
        shape=[],
        unit='joule',
        description="""
        Total energy from semiempirical calculation. This value is dependent on the basis selected
        and should not be used as an absolute value.
        """,
    )


class ElectronicEnergy(PhysicalProperty):
    """ """

    value = Quantity(
        type=np.float64,
        shape=[],
        unit='joule',
        description="""
        Balance electron energy from semiempirical calculation.
        """,
    )


class RepulsiveEnergy(PhysicalProperty):
    """ """

    value = Quantity(
        type=np.float64,
        shape=[],
        unit='joule',
        description="""
        Repulsive Energy.
        """,  # FIXME: Add description
    )


class IonizationPotential(PhysicalProperty):
    """ """

    value = Quantity(
        type=np.float64,
        shape=[],
        unit='joule',
        description="""
        Ionization Potential.
        """,  # FIXME: Add description
    )


class GapEnergy(PhysicalProperty):
    """ """

    value_homo = Quantity(
        type=np.float64,
        shape=[],
        unit='joule',
        description="""
        Highest occupied molecular orbital value.
        """,  # FIXME: Add description
    )

    value_lumo = Quantity(
        type=np.float64,
        shape=[],
        unit='joule',
        description="""
        Lowest unoccupied molecular orbital value.
        """,  # FIXME: Add description
    )

    value = Quantity(
        type=np.float64,
        shape=[],
        unit='joule',
        description="""
        Value of the gap of energies. This is calculated as the difference `value_homo - value_lumo`; if the
        `value` is negative, we don't set it.
        """,
    )

    def extract_gap(self) -> None:
        if self.value_homo and self.value_lumo:
            value = self.value_homo - self.value_lumo
            if value.magnitude > 0.0:
                self.value = value


class HeatOfFormation(PhysicalProperty):
    """ """

    value = Quantity(
        type=np.float64,
        shape=[],
        unit='kcal/mol',
        description="""
        Heat of Formation.
        """,  # FIXME: Add description
    )


class MultipoleMoment(PhysicalProperty):
    """ """

    value = Quantity(
        type=np.float64,
        shape=[],
        unit='dimensionless',
        description="""
        Value of the total moment.
        """,
    )

    value_dipole = Quantity(
        type=np.float64,
        shape=[3],
        unit='dimensionless',
        description="""
        Value of the dipole moment.
        """,
    )

    # value_quadrupole = Quantity(
    #     type=np.float64,
    #     shape=[3, 3],
    #     unit='dimensionless',
    #     description="""
    #     Value of the dipole moment.
    #     """,
    # )

    # value_octupole = Quantity(
    #     type=np.float64,
    #     shape=[3, 3, 3, 3],
    #     unit='dimensionless',
    #     description="""
    #     Value of the octupole moment.
    #     """,
    # )


class Enthalpy(PhysicalProperty):
    """ """

    value = Quantity(
        type=np.float64,
        shape=[],
        unit='joule',
        description="""
        Enthalpy.
        """,  # FIXME: Add description
    )


class Entropy(PhysicalProperty):
    """ """

    value = Quantity(
        type=np.float64,
        shape=[],
        unit='joule',
        description="""
        Entropy.
        """,  # FIXME: Add description
    )


class HeatCapacity(PhysicalProperty):
    """ """

    value = Quantity(
        type=np.float64,
        shape=[],
        unit='kcal/mol',
        description="""
        Heat capacity.
        """,  # FIXME: Add description (which specific heat capacity?)
    )


class ZeroPointEnergy(PhysicalProperty):
    """ """

    value = Quantity(
        type=np.float64,
        shape=[],
        unit='joule',
        description="""
        Zero point energy.
        """,  # FIXME: Add description
    )


class ElectronicLevels(PhysicalProperty):
    """ """

    type = Quantity(
        type=str,
        shape=[],
        description="""
        Type of electronic levels. For example, UV-VIS.
        """,
    )

    n_levels = Quantity(
        type=np.int32,
        shape=[],
        description="""
        Number of electronic levels.
        """,
    )

    excited_state = Quantity(
        type=np.int32,
        shape=['n_levels'],
        description="""
        Excited state integer.
        """,
    )

    value = Quantity(
        type=np.float64,
        shape=['n_levels'],
        unit='Hz',
        description="""
        Electronic levels values in frequencies.
        """,
    )

    value_wavelength = Quantity(
        type=np.float64,
        shape=['n_levels'],
        unit='meter',
        description="""
        Electronic levels values in wavelengths.
        """,
    )

    oscillator_strength = Quantity(
        type=np.float64,
        shape=['n_levels'],
        unit='dimensionless',
        description="""
        Electronic levels oscillator strength.
        """,
    )

    transition_type = Quantity(
        type=np.int32,
        shape=['n_levels'],
        description="""
        Transition type of the electronic level.
        """,  # TODO add examples of what this means
    )


class VibrationalModes(PhysicalProperty):
    """ """

    n_modes = Quantity(
        type=np.int32,
        shape=[],
        description="""
        Number of vibrational modes.
        """,
    )

    value = Quantity(
        type=str,
        shape=['n_modes'],
        description="""
        Vibrational modes values.
        """,
    )

    frequency = Quantity(
        type=np.float64,
        shape=['n_modes'],
        unit='Hz',
        description="""
        Vibrational modes frequencies.
        """,
    )

    reduced_mass = Quantity(
        type=np.float64,
        shape=['n_modes'],
        unit='dimensionless',
        description="""
        Vibrational modes reduced masses.
        """,
    )

    raman_intensity = Quantity(
        type=np.float64,
        shape=['n_modes'],
        unit='dimensionless',
        description="""
        Vibrational modes Raman intensities.
        """,
    )


class VibrationalSpectrum(PhysicalProperty):
    """ """

    n_frequencies = Quantity(
        type=np.int32,
        shape=[],
        description="""
        Number of frequencies.
        """,
    )

    frequency = Quantity(
        type=np.float64,
        shape=['n_frequencies'],
        unit='Hz',
        description="""
        Vibrational spectrum frequencies.
        """,
    )

    value = Quantity(
        type=np.float64,
        shape=['n_frequencies'],
        unit='dimensionless',
        description="""
        Vibrational spectrum intensity values.
        """,
    )


m_package.__init_metainfo__()
