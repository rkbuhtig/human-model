"""Executable Human Model Dynamics v0.2 temporal and audit slices.

The package tests type boundaries, transition behavior, and reducer proposal
instrumentation.  It is not an empirically calibrated model of human
psychology or a theory of qualia.
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
