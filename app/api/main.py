from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.core.config import get_settings
from app.core.mesh import mesh_chat
from app.models import ResearchRequest, ResearchResponse
from app.agents.planner import plan_research

ROOT = Path(__file__).resolve().parents[1]
app = FastAPI(title="DeepDive API", version="0.1.0", description="Self-verifying research analyst")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")


@app.get("/health")
def health():
    return {"status": "ok", "app": get_settings().app_name, "llm_gateway": "Mesh API"}


@app.get("/", response_class=HTMLResponse)
def home():
    return (ROOT / "templates" / "index.html").read_text(encoding="utf-8")


@app.post("/api/mesh-test")
def mesh_test():
    try:
        answer = mesh_chat("You are a concise connectivity tester.", "Reply with exactly: Mesh connection successful.", temperature=0)
        return {"status": "ok", "model_response": answer}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Mesh API call failed: {exc}") from exc


@app.post("/api/plan")
def create_plan(request: ResearchRequest):
    try:
        tasks = plan_research(request.question, request.research_depth)
        return {"tasks": [task.model_dump() for task in tasks]}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Planning failed: {exc}") from exc


@app.post("/api/research", response_model=ResearchResponse)
def research_placeholder(request: ResearchRequest):
    # Temporary milestone endpoint: full graph will replace this in the next implementation step.
    return ResearchResponse(run_id="not-started", status="scaffold", message="Mesh connectivity and planning are implemented. Research, verification, and reporting are the next milestones.")
