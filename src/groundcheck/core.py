"""Claim-level evidence matching with a transparent lexical-overlap baseline."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import re

_TOKEN_PATTERN = re.compile(r"[^\W_]+", re.UNICODE)
_SENTENCE_PATTERN = re.compile(r"(?<=[.!?])\s+")
_STOP_WORDS = frozenset(
    "a an and are as at be by for from in is it of on or that the this to was were "
    "will with".split()
)


@dataclass(frozen=True)
class ClaimResult:
    claim: str
    status: str
    score: float
    evidence: str | None


@dataclass(frozen=True)
class GroundingReport:
    supported: int
    needs_review: int
    claims: tuple[ClaimResult, ...]

    def to_dict(self) -> dict:
        return {
            "supported": self.supported,
            "needs_review": self.needs_review,
            "claims": [asdict(claim) for claim in self.claims],
        }


def _tokens(text: str) -> set[str]:
    return {
        token.casefold()
        for token in _TOKEN_PATTERN.findall(text)
        if token.casefold() not in _STOP_WORDS
    }


def _split_claims(answer: str) -> list[str]:
    return [
        sentence.strip()
        for sentence in _SENTENCE_PATTERN.split(answer.strip())
        if sentence.strip()
    ]


def _overlap_score(claim: str, passage: str) -> float:
    claim_tokens = _tokens(claim)
    passage_tokens = _tokens(passage)
    if not claim_tokens or not passage_tokens:
        return 0.0
    return len(claim_tokens & passage_tokens) / len(claim_tokens | passage_tokens)


def check_answer(
    answer: str,
    contexts: list[str],
    *,
    threshold: float = 0.2,
) -> GroundingReport:
    """Match each answer sentence to its best context using Jaccard token overlap.

    This is a screening baseline, not a semantic entailment or truth detector.
    """
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1")
    if not isinstance(answer, str):
        raise TypeError("answer must be a string")
    if not isinstance(contexts, list):
        raise TypeError("contexts must be a list of strings")
    if not all(isinstance(context, str) for context in contexts):
        raise TypeError("each context must be a string")

    results: list[ClaimResult] = []
    for claim in _split_claims(answer):
        best_context: str | None = None
        best_score = 0.0
        for context in contexts:
            score = _overlap_score(claim, context)
            if score > best_score:
                best_context, best_score = context, score
        is_supported = best_context is not None and best_score >= threshold
        results.append(
            ClaimResult(
                claim=claim,
                status="supported" if is_supported else "needs_review",
                score=round(best_score, 4),
                evidence=best_context if is_supported else None,
            )
        )

    supported = sum(result.status == "supported" for result in results)
    return GroundingReport(
        supported=supported,
        needs_review=len(results) - supported,
        claims=tuple(results),
    )
