"""Executable simulation contracts for Human Model Dynamics v0.1.1.

The package tests type boundaries and transition behavior.  It is not an
empirically calibrated model of human psychology or a theory of qualia.
"""

from .engine import DynamicsEngine, EngineConfig, SimulationResult
from .models import HumanState
from .protocol import ScenarioEvent

__all__ = [
    "DynamicsEngine",
    "EngineConfig",
    "HumanState",
    "ScenarioEvent",
    "SimulationResult",
]
