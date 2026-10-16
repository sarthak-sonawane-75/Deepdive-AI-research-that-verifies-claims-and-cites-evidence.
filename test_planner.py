
from app.agents.planner import plan_research

tasks = plan_research(
    "How is artificial intelligence changing healthcare in India?",
    depth="standard",
    mock=True,
)

print(f"Number of tasks: {len(tasks)}")

for task in tasks:
    print(f"\n{task.task_id}: {task.question}")
    print(f"Reason: {task.rationale}")
    print(f"Search queries: {task.search_queries}")
