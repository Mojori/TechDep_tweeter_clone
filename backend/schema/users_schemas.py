from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str


"""User Data Response"""


class UserFollowersInfo(BaseModel):
    follower_id: int
    user_id: int


class UserUserInfo(BaseModel):
    id: int
    name: str
    followers: list[UserFollowersInfo]
    following: list[UserFollowersInfo]


class UserDataSchema(BaseModel):
    result: bool
    user: UserUserInfo


""""""
