
from uuid import uuid4

from app.agents.planner import plan_research
from app.models import EvidenceRecord, ResearchTask, SourceRecord
from app.services.retrieval import fetch_page_text, search_web


def research_task(
    task: ResearchTask,
    max_results: int = 3,
) -> tuple[list[SourceRecord], list[EvidenceRecord]]:
    """Retrieve sources and create evidence linked to each source."""
    sources: list[SourceRecord] = []
    evidence: list[EvidenceRecord] = []
    seen_urls: set[str] = set()

    for query in task.search_queries:
        if len(sources) >= max_results:
            break

        results = search_web(
            query,
            max_results=max_results - len(sources),
        )

        for result in results:
            url = result.get("url", "").strip()

            if not url or url in seen_urls:
                continue

            seen_urls.add(url)

            source_id = f"S-{uuid4().hex[:8]}"
            snippet = result.get("snippet", "")

            source = SourceRecord(
                source_id=source_id,
                title=result.get("title") or "Untitled source",
                url=url,
                snippet=snippet,
                source_type="web",
            )
            sources.append(source)

            # A page may block automated requests. Keep its search snippet.
            try:
                page_text = fetch_page_text(url, max_chars=18000)
            except Exception:
                page_text = ""

            source.extracted_text = page_text

            passage = page_text.strip() or snippet.strip()

            if passage:
                evidence.append(
                    EvidenceRecord(
                        evidence_id=f"E-{uuid4().hex[:8]}",
                        source_id=source_id,
                        passage=passage[:2000],
                        task_id=task.task_id,
                    )
                )

            if len(sources) >= max_results:
                break

    return sources, evidence


def research_question(
    question: str,
    depth: str = "standard",
    max_results_per_task: int = 3,
) -> dict[str, dict[str, list]]:
    """Plan a question and collect sources and evidence for each task."""
    tasks = plan_research(question, depth=depth, mock=True)
    output = {}

    for task in tasks:
        sources, evidence = research_task(task, max_results_per_task)
        output[task.task_id] = {
            "sources": sources,
            "evidence": evidence,
        }

    return output
