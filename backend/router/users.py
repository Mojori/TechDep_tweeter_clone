from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from backend.config.database import get_db
from backend.models import User
from backend.repository.users_repository import UserRepository
from backend.schema.schemas import ErrorSchema, BoolResponseSchema

users_router = APIRouter()


@users_router.post("/TEST/create_user")
def test_user_create(user_name: str, api_key: str, db: Session = Depends(get_db)):
    db_user = User(name=user_name, api_key=api_key)
    db.add(db_user)
    db.commit()
    return db_user


@users_router.get("/TEST/get_user_id_by_api_key")
def get_user_id_by_api_key(api_key: str, db: Session = Depends(get_db)):
    db_user = get_user_by_api_key(api_key, db)
    if db_user:
        return db_user.id
    else:
        return False


@users_router.get("/TEST/get_user_by_id")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        return db_user
    else:
        return False


@users_router.get("/TEST/get_user_by_api_key")
def get_user_by_api_key(api_key: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.api_key == api_key).first()
    if db_user:
        return db_user
    else:
        return False


@users_router.get("/me")
def get_self_user_info(
    api_key: str = Depends(APIKeyHeader(name="api-key")), db=Depends(get_db)
):
    try:
        db_user = get_user_by_api_key(api_key, db)

        user_repo = UserRepository(db)
        res = user_repo.get_user_info(db_user)

        return res

    except Exception as ex:
        res = ErrorSchema(error_type="400", error_message=ex)
        return res


@users_router.get("/{user_id}")
def get_another_user_info(user_id: int, db=Depends(get_db)):
    try:
        db_user = get_user_by_id(user_id, db)

        user_repo = UserRepository(db)
        res = user_repo.get_user_info(db_user)

        return res

    except Exception as ex:
        res = ErrorSchema(error_type="400", error_message=ex)
        return res


@users_router.post("/{user_id}/follow", response_model=BoolResponseSchema)
def follow_user(
    user_id: int,
    api_key: str = Depends(APIKeyHeader(name="api-key")),
    db=Depends(get_db),
):
    try:
        user_repo = UserRepository(db)

        follower_id = get_user_id_by_api_key(api_key, db)

        res = user_repo.follow_user(user_id=user_id, follower_id=follower_id)

        return res

    except Exception as ex:
        res = ErrorSchema(error_type="400", error_message=ex)
        return res


@users_router.delete("/{user_id}/follow", response_model=BoolResponseSchema)
def unfollow_user(
    user_id: int,
    api_key: str = Depends(APIKeyHeader(name="api-key")),
    db=Depends(get_db),
):
    try:
        user_repo = UserRepository(db)

        follower_id = get_user_id_by_api_key(api_key, db)

        res = user_repo.unfollow_user(user_id=user_id, follower_id=follower_id)

        return res

    except Exception as ex:
        res = ErrorSchema(error_type="400", error_message=ex)
        return res
