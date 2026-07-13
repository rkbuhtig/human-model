"""Executable Human Model Dynamics v0.2 temporal and audit slices.

The package tests type boundaries, transition behavior, and reducer proposal
instrumentation plus an opt-in declared-band proxy comparison. It is not an
empirically calibrated model of human psychology, human accommodation
capacity, morphic load, or qualia.

Public runtime symbols are resolved lazily so importing a detached laboratory
does not bootstrap the Dynamics engine, model, or protocol layers.
"""

from importlib import import_module
from typing import Any


_LAZY_EXPORTS = {
    "DynamicsEngine": (".engine", "DynamicsEngine"),
    "EngineConfig": (".engine", "EngineConfig"),
    "HumanState": (".models", "HumanState"),
    "ScenarioEvent": (".protocol", "ScenarioEvent"),
    "SimulationResult": (".engine", "SimulationResult"),
}

__all__ = [
    "DynamicsEngine",
    "EngineConfig",
    "HumanState",
    "ScenarioEvent",
    "SimulationResult",
]


def __getattr__(name: str) -> Any:
    try:
        module_name, attribute_name = _LAZY_EXPORTS[name]
    except KeyError as error:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from error
    value = getattr(import_module(module_name, __name__), attribute_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted({*globals(), *__all__})
