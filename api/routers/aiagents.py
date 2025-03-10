from pydantic import BaseModel
from typing import List, Optional
from fastapi import APIRouter, status, HTTPException
from datetime import datetime

from api.models import AIAgent, Conversation, Message
from api.deps import db_dependency, user_dependency

router = APIRouter(prefix="/aiagents", tags=["aiagents"])

router = APIRouter(
    prefix='/aiagents',
    tags=['aiagents']
)

class AIAgentBase(BaseModel):
    agent_name: str
    agent_bio: List[str]
    agent_twitter: Optional[str] = None
    traits: List[str]
    evm_private_key: Optional[str] = None
    solana_private_key: Optional[str] = None
    sonic_private_key: Optional[str] = None
    goat_rpc_provider_url: Optional[str] = None
    goat_wallet_private_key: Optional[str] = None
    monad_private_key: Optional[str] = None
    farcaster_mnemonic: Optional[str] = None
    twitter_consumer_key: Optional[str] = None
    twitter_consumer_secret: Optional[str] = None
    twitter_access_token: Optional[str] = None
    twitter_access_token_secret: Optional[str] = None
    twitter_user_id: Optional[str] = None
    twitter_bearer_token: Optional[str] = None
    discord_token: Optional[str] = None
    allora_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    xai_api_key: Optional[str] = None
    together_api_key: Optional[str] = None
    hyperbolic_api_key: Optional[str] = None
    galadriel_api_key: Optional[str] = None
    galadriel_fine_tune_api_key: Optional[str] = None
    eternalai_api_key: Optional[str] = None
    eternalai_api_url: Optional[str] = None


class AIAgentCreate(AIAgentBase):
    pass


class AIAgentUpdate(AIAgentBase):
    pass


class AIAgentResponse(AIAgentBase):
    id: int

    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    role: str
    content: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ConversationBase(BaseModel):
    agent_id: int

class ConversationCreate(ConversationBase):
    pass

class ConversationResponse(ConversationBase):
    id: int
    created_at: datetime
    messages: List[MessageResponse] = []

    class Config:
        orm_mode = True


@router.get("/", response_model=List[AIAgentResponse])
def get_aiagents(db: db_dependency, user: user_dependency):
    # Filter agents by the authenticated user's ID
    return db.query(AIAgent).filter(AIAgent.user_id == user["id"]).all()


@router.get("/{aiagent_id}", response_model=AIAgentResponse)
def get_aiagent(db: db_dependency, user: user_dependency, aiagent_id: int):
    # Filter by both agent ID and user ID to ensure the user owns this agent
    db_aiagent = (
        db.query(AIAgent)
        .filter(AIAgent.id == aiagent_id, AIAgent.user_id == user["id"])
        .first()
    )

    if db_aiagent is None:
        raise HTTPException(status_code=404, detail="AIAgent not found")
    return db_aiagent


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AIAgentResponse)
def create_aiagent(db: db_dependency, user: user_dependency, aiagent: AIAgentCreate):
    # Create the agent with the user_id set to the authenticated user
    db_aiagent = AIAgent(**aiagent.dict(), user_id=user["id"])
    db.add(db_aiagent)
    db.commit()
    db.refresh(db_aiagent)
    return db_aiagent


@router.put("/{aiagent_id}", response_model=AIAgentResponse)
def update_aiagent(db: db_dependency, user: user_dependency, aiagent_id: int, aiagent: AIAgentUpdate):
    db_aiagent = db.query(AIAgent).filter(
        AIAgent.id == aiagent_id,
        AIAgent.user_id == user['id']
    ).first()
    
    if db_aiagent is None:
        raise HTTPException(status_code=404, detail="AIAgent not found")
    
    for key, value in aiagent.dict().items():
        setattr(db_aiagent, key, value)
    
    db.commit()
    db.refresh(db_aiagent)
    return db_aiagent


@router.delete("/{aiagent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_aiagent(db: db_dependency, user: user_dependency, aiagent_id: int):
    db_aiagent = db.query(AIAgent).filter(
        AIAgent.id == aiagent_id,
        AIAgent.user_id == user['id']
    ).first()
    
    if db_aiagent is None:
        raise HTTPException(status_code=404, detail="AIAgent not found")
    
    db.delete(db_aiagent)
    db.commit()
    return {"ok": True}

@router.post("/{aiagent_id}/conversations", status_code=status.HTTP_201_CREATED, response_model=ConversationResponse)
def create_conversation(db: db_dependency, user: user_dependency, aiagent_id: int, conversation: ConversationCreate):
    db_aiagent = db.query(AIAgent).filter(
        AIAgent.id == aiagent_id,
        AIAgent.user_id == user['id']
    ).first()
    
    if db_aiagent is None:
        raise HTTPException(status_code=404, detail="AIAgent not found")
    
    conversation_data = conversation.dict()
    conversation_data['user_id'] = user['id']
    conversation_data['agent_id'] = aiagent_id
    
    db_conversation = Conversation(**conversation_data)
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

@router.get("/{aiagent_id}/conversations", response_model=List[ConversationResponse])
def get_conversations(db: db_dependency, user: user_dependency, aiagent_id: int):
    db_aiagent = db.query(AIAgent).filter(
        AIAgent.id == aiagent_id,
        AIAgent.user_id == user['id']
    ).first()
    
    if db_aiagent is None:
        raise HTTPException(status_code=404, detail="AIAgent not found")
    
    return db.query(Conversation).filter(
        Conversation.agent_id == aiagent_id,
        Conversation.user_id == user['id']
    ).all()

@router.post("/{aiagent_id}/conversations/{conversation_id}/messages", status_code=status.HTTP_201_CREATED, response_model=MessageResponse)
def create_message(db: db_dependency, user: user_dependency, aiagent_id: int, conversation_id: int, message: MessageCreate):
    db_conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.agent_id == aiagent_id,
        Conversation.user_id == user['id']
    ).first()
    
    if db_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    db_message = Message(**message.dict(), conversation_id=conversation_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@router.get("/{aiagent_id}/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
def get_messages(db: db_dependency, user: user_dependency, aiagent_id: int, conversation_id: int):
    db_conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id,
        Conversation.agent_id == aiagent_id,
        Conversation.user_id == user['id']
    ).first()
    
    if db_conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).all()
