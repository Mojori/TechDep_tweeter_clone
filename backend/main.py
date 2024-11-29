import uvicorn

from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from router.medias import medias_router
from router.users import users_router
from router.tweets import tweets_router

app = FastAPI()

app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(tweets_router, prefix="/api/tweets", tags=["tweets"])
app.include_router(medias_router, prefix="/api/medias", tags=["medias"])

app.mount("/files", StaticFiles(directory="./backend/static/files"), name="files")
app.mount("/", StaticFiles(directory="./backend/static/ui", html=True), name="ui")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
