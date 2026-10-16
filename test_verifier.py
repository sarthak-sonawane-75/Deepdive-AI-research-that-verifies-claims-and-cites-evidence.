
from app.agents.verifier import verify_claim
from app.models import ClaimDraft, EvidenceRecord

evidence = EvidenceRecord(
    evidence_id="E-001",
    source_id="S-001",
    passage="The WHO identifies potential benefits and risks of AI in healthcare.",
    task_id="T1",
)

claim = ClaimDraft(
    claim_id="C-001",
    text="AI in healthcare has potential benefits and risks.",
    evidence_ids=["E-001"],
)

verdict = verify_claim(claim, [evidence], mock=True)

print("Claim:", claim.text)
print("Verdict:", verdict.verdict)
print("Explanation:", verdict.explanation)
print("Evidence IDs:", verdict.evidence_ids)

assert verdict.verdict == "supported"
assert verdict.evidence_ids == ["E-001"]

# A claim without usable evidence must not be marked supported.
unsupported_claim = ClaimDraft(
    claim_id="C-002",
    text="A claim without evidence.",
    evidence_ids=["E-MISSING"],
)

missing_verdict = verify_claim(
    unsupported_claim,
    [evidence],
    mock=True,
)

assert missing_verdict.verdict == "insufficient"
print("\nBoth verifier tests passed.")
