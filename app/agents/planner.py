import json
from app.core.mesh import mesh_chat
from app.models import ResearchTask

SYSTEM = """You are DeepDive's research planner. Break the user's question into 3-6 narrow, answerable research sub-questions. Return ONLY valid JSON: {\"tasks\":[{\"task_id\":\"T1\",\"question\":\"...\",\"rationale\":\"...\",\"search_queries\":[\"...\"]}]}. Do not answer the research question. Prefer specific, independently verifiable questions. Never invent sources."""


def plan_research(question: str, depth: str = "standard") -> list[ResearchTask]:
    response = mesh_chat(SYSTEM, json.dumps({"question": question, "depth": depth}))
    try:
        payload = json.loads(response)
        tasks = payload["tasks"]
        return [ResearchTask(**task) for task in tasks]
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise RuntimeError(f"Planner returned invalid JSON: {exc}") from exc
