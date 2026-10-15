# DeepDive — Self-Verifying Research Analyst

DeepDive is a research system designed to produce claim-level cited reports. Its core rule is that a citation is not sufficient by itself: the cited passage must be checked against the claim.

## Current milestone

This starter currently includes:
- FastAPI backend and custom HTML/CSS/JS frontend.
- A centralized Mesh API client (`app/core/mesh.py`). All LLM calls must use `mesh_chat` and the OpenAI-compatible Mesh endpoint.
- A planner agent that returns structured research tasks.
- Initial web search/page-fetch and PDF/DOCX/TXT/Markdown extraction helpers.
- Health endpoint and starter test.

The full research orchestration, evidence persistence, claim verifier, retry loop, report synthesis and benchmark are the next milestones. Do not describe these as complete until implemented and tested.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set `MESH_API_KEY` to your real Mesh key. Never commit `.env`.

Run the app from the project root:

```bash
uvicorn app.api.main:app --reload
```

Open http://127.0.0.1:8000. API docs are at http://127.0.0.1:8000/docs. Test Mesh connectivity with `POST /api/mesh-test`.

## Environment variables

- `MESH_API_KEY`: required Mesh key (`rsk_...`).
- `MESH_BASE_URL`: defaults to `https://api.meshapi.ai/v1`.
- `MESH_MODEL`: defaults to `openai/gpt-4o`; choose a model supported by your Mesh account.
- `MAX_RESEARCH_ROUNDS`: maximum verification-driven research retries.
- `MIN_VERIFIED_CLAIMS`: minimum claim target before a report can be considered sufficiently supported.

## Non-negotiable architecture rule

Every generative model call must route through Mesh API. Import `mesh_chat` from `app.core.mesh` for LLM calls. Do not create direct OpenAI, Anthropic, Gemini, or other model clients elsewhere in the codebase. Web search and deterministic parsing are tools, not LLM calls.

## Planned graph

`plan -> research -> draft_claims -> verify -> (research if coverage is weak and retries remain) -> synthesize -> audit/report`

Claims will be stored atomically with evidence IDs. Unsupported claims will be rejected or marked unverified, and contradictions will remain visible. Evaluation metrics will be reported only after the benchmark has actually run.

## Security

Never commit `.env`, API keys, uploaded private documents, or private user data. Configure `MESH_API_KEY` and `SUBMISSION_TOKEN` as GitHub Actions repository secrets for the hackathon checks.
