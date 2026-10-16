
import os

import httpx
from bs4 import BeautifulSoup
from tavily import TavilyClient


def search_web(query: str, max_results: int = 5) -> list[dict[str, str]]:
    """Search the web and return structured source records."""
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise RuntimeError(
            "TAVILY_API_KEY is missing. Add it to your .env file."
        )

    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    client = TavilyClient(api_key=api_key)
    response = client.search(
        query=query,
        max_results=max(1, min(max_results, 10)),
        search_depth="basic",
    )

    results = []

    for item in response.get("results", []):
        results.append({
            "title": item.get("title") or "Untitled source",
            "url": item.get("url", ""),
            "snippet": item.get("content", ""),
        })

    return results


def fetch_page_text(url: str, max_chars: int = 18000) -> str:
    """Fetch readable HTML text from a public webpage."""
    if not url.startswith(("http://", "https://")):
        raise ValueError("Only HTTP and HTTPS URLs are supported.")

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; DeepDiveResearch/1.0)"
    }

    with httpx.Client(
        timeout=20.0,
        follow_redirects=True,
        headers=headers,
    ) as client:
        response = client.get(url)
        response.raise_for_status()

    content_type = response.headers.get("content-type", "").lower()
    if "text/html" not in content_type:
        return ""

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup.select(
        "script, style, nav, footer, header, noscript, iframe"
    ):
        tag.decompose()

    return " ".join(soup.stripped_strings)[:max_chars]
