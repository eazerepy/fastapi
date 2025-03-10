import os
from pydantic import BaseModel
from typing import List, Optional, Any
from fastapi import APIRouter, status, HTTPException
from web3 import Account

from api.models import AIAgent
from api.deps import db_dependency, user_dependency
from api.agent.agent import Agent, process_response
from api.agent.prompt import get_system_prompt

router = APIRouter(prefix="/zerepy", tags=["zerepy"])


openai_agent = Agent(model=os.getenv("OPENAI_MODEL"))


class ZerepyRequest(BaseModel):
    prompt: str
    agent_id: int


class ZerepyResponse(BaseModel):
    status: str
    action: str
    result: Any


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ZerepyResponse)
def zerepy_request(db: db_dependency, user: user_dependency, request: ZerepyRequest):
    # 1 user => pk
    # 2 prompt

    prompt = request.prompt
    print("prompt", prompt)

    print("user", user)

    agent = db.query(AIAgent).filter(AIAgent.id == request.agent_id).first()
    print("agent", agent)

    pk = agent.evm_private_key

    account = Account.from_key(pk)
    address = account.address

    response = openai_agent.structured_call(
        system_prompt=get_system_prompt(agent),
        messages=[
            {
                "role": "user",
                "content": f"""
                helper informations:
                user address is: {address}
                --------------------------------------------------------
                below is the user prompt:
                {prompt}
                """,
            }
        ],
    )
    print(response)

    res = process_response(response, private_key=pk)
    print("res status", res["status"])
    print("res result", res["result"])

    return ZerepyResponse(
        status=res["status"], action=res["action"], result=res["result"]
    )


class ChatMessage(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: str


class ZerepyRequestV2(BaseModel):
    chat_history: List[ChatMessage]
    agent_id: int


@router.post("/v2", status_code=status.HTTP_201_CREATED, response_model=ZerepyResponse)
def zerepy_request_v2(
    db: db_dependency, user: user_dependency, request: ZerepyRequestV2
):
    # 1 user => pk
    # 2 prompt

    print("user", user)

    agent = db.query(AIAgent).filter(AIAgent.id == request.agent_id).first()
    print("agent", agent)

    pk = agent.evm_private_key

    account = Account.from_key(pk)
    address = account.address

    system_prompt = get_system_prompt(agent)

    messages = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in request.chat_history
    ]

    # find last message with role "user" and add a prefix to the content
    last_user_message = next(
        (message for message in messages if message["role"] == "user"), None
    )
    if last_user_message:
        last_user_message["content"] = (
            f"""
            helper informations:
            user address is: {address}
            --------------------------------------------------------
            below is the user prompt:
            {last_user_message['content']}
            """
        )

    print("last user message", last_user_message)
    print("messages", messages)

    response = openai_agent.structured_call(
        system_prompt=get_system_prompt(agent),
        messages=messages,
    )
    print(response)

    res = process_response(response, private_key=pk)
    print("res status", res["status"])
    print("res result", res["result"])

    return ZerepyResponse(
        status=res["status"], action=res["action"], result=res["result"]
    )
