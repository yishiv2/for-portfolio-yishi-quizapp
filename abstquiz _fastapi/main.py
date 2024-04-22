import os

from agraffe import Agraffe
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.quiz import router as quiz_router
from routes.quiz_sets import router as quiz_sets_router

app = FastAPI()

app.include_router(quiz_router)
app.include_router(quiz_sets_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"])


@app.get("/")
async def read_root():
    return {"message": "Hello, World!!"}


if os.environ.get("gcp") == "yes":
    entry_point = Agraffe.entry_point(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
