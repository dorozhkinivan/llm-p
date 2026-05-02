from pydantic import BaseModel, Field, ConfigDict


class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Текст запроса пользователя")
    system: str | None = Field(default=None, description="Системная инструкция для LLM")
    max_history: int = Field(default=10, ge=0, description="Сколько предыдущих сообщений использовать как контекст")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0,
                               description="Креативность модели (0.0 - точная, 1.0+ - креативная)")


class ChatResponse(BaseModel):
    answer: str


class ChatMessagePublic(BaseModel):
    id: int
    role: str
    content: str

    model_config = ConfigDict(from_attributes=True)
