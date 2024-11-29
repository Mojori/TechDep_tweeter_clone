from sqlalchemy import insert, delete
from sqlalchemy.orm import Session

from backend.models import Follows


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_info(self, db_user):
        followers_db = (
            self.db.query(Follows).filter(Follows.user_id == db_user.id).all()
        )
        following_db = (
            self.db.query(Follows).filter(Follows.follower_id == db_user.id).all()
        )

        res = {
            "result": True,
            "user": {
                "id": db_user.id,
                "name": db_user.name,
                "followers": followers_db,
                "following": following_db,
            },
        }
        return res

    def follow_user(self, user_id: int, follower_id: int):
        stmt = insert(Follows).values(follower_id=follower_id, user_id=user_id)

        self.db.execute(stmt)
        self.db.commit()

        res = {"result": True}

        return res

    def unfollow_user(self, user_id, follower_id):
        stmt = delete(Follows).where(
            Follows.user_id == user_id, Follows.follower_id == follower_id
        )

        self.db.execute(stmt)
        self.db.commit()

        res = {"result": True}

        return res
