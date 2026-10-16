
from dotenv import load_dotenv
from app.services.retrieval import search_web, fetch_page_text

load_dotenv()

query = "official WHO artificial intelligence healthcare"
results = search_web(query, max_results=3)

print(f"Found {len(results)} search results.")

for i, result in enumerate(results, start=1):
    print(f"\n--- Result {i} ---")
    print("Title:", result["title"])
    print("URL:", result["url"])
    print("Snippet:", result["snippet"][:250])

if results:
    page_text = fetch_page_text(results[0]["url"])
    print("\nExtracted page text:")
    print(page_text[:500] if page_text else "No readable text extracted.")
