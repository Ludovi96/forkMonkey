"""
Shared pytest fixtures for ForkMonkey tests.

This module provides reusable fixtures for testing the genetics,
achievements, storage, and visualizer modules.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Generator, Dict, Any

from src.genetics import (
    GeneticsEngine, MonkeyDNA, Trait, TraitCategory, Rarity
)


# =============================================================================
# Temporary Directory Fixtures
# =============================================================================

@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def temp_monkey_dir(temp_dir: Path) -> Path:
    """Create a temporary monkey_data directory structure."""
    monkey_dir = temp_dir / "monkey_data"
    monkey_dir.mkdir()
    return monkey_dir


# =============================================================================
# DNA Fixtures
# =============================================================================

@pytest.fixture
def sample_dna() -> MonkeyDNA:
    """Generate a random DNA sample for testing."""
    return GeneticsEngine.generate_random_dna()


@pytest.fixture
def gen1_dna() -> MonkeyDNA:
    """Generate a Generation 1 DNA sample."""
    return GeneticsEngine.generate_random_dna(generation=1)


@pytest.fixture
def gen5_dna() -> MonkeyDNA:
    """Generate a Generation 5 DNA sample."""
    return GeneticsEngine.generate_random_dna(generation=5)


@pytest.fixture
def legendary_trait() -> Trait:
    """Create a legendary trait for testing."""
    return Trait(
        category=TraitCategory.SPECIAL,
        value="genesis_blessing",
        rarity=Rarity.LEGENDARY
    )


@pytest.fixture
def common_trait() -> Trait:
    """Create a common trait for testing."""
    return Trait(
        category=TraitCategory.BODY_COLOR,
        value="brown",
        rarity=Rarity.COMMON
    )


@pytest.fixture
def dna_dict(sample_dna: MonkeyDNA) -> Dict[str, Any]:
    """Convert sample DNA to dictionary format."""
    return GeneticsEngine.dna_to_dict(sample_dna)


# =============================================================================
# Stats Fixtures
# =============================================================================

@pytest.fixture
def empty_stats() -> Dict[str, Any]:
    """Empty stats dictionary."""
    return {}


@pytest.fixture
def new_monkey_stats() -> Dict[str, Any]:
    """Stats for a newly created monkey."""
    return {
        "created_at": "2024-01-01",
        "age_days": 0,
        "generation": 1,
        "total_mutations": 0,
        "rarity_score": 0,
        "children_count": 0,
    }


@pytest.fixture
def veteran_monkey_stats() -> Dict[str, Any]:
    """Stats for a well-established monkey."""
    return {
        "created_at": "2024-01-01",
        "age_days": 100,
        "generation": 3,
        "total_mutations": 50,
        "rarity_score": 75,
        "children_count": 5,
        "leaderboard_rank": 10,
    }


@pytest.fixture
def week_old_stats() -> Dict[str, Any]:
    """Stats for a 7-day old monkey."""
    return {
        "created_at": "2024-01-01",
        "age_days": 7,
        "total_mutations": 3,
    }


@pytest.fixture
def month_old_stats() -> Dict[str, Any]:
    """Stats for a 30-day old monkey."""
    return {
        "created_at": "2024-01-01",
        "age_days": 30,
        "total_mutations": 15,
        "rarity_score": 50,
    }


# =============================================================================
# Trait Fixtures
# =============================================================================

@pytest.fixture
def all_trait_categories() -> list:
    """List of all trait categories."""
    return list(TraitCategory)


@pytest.fixture
def all_rarities() -> list:
    """List of all rarity levels."""
    return list(Rarity)


# =============================================================================
# Breeding Fixtures
# =============================================================================

@pytest.fixture
def parent_child_pair(sample_dna: MonkeyDNA) -> tuple:
    """Create a parent-child DNA pair."""
    parent = sample_dna
    child = GeneticsEngine.breed(parent, mutation_rate=0.3)
    return parent, child


@pytest.fixture
def evolved_dna(sample_dna: MonkeyDNA) -> MonkeyDNA:
    """Create an evolved version of sample DNA."""
    return GeneticsEngine.evolve(sample_dna, evolution_strength=0.5)


# =============================================================================
# Multi-Generation Fixtures
# =============================================================================

@pytest.fixture
def three_generations() -> list:
    """Create a 3-generation lineage."""
    gen1 = GeneticsEngine.generate_random_dna(generation=1)
    gen2 = GeneticsEngine.breed(gen1)
    gen3 = GeneticsEngine.breed(gen2)
    return [gen1, gen2, gen3]


# =============================================================================
# Test Markers
# =============================================================================

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "flaky: marks tests that may be flaky"
    )

