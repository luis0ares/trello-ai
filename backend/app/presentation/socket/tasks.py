from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from openai import AsyncOpenAI, DefaultAioHttpClient

from app.application.use_cases.task_suggestion import TaskSuggestionUseCase
from app.config.settings import envs

router = APIRouter(prefix="/ws", tags=["WebSockets"])


@router.websocket("/tasks", name="Auto generate tasks with AI")
async def ai_tasks_ws(websocket: WebSocket):
    await websocket.accept()

    open_ai_key = envs.OPENAI_API_KEY
    if not open_ai_key:
        await websocket.close(code=4000, reason="Missing OpenAI API Key")
        return

    async with AsyncOpenAI(
        api_key=open_ai_key,
        http_client=DefaultAioHttpClient(),
    ) as client:
        use_case = TaskSuggestionUseCase(client)
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
                        "details": f"OpenAI request failed: {str(e)}"
                    })
                    continue

        except WebSocketDisconnect:
            ...
        except Exception as e:
            # Unexpected errors: try to notify client and close connection
            try:
                await websocket.send_json({
                    "type": "error",
                    "details": f"Unexpected error: {str(e)}"}
                )
            finally:
                await websocket.close()


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/api/ws/tasks");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/tasks/client")
async def get():
    return HTMLResponse(html)
