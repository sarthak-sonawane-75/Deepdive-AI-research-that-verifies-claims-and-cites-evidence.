from typing import Literal
from pydantic import BaseModel, Field, HttpUrl


class ResearchRequest(BaseModel):
    question: str = Field(min_length=8, max_length=2000)
    research_depth: Literal["quick", "standard", "deep"] = "standard"


class ResearchTask(BaseModel):
    task_id: str
    question: str
    rationale: str
    search_queries: list[str] = Field(default_factory=list)


class SourceRecord(BaseModel):
    source_id: str
    title: str
    url: str
    snippet: str = ""
    extracted_text: str = ""
    source_type: Literal["web", "document"] = "web"
    quality_label: Literal["primary", "reputable_secondary", "other", "unknown"] = "unknown"


class EvidenceRecord(BaseModel):
    evidence_id: str
    source_id: str
    passage: str
    task_id: str


class ClaimDraft(BaseModel):
    claim_id: str
    text: str
    evidence_ids: list[str] = Field(default_factory=list)


class ClaimVerdict(BaseModel):
    claim_id: str
    verdict: Literal["supported", "contradicted", "insufficient"]
    explanation: str
    evidence_ids: list[str] = Field(default_factory=list)


class ResearchResponse(BaseModel):
    run_id: str
    status: str
    message: str
