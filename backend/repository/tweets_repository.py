from sqlalchemy import desc, insert, delete
from sqlalchemy.orm import Session

from backend.models import Tweet, Media, Likes
from backend.router.users import get_user_by_id
from backend.schema.tweets_schema import TweetSchema


class TweetRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_tweets(self):
        tweets_db = self.db.query(Tweet).order_by(desc(Tweet.id))

        res = {"result": True, "tweets": []}

        for tweet_db in tweets_db:
            user_db = get_user_by_id(tweet_db.user_id, self.db)

            medias_filepath_list = self.db.scalars(
                self.db.query(Media.file_path).filter(Media.tweet_id == tweet_db.id)
            ).all()

            likes_db = self.db.query(Likes).filter(Likes.tweet_id == tweet_db.id).all()

            tweet = {
                "id": tweet_db.id,
                "content": tweet_db.tweet_data,
                "attachments": medias_filepath_list,
                "author": {"id": user_db.id, "name": user_db.name},
                "likes": likes_db,
            }

            res["tweets"].append(tweet)

        return res

    def create_tweet(self, tweet: TweetSchema, user_id: int):
        db_tweet = Tweet(tweet_data=tweet.tweet_data, user_id=user_id)

        self.db.add(db_tweet)
        self.db.commit()
        self.db.refresh(db_tweet)

        for media_id in tweet.tweet_media_ids:
            media_db = (
                self.db.query(Media)
                .filter(Media.id == media_id)
                .filter(Media.tweet_id == None)
            )

            if media_db:
                media_db.update({"tweet_id": db_tweet.id})
            else:
                pass

        self.db.commit()

        res = {"result": True, "tweet_id": db_tweet.id}

        return res

    def delete_tweet(self, tweet_id: int):
        tweet_db = self.db.query(Tweet).filter(Tweet.id == tweet_id)

        tweet_db.delete()
        self.db.commit()

        res = {"result": True}

        return res

    def like_tweet(self, user_id: int, tweet_id: int):
        stmt = insert(Likes).values(tweet_id=tweet_id, user_id=user_id)

        self.db.execute(stmt)
        self.db.commit()

        res = {"result": True}

        return res

    def unlike_tweet(self, user_id, tweet_id):
        stmt = delete(Likes).where(Likes.tweet_id == tweet_id, Likes.user_id == user_id)

        self.db.execute(stmt)
        self.db.commit()

        res = {"result": True}

        return res
