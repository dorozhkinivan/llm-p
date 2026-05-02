import httpx
from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    async def chat(self, messages: list[dict[str, str]], temperature: float = 0.7) -> str:
        headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "HTTP-Referer": settings.openrouter_site_url,
            "X-Title": settings.openrouter_app_name,
        }

        payload = {
            "model": settings.openrouter_model,
            "messages": messages,
            "temperature": temperature
        }

        url = f"{settings.openrouter_base_url.rstrip('/')}/chat/completions"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, json=payload, timeout=60.0)
                response.raise_for_status()
            except httpx.HTTPError as e:
                raise ExternalServiceError(f"Ошибка OpenRouter: {str(e)}")

        data = response.json()

        try:
            answer = data["choices"][0]["message"]["content"]
            return answer
        except (KeyError, IndexError):
            raise ExternalServiceError("Неожиданный формат ответа от OpenRouter")
