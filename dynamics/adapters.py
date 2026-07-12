"""Explicit cross-layer adapters retained by the composition root."""

from __future__ import annotations

from .interfaces import clamp01


def legacy_v01_access_pressure_bridge(protocol_queue_pressure: float) -> float:
    """Preserve the frozen v0.1 queue→Access coupling without normalizing it.

    This bridge is a known descriptive/protocol confound: its value depends on
    the experimental queue limit.  It exists only so v0.1.1 can correct package
    boundaries while retaining the exact v0.1 semantic baseline.  New temporal
    models must replace it with an explicitly modeled access-demand input.
    """

    return clamp01(protocol_queue_pressure)
