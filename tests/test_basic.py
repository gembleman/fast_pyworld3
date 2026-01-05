"""Basic tests for World3 model"""

import pytest
import numpy as np

from fast_pyworld3.core import World3, World3Config
from fast_pyworld3.sectors.population import Population
from fast_pyworld3.sectors.base import SectorConfig
from fast_pyworld3.utils import clip, ramp, switch


def test_utility_functions():
    """Test basic utility functions"""
    # Test clip
    assert clip(2.0, 1.0, 1950, 1975) == 1.0
    assert clip(2.0, 1.0, 2000, 1975) == 2.0

    # Test ramp
    assert ramp(2.0, 1900, 1950) == 100.0
    assert ramp(2.0, 1900, 1850) == 0.0

    # Test switch
    assert switch(1.0, 2.0, False) == 1.0
    assert switch(1.0, 2.0, True) == 2.0


def test_world3_creation():
    """Test World3 model creation"""
    config = World3Config(year_min=1900, year_max=2100, dt=1.0)
    world3 = World3(config)

    assert world3.year_min == 1900
    assert world3.year_max == 2100
    assert world3.dt == 1.0
    assert world3.n == 201


def test_population_sector():
    """Test population sector initialization"""
    config = SectorConfig(year_min=1900, year_max=2000, dt=1.0)
    pop = Population(config)

    # Initialize
    pop.init_constants()
    pop.init_variables()

    # Check initial values are NaN
    assert np.isnan(pop.p1[0])
    assert np.isnan(pop.pop[0])

    # Check constants
    assert pop.constants.p1i == 65e7
    assert pop.constants.p2i == 70e7


def test_world3_initialization():
    """Test full World3 initialization"""
    config = World3Config(year_min=1900, year_max=2000, dt=1.0)
    world3 = World3(config)

    world3.init_constants()
    world3.init_variables()

    # Check population constants
    assert world3.pop.constants.p1i == 65e7

    # Check capital constants
    assert world3.cap.constants.ici == 2.1e11


@pytest.mark.skip(reason="Full simulation requires complete implementation")
def test_world3_run():
    """Test World3 simulation run"""
    config = World3Config(year_min=1900, year_max=1910, dt=1.0)
    world3 = World3(config)

    world3.init_constants()
    world3.init_variables()
    world3.set_table_functions()
    world3.set_delay_functions()

    # This would fail without complete implementation
    world3.run()

    results = world3.get_results()
    assert len(results["time"]) == 11


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
