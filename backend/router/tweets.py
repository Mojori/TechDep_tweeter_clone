from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader

from backend.config.database import get_db
from backend.repository.tweets_repository import TweetRepository
from backend.router.users import get_user_id_by_api_key
from backend.schema.schemas import ErrorSchema, BoolResponseSchema
from backend.schema.tweets_schema import (
    TweetSchema,
    TweetResponseSchema,
    GetTweetSchemaResponseSchema,
)

tweets_router = APIRouter()


@tweets_router.get("", response_model=GetTweetSchemaResponseSchema)
def get_tweets(db=Depends(get_db)):
    try:
        tweet_repo = TweetRepository(db)
        res = tweet_repo.get_tweets()
        return res
    except Exception as ex:

        res = ErrorSchema(error_type="400", error_message=ex)

        return res


@tweets_router.post("", response_model=TweetResponseSchema)
def create_tweet(
    tweet: TweetSchema,
    api_key: str = Depends(APIKeyHeader(name="api-key")),
    db=Depends(get_db),
):
    try:
        tweet_repo = TweetRepository(db)

        user_id = get_user_id_by_api_key(api_key, db=db)

        res = tweet_repo.create_tweet(tweet=tweet, user_id=user_id)
        return res

    except Exception as ex:

        res = ErrorSchema(error_type="400", error_message=ex)

        return res


@tweets_router.delete("/{tweet_id}", response_model=BoolResponseSchema)
def delete_tweet(tweet_id: int, db=Depends(get_db)):
    try:
        tweet_repo = TweetRepository(db)

        res = tweet_repo.delete_tweet(tweet_id)

        return res

    except Exception as ex:

        res = ErrorSchema(error_type="400", error_message=ex)

        return res


@tweets_router.post("/{tweet_id}/likes", response_model=BoolResponseSchema)
def like_tweet(
    tweet_id: int,
    api_key: str = Depends(APIKeyHeader(name="api-key")),
    db=Depends(get_db),
):
    try:
        tweet_repo = TweetRepository(db)
        user_id = get_user_id_by_api_key(api_key, db)

        res = tweet_repo.like_tweet(user_id=user_id, tweet_id=tweet_id)

        return res
    except Exception as ex:

        res = ErrorSchema(error_type="400", error_message=ex)

        return res


@tweets_router.delete("/{tweet_id}/likes", response_model=BoolResponseSchema)
def unlike_tweet(
    tweet_id: int,
    api_key: str = Depends(APIKeyHeader(name="api-key")),
    db=Depends(get_db),
):
    try:
        tweet_repo = TweetRepository(db)
        user_id = get_user_id_by_api_key(api_key, db)

        res = tweet_repo.unlike_tweet(user_id=user_id, tweet_id=tweet_id)

        return res
    except Exception as ex:

        res = ErrorSchema(error_type="400", error_message=ex)

        return res
