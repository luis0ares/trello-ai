from collections import defaultdict
import json
from typing import Dict, List, Literal, TypedDict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from openai import AsyncOpenAI, DefaultAioHttpClient
from uuid import UUID

from app.config.settings import envs
from app.presentation.socket.tasks_prompt import TASK_SYSTEM_PROMPT


class ConversationContent(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str


# TODO: move to redis or other storage to persist conversations
conversations: Dict[str, List[ConversationContent]] = defaultdict(list)
router = APIRouter(prefix="/ws/tasks", tags=["Tasks"])


def get_conversation(session_id: str) -> List[ConversationContent]:
    return [{"role": "system",
             "content": TASK_SYSTEM_PROMPT}] + conversations[session_id]

def try_parse_json(text: str):
    try:
        return json.loads(text)
    except:
        return None


@router.websocket("/{session_id}", name="Auto generate tasks with AI")
async def ai_tasks_ws(websocket: WebSocket, session_id: UUID):
    await websocket.accept()

    session_id = str(session_id)
    open_ai_key = envs.OPENAI_API_KEY
    if not open_ai_key:
        await websocket.close(code=4000, reason="Missing OpenAI API Key")
        return

    # TODO: move to a use case
    async with AsyncOpenAI(
        api_key=open_ai_key,
        http_client=DefaultAioHttpClient(),
    ) as client:
        try:
            while True:
                last_user_message = await websocket.receive_text()
                conversations[session_id].append(
                    {"role": "user", "content": last_user_message})
                messages = get_conversation(session_id)

                try:
                    completion = await client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=messages,
                        temperature=0.2,
                    )
                except Exception as e:
                    # Send an error payload to the client
                    await websocket.send_json({
                        "type": "error",
                        "error": f"OpenAI request failed: {str(e)}"
                    })
                    # Do not break; let the client continue if they want
                    continue

                # Save AI reply in history
                ai_reply = completion.choices[0].message.content or ""
                conversations[session_id].append(
                    {"role": "assistant", "content": ai_reply})
                
                # If the AI produced JSON, send it as a structured event too
                parsed = try_parse_json(ai_reply)
                if parsed is not None:
                    await websocket.send_json({
                        "type": "structured",
                        "data": parsed
                    })
                else:
                    # Normal AI message
                    await websocket.send_json({
                        "type": "assistant",
                        "text": ai_reply
                    })

        except WebSocketDisconnect:
            # Cleanup when the client disconnects
            conversations.pop(session_id, None)
        except Exception as e:
            # Unexpected errors: notify client and cleanup
            try:
                await websocket.send_json({"type": "error", "details": str(e)})
            finally:
                conversations.pop(session_id, None)
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
            var ws = new WebSocket("ws://localhost:8000/api/ws/tasks/3453ef39-1137-4fb2-9fd3-c4e412a89951");
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


@router.get("/client")
async def get():
    return HTMLResponse(html)