
from dotenv import load_dotenv

from app.services.research import research_question

load_dotenv()

results = research_question(
    "How is artificial intelligence changing healthcare in India?",
    depth="standard",
    max_results_per_task=2,
)

for task_id, data in results.items():
    print(f"\n{'=' * 50}")
    print(f"Task: {task_id}")

    print(f"Sources: {len(data['sources'])}")
    print(f"Evidence passages: {len(data['evidence'])}")

    for evidence in data["evidence"]:
        source = next(
            s for s in data["sources"]
            if s.source_id == evidence.source_id
        )

        print(f"\nEvidence ID: {evidence.evidence_id}")
        print(f"Source: {source.title}")
        print(f"URL: {source.url}")
        print(f"Passage: {evidence.passage[:300]}")
