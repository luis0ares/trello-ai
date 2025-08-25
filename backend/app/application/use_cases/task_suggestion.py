import json
from typing import List, Literal, TypedDict

from openai import AsyncOpenAI
from openai.types import ChatModel

from app.application.dtos.task_dto import TaskSuggestionDTO
from app.config.tasks_prompt import TASK_SYSTEM_PROMPT, StructuredReply


class _ConversationContent(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str


class TaskSuggestionUseCase:
    def __init__(self, client: AsyncOpenAI,
                 model: ChatModel = "gpt-4o-mini"):
        self.client = client
        self.open_ai_model = model
        self._conversation_history: List[_ConversationContent] = [
            {"role": "system", "content": TASK_SYSTEM_PROMPT}]

    def __try_parse_json(self, text: str) -> List[StructuredReply]:
        try:
            return json.loads(text)
        except Exception:
            return None

    async def execute(self, message: str):
        """
        This function takes the message and process with
        the ai model to get the task suggestion.

        Each interaction is stored in a conversation history.

        :param message: The last message to be processed by the AI.
        :type message: str

        :return: The AI reply as a dataclass object.

        :raise RuntimeError: OpenAI API error.
        """

        self._conversation_history.append(
            {"role": "user", "content": message})

        try:
            completion = await self.client.chat.completions.create(
                model=self.open_ai_model,
                messages=self._conversation_history,
                temperature=0.2,
            )
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {e}")

        # Save AI reply in conversation history
        ai_reply = completion.choices[0].message.content or ""
        if ai_reply:
            self._conversation_history.append(
                {"role": "assistant", "content": ai_reply})

        parsed = self.__try_parse_json(ai_reply)
        if parsed is not None:
            return TaskSuggestionDTO(
                final=True,
                message=None,
                tasks=parsed
            )
        return TaskSuggestionDTO(
            final=False,
            message=ai_reply,
            tasks=None
        )
