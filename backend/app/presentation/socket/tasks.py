from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from openai import AsyncOpenAI, DefaultAioHttpClient

from app.application.use_cases.task_suggestion import TaskSuggestionUseCase
from app.config.settings import envs
from app.config.logging import logger

router = APIRouter(prefix="/ws", tags=["WebSockets"])


@router.websocket("/tasks", name="Auto generate tasks with AI")
async def ai_tasks_ws(websocket: WebSocket):
    await websocket.accept()
    logger.info(f"WebSocket connection accepted.")

    open_ai_key = envs.OPENAI_API_KEY
    if not open_ai_key:
        logger.error("OpenAI API key is missing, closing websocket connection")
        await websocket.close(code=4000, reason="Missing OpenAI API Key")
        return

    async with AsyncOpenAI(
        api_key=open_ai_key,
        http_client=DefaultAioHttpClient(),
    ) as client:
        use_case = TaskSuggestionUseCase(logger, client)
        try:
            while True:
                last_message = await websocket.receive_text()

                try:
                    result = await use_case.execute(last_message)
                    data = result.tasks if result.final else result.message
                    await websocket.send_json({
                        "type": "final" if result.final else "reply",
                        "data": data
                    })

                except RuntimeError as e:
                    await websocket.send_json({
                        "type": "error",
                        "details": "The AI model couldn't process your request. Please try again later."
                    })
                    continue

        except WebSocketDisconnect:
            logger.info("Websocket disconnected due to client disconnect")

        except Exception as err:
            # Unexpected errors: try to notify client and close connection
            try:
                logger.info("Trying to notify client about error...")
                await websocket.send_json({
                    "type": "error",
                    "details": "Closing connection due to unexpected error"
                })
            finally:
                logger.error(
                    f"Closing connection due to unexpected error: {str(err)}")
                logger.error(
                    str(err), exc_info=err, stacklevel=1, stack_info=True)
                await websocket.close()
