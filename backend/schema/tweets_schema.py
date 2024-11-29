from pydantic import BaseModel


class TweetSchema(BaseModel):
    tweet_data: str
    tweet_media_ids: list[int]


"""TWEET DATA RESPONSE"""


class TweetUserData(BaseModel):
    id: int
    name: str


class TweetLikeUserData(BaseModel):
    tweet_id: int
    user_id: int


class TweetsData(BaseModel):
    id: int
    content: str
    attachments: list[str]
    author: TweetUserData
    likes: list[TweetLikeUserData]


"""_______________"""


class GetTweetSchemaResponseSchema(BaseModel):
    result: bool
    tweets: list[TweetsData]


class TweetResponseSchema(BaseModel):
    result: bool
    tweet_id: int


class MediaResponseSchema(BaseModel):
    result: bool
    media_id: int
