import os
import string
import random

from typing import Annotated

from sqlalchemy.orm import Session

from fastapi import APIRouter, UploadFile, Depends, File

from backend.config.database import get_db
from backend.repository.media_repository import MediaRepository

from backend.schema.schemas import ErrorSchema
from backend.schema.tweets_schema import (
    MediaResponseSchema,
)

medias_router = APIRouter()


def file_name_generator(size=32, chars=string.ascii_lowercase + string.digits):
    return "".join(random.choice(chars) for char in range(size))


@medias_router.post("", response_model=MediaResponseSchema)
def create_media_for_tweet(
    file: Annotated[UploadFile, File()], db: Session = Depends(get_db)
):
    try:
        media_repo = MediaRepository(db)

        file_name = file_name_generator() + ".jpg"
        file_path = f"backend/static/files/{file_name}"
        static_path = "files/" + file_name

        if not os.path.isfile(file_path):
            with open(file_path, "wb") as file_object:
                file_object.write(file.file.read())
            res = media_repo.create_media_for_tweet(file_path=static_path)
            return res
        else:
            return ErrorSchema(error_type="400", error_message="You're really lucky.")

    except Exception as ex:
        res = ErrorSchema(error_type="400", error_message=ex)
        return res
