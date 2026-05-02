from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.db.models import ChatMessage

class ChatUseCase:
    def __init__(self, chat_repo: ChatMessageRepository, llm_client: OpenRouterClient):
        self._chat_repo = chat_repo
        self._llm_client = llm_client

    async def ask(self, user_id: int, prompt: str, system: str | None, max_history: int, temperature: float) -> str:
        messages_for_llm = []

        if system:
            messages_for_llm.append({"role": "system", "content": system})

        history = await self._chat_repo.get_last_n_messages(user_id=user_id, limit=max_history)
        for msg in history:
            messages_for_llm.append({"role": msg.role, "content": msg.content})

        messages_for_llm.append({"role": "user", "content": prompt})

        await self._chat_repo.add_message(user_id=user_id, role="user", content=prompt)

        answer = await self._llm_client.chat(messages=messages_for_llm, temperature=temperature)

        await self._chat_repo.add_message(user_id=user_id, role="assistant", content=answer)

        return answer

    async def get_history(self, user_id: int) -> list[ChatMessage]:
        return await self._chat_repo.get_last_n_messages(user_id=user_id, limit=50)

    async def clear_history(self, user_id: int) -> None:
        await self._chat_repo.delete_history(user_id=user_id)
