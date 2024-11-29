from sqlalchemy.orm import Session

from backend.models import Media


class MediaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_media_for_tweet(self, file_path):
        media = Media(file_path=file_path)
        self.db.add(media)
        self.db.commit()
        self.db.refresh(media)

        res = {"result": True, "media_id": media.id}

        return res
