"""Dependency-free candidate models for HUMAN-DYN-ADEQ-S0.

This package is an initial synthetic benchmark implementation. It is not a
canonical HumanState runtime and contains no evaluator-side hidden source.
"""

from .core import ObservableEpisodePrefix, ObservableReceipt, TrainingExample
from .models import empty_parameter_document, fit_parameters
from .runner import run_model

__all__ = [
    "ObservableEpisodePrefix",
    "ObservableReceipt",
    "TrainingExample",
    "empty_parameter_document",
    "fit_parameters",
    "run_model",
]
