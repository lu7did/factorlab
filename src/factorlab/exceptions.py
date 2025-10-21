"""Custom exception hierarchy for factorlab."""

from __future__ import annotations


class FactorlabError(Exception):
    """Base exception for factorlab."""


class ValidationError(FactorlabError):
    """Raised when input validation fails."""


class ComputationError(FactorlabError):
    """Raised when factorial computation fails."""
