from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, desc
from app.db.models import ChatMessage


class ChatMessageRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessage:
        msg = ChatMessage(user_id=user_id, role=role, content=content)
        self._session.add(msg)
        await self._session.commit()
        await self._session.refresh(msg)
        return msg

    async def get_last_n_messages(self, user_id: int, limit: int) -> list[ChatMessage]:
        if limit <= 0:
            return []

        stmt = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(desc(ChatMessage.created_at))
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        messages = list(result.scalars().all())

        messages.reverse()
        return messages

    async def delete_history(self, user_id: int) -> None:
        stmt = delete(ChatMessage).where(ChatMessage.user_id == user_id)
        await self._session.execute(stmt)
        await self._session.commit()