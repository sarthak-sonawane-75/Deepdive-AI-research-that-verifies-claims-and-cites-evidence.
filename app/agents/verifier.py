
from app.models import ClaimDraft, ClaimVerdict, EvidenceRecord


def verify_claim(
    claim: ClaimDraft,
    evidence: list[EvidenceRecord],
    *,
    mock: bool = False,
) -> ClaimVerdict:
    """Verify a claim against evidence linked to the claim's cited IDs."""

    evidence_by_id = {item.evidence_id: item for item in evidence}

    cited_evidence = [
        evidence_by_id[evidence_id]
        for evidence_id in claim.evidence_ids
        if evidence_id in evidence_by_id
    ]

    if not cited_evidence:
        return ClaimVerdict(
            claim_id=claim.claim_id,
            verdict="insufficient",
            explanation="No matching evidence was provided for this claim.",
            evidence_ids=[],
        )

    if mock:
        # Deterministic test fixture only; this does not assess truth.
        return ClaimVerdict(
            claim_id=claim.claim_id,
            verdict="supported",
            explanation="Mock verdict for testing the verification pipeline.",
            evidence_ids=[item.evidence_id for item in cited_evidence],
        )

    raise NotImplementedError(
        "Live verification will be connected through Mesh in the next step."
    )
