"""Single gateway for every LLM call. Do not instantiate model clients elsewhere."""
from openai import OpenAI
from app.core.config import get_settings


def get_mesh_client() -> OpenAI:
    settings = get_settings()
    if not settings.mesh_api_key or settings.mesh_api_key == "rsk_replace_me":
        raise RuntimeError("MESH_API_KEY is missing. Copy .env.example to .env and add your Mesh key.")
    return OpenAI(base_url=settings.mesh_base_url, api_key=settings.mesh_api_key, timeout=60.0, max_retries=2)


def mesh_chat(system_prompt: str, user_prompt: str, *, temperature: float = 0.1) -> str:
    """All generative model calls must pass through this function."""
    settings = get_settings()
    client = get_mesh_client()
    response = client.chat.completions.create(
        model=settings.mesh_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
    )
    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("Mesh returned an empty model response.")
    return content
