from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text
from sqlalchemy.orm import relationship

from sqlalchemy import Column, JSON
from sqlalchemy.ext.mutable import MutableList

from .database import Base

workout_routine_association = Table(
    'workout_routine', Base.metadata,
    Column('workout_id', Integer, ForeignKey('workouts.id')),
    Column('routine_id', Integer, ForeignKey('routines.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
class Workout(Base):
    __tablename__ = 'workouts'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, index=True)
    description = Column(String, index=True)
    routines = relationship('Routine', secondary=workout_routine_association, back_populates='workouts')
    
class Routine(Base):
    __tablename__ = 'routines'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String, index=True)
    description = Column(String, index=True)
    workouts = relationship('Workout', secondary=workout_routine_association, back_populates='routines')

class Try(Base):
    __tablename__ = 'tries'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

class AIAgent(Base):
    __tablename__ = 'aiagents'
    id = Column(Integer, primary_key=True, index=True)
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
    
    
Workout.routines = relationship('Routine', secondary=workout_routine_association, back_populates='workouts')