from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import relationship

from sqlalchemy import Column, JSON
from sqlalchemy.ext.mutable import MutableList

from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class AIAgent(Base):
  __tablename__ = 'aiagents'
  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Add this line
  agent_name = Column(String, nullable=False)
  agent_bio = Column(MutableList.as_mutable(JSON), nullable=False)
  agent_twitter = Column(String, nullable=True)
  traits = Column(MutableList.as_mutable(JSON), nullable=False)
  evm_private_key = Column(String, nullable=True)
  solana_private_key = Column(String, nullable=True)
  sonic_private_key = Column(String, nullable=True)
  goat_rpc_provider_url = Column(String, nullable=True)
  goat_wallet_private_key = Column(String, nullable=True)
  monad_private_key = Column(String, nullable=True)
  farcaster_mnemonic = Column(String, nullable=True)
  twitter_consumer_key = Column(String, nullable=True)
  twitter_consumer_secret = Column(String, nullable=True)
  twitter_access_token = Column(String, nullable=True)
  twitter_access_token_secret = Column(String, nullable=True)
  twitter_user_id = Column(String, nullable=True)
  twitter_bearer_token = Column(String, nullable=True)
  discord_token = Column(String, nullable=True)
  allora_api_key = Column(String, nullable=True)
  anthropic_api_key = Column(String, nullable=True)
  openai_api_key = Column(String, nullable=True)
  groq_api_key = Column(String, nullable=True)
  xai_api_key = Column(String, nullable=True)
  together_api_key = Column(String, nullable=True)
  hyperbolic_api_key = Column(String, nullable=True)
  galadriel_api_key = Column(String, nullable=True)
  galadriel_fine_tune_api_key = Column(String, nullable=True)
  eternalai_api_key = Column(String, nullable=True)
  eternalai_api_url = Column(String, nullable=True)
  
  # Add relationship to User model
  user = relationship("User", back_populates="aiagents")
    
User.aiagents = relationship("AIAgent", back_populates="user")