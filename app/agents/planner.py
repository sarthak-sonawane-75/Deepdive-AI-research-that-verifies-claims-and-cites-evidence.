
import json
import os

from app.core.mesh import mesh_chat
from app.models import ResearchTask

SYSTEM = """
You are DeepDive's research planner.

Break the user's research question into 3-6 narrow,
answerable, independently verifiable subquestions.

Return ONLY valid JSON in this format:
{
  "tasks": [
    {
      "task_id": "T1",
      "question": "A specific research question",
      "rationale": "Why this question matters",
      "search_queries": ["search phrase 1", "search phrase 2"]
    }
  ]
}

Do not answer the research question.
Do not invent sources or claim that research has already been performed.
"""


def _validate_tasks(payload: dict) -> list[ResearchTask]:
    if not isinstance(payload, dict):
        raise ValueError("Response must be a JSON object.")

    raw_tasks = payload.get("tasks")

    if not isinstance(raw_tasks, list) or not 3 <= len(raw_tasks) <= 6:
        raise ValueError("Planner must return between 3 and 6 tasks.")

    tasks = [ResearchTask(**task) for task in raw_tasks]

    for task in tasks:
        if not task.question.strip():
            raise ValueError("Task questions cannot be empty.")
        if not task.rationale.strip():
            raise ValueError("Task rationales cannot be empty.")
        if not task.search_queries or not any(
            query.strip() for query in task.search_queries
        ):
            raise ValueError("Every task needs a search query.")

    ids = [task.task_id for task in tasks]
    if len(ids) != len(set(ids)):
        raise ValueError("Task IDs must be unique.")

    return tasks


def plan_research(
    question: str,
    depth: str = "standard",
    *,
    mock: bool = False,
) -> list[ResearchTask]:
    question = question.strip()

    if len(question) < 8:
        raise ValueError("Research question must contain at least 8 characters.")

    if len(question) > 2000:
        raise ValueError("Research question cannot exceed 2000 characters.")

    if depth not in {"quick", "standard", "deep"}:
        raise ValueError("Depth must be quick, standard, or deep.")

    if mock:
        payload = {
            "tasks": [
                {
                    "task_id": "T1",
                    "question": f"What is the current state of {question}?",
                    "rationale": "Establish the relevant background.",
                    "search_queries": [question + " overview"],
                },
                {
                    "task_id": "T2",
                    "question": f"What evidence supports the main findings about {question}?",
                    "rationale": "Identify verifiable findings.",
                    "search_queries": [question + " research evidence"],
                },
                {
                    "task_id": "T3",
                    "question": f"What limitations or counterarguments exist regarding {question}?",
                    "rationale": "Identify uncertainty and opposing evidence.",
                    "search_queries": [question + " limitations criticism"],
                },
            ]
        }
    else:
        response = mesh_chat(
            SYSTEM,
            json.dumps({"question": question, "depth": depth}),
            temperature=0.1,
        )

        try:
            payload = json.loads(response)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"Planner returned invalid JSON: {exc}"
            ) from exc

    try:
        return _validate_tasks(payload)
    except (ValueError, TypeError) as exc:
        raise RuntimeError(f"Planner returned invalid tasks: {exc}") from exc
