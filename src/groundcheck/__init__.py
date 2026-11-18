"""GroundCheck: a lightweight grounding baseline for RAG answers."""

from .core import ClaimResult, GroundingReport, check_answer

__all__ = ["ClaimResult", "GroundingReport", "check_answer"]
