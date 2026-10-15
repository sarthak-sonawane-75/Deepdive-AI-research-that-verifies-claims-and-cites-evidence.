"""Web and uploaded-document retrieval helpers. Search results are untrusted input."""
from __future__ import annotations
import re
import httpx
from bs4 import BeautifulSoup


def search_web(query: str, max_results: int = 5) -> list[dict[str, str]]:
    """DuckDuckGo HTML fallback search. For production, swap in an official search API."""
    from urllib.parse import quote_plus
    url = "https://html.duckduckgo.com/html/?q=" + quote_plus(query)
    headers = {"User-Agent": "DeepDiveResearchBot/0.1 (educational research prototype)"}
    with httpx.Client(timeout=20.0, follow_redirects=True, headers=headers) as client:
        response = client.get(url)
        response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    results: list[dict[str, str]] = []
    for item in soup.select(".result")[:max_results]:
        link = item.select_one("a.result__a")
        snippet = item.select_one(".result__snippet")
        if link and link.get("href"):
            results.append({"title": link.get_text(" ", strip=True), "url": link["href"], "snippet": snippet.get_text(" ", strip=True) if snippet else ""})
    return results


def fetch_page_text(url: str, max_chars: int = 18000) -> str:
    """Fetch a public web page and extract readable text; does not execute page scripts."""
    with httpx.Client(timeout=20.0, follow_redirects=True, headers={"User-Agent": "Mozilla/5.0 DeepDive/0.1"}) as client:
        response = client.get(url)
        response.raise_for_status()
    content_type = response.headers.get("content-type", "")
    if "text/html" not in content_type:
        return ""
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()
    text = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
    return text[:max_chars]
