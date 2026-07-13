"""Executable Human Model Dynamics v0.2 temporal and audit slices.

The package tests type boundaries, transition behavior, and reducer proposal
instrumentation plus an opt-in declared-band proxy comparison. It is not an
empirically calibrated model of human psychology, human accommodation
capacity, morphic load, or qualia.
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
