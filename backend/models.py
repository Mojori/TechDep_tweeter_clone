from typing import List

from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from backend.config.database import Base, engine


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(unique=True)

    api_key: Mapped[str]

    tweets: Mapped[List["Tweet"]] = relationship(
        backref="tweets.user_id", cascade="all, delete-orphan"
    )


class Tweet(Base):
    __tablename__ = "tweets"
    id: Mapped[int] = mapped_column(primary_key=True)

    tweet_data: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    medias: Mapped[List["Media"]] = relationship(
        back_populates="tweet", cascade="all, delete-orphan"
    )


class Media(Base):
    __tablename__ = "medias"
    id: Mapped[int] = mapped_column(primary_key=True)

    file_path: Mapped[str]

    tweet_id: Mapped[int] = mapped_column(
        ForeignKey("tweets.id", ondelete="CASCADE"), nullable=True
    )
    tweet: Mapped["Tweet"] = relationship(back_populates="medias")


class Likes(Base):
    __tablename__ = "likes"
    tweet_id: Mapped[int] = mapped_column(
        ForeignKey("tweets.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )


class Follows(Base):
    __tablename__ = "follows"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    follower_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


Base.metadata.create_all(engine)
