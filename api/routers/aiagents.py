from pydantic import BaseModel
from typing import List, Optional
from fastapi import APIRouter, status, HTTPException

from api.models import AIAgent
from api.deps import db_dependency, user_dependency

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

@router.get('/', response_model=List[AIAgentResponse])
def get_aiagents(db: db_dependency, user: user_dependency):
  # Filter agents by the authenticated user's ID
  return db.query(AIAgent).filter(AIAgent.user_id == user['id']).all()

@router.get('/{aiagent_id}', response_model=AIAgentResponse)
def get_aiagent(db: db_dependency, user: user_dependency, aiagent_id: int):
  # Filter by both agent ID and user ID to ensure the user owns this agent
  db_aiagent = db.query(AIAgent).filter(
    AIAgent.id == aiagent_id,
    AIAgent.user_id == user['id']
  ).first()
  
  if db_aiagent is None:
      raise HTTPException(status_code=404, detail="AIAgent not found")
  return db_aiagent

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AIAgentResponse)
def create_aiagent(db: db_dependency, user: user_dependency, aiagent: AIAgentCreate):
  # Create the agent with the user_id set to the authenticated user
  db_aiagent = AIAgent(**aiagent.dict(), user_id=user['id'])
  db.add(db_aiagent)
  db.commit()
  db.refresh(db_aiagent)
  return db_aiagent

@router.put("/{aiagent_id}", response_model=AIAgentResponse)
def update_aiagent(db: db_dependency, user: user_dependency, aiagent_id: int, aiagent: AIAgentUpdate):
  # Filter by both agent ID and user ID to ensure the user owns this agent
  db_aiagent = db.query(AIAgent).filter(
    AIAgent.id == aiagent_id,
    AIAgent.user_id == user['id']
  ).first()
  
  if db_aiagent is None:
      raise HTTPException(status_code=404, detail="AIAgent not found")
  
  # Update all fields
  for key, value in aiagent.dict().items():
      setattr(db_aiagent, key, value)
  
  db.commit()
  db.refresh(db_aiagent)
  return db_aiagent

@router.delete("/{aiagent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_aiagent(db: db_dependency, user: user_dependency, aiagent_id: int):
  # Filter by both agent ID and user ID to ensure the user owns this agent
  db_aiagent = db.query(AIAgent).filter(
    AIAgent.id == aiagent_id,
    AIAgent.user_id == user['id']
  ).first()
  
  if db_aiagent is None:
      raise HTTPException(status_code=404, detail="AIAgent not found")
  
  db.delete(db_aiagent)
  db.commit()
  return {"ok": True}

