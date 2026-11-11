from sqlalchemy import Column, Integer, String, Text, ForeignKey, CheckConstraint, UniqueConstraint, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    ratings = relationship("UserMediaRating", back_populates="user")
    favorite_characters = relationship("UserCharacterFavorite", back_populates="user")
    communities = relationship("CommunityMember", back_populates="user")
    messages = relationship("ChatMessage", back_populates="user")

class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    tmdb_id = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    type = Column(String(20), CheckConstraint("type IN ('movie', 'series')"), nullable=False)

    __table_args__ = (UniqueConstraint('tmdb_id', 'type', name='uq_tmdb_type'),)

    ratings = relationship("UserMediaRating", back_populates="media")
    communities = relationship("Community", back_populates="media")

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    tmdb_id = Column(Integer, unique=True)
    name = Column(String(255), nullable=False)

    favorited_by = relationship("UserCharacterFavorite", back_populates="character")

class UserMediaRating(Base):
    __tablename__ = "user_media_ratings"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    media_id = Column(Integer, ForeignKey("media.id", ondelete="CASCADE"), primary_key=True)
    rating = Column(Integer, CheckConstraint("rating >= 1 AND rating <= 10"))

    user = relationship("User", back_populates="ratings")
    media = relationship("Media", back_populates="ratings")

class UserCharacterFavorite(Base):
    __tablename__ = "user_character_favorites"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"), primary_key=True)

    user = relationship("User", back_populates="favorite_characters")
    character = relationship("Character", back_populates="favorited_by")

class Community(Base):
    __tablename__ = "communities"

    id = Column(Integer, primary_key=True, index=True)
    media_id = Column(Integer, ForeignKey("media.id", ondelete="CASCADE"))
    name = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    media = relationship("Media", back_populates="communities")
    members = relationship("CommunityMember", back_populates="community")
    messages = relationship("ChatMessage", back_populates="community")

class CommunityMember(Base):
    __tablename__ = "community_members"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    community_id = Column(Integer, ForeignKey("communities.id", ondelete="CASCADE"), primary_key=True)
    joined_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    user = relationship("User", back_populates="communities")
    community = relationship("Community", back_populates="members")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    community_id = Column(Integer, ForeignKey("communities.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    room_type = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    community = relationship("Community", back_populates="messages")
    user = relationship("User", back_populates="messages")