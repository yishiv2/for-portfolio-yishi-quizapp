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

# import yaml
# @app.get("/openapi.yaml", include_in_schema=False)
# async def get_openapi_yaml():
#     from fastapi.openapi.utils import get_openapi
#     openapi_schema = get_openapi(
#         title="My API", version="1.0.0", routes=app.routes)
#     yaml_schema = yaml.dump(openapi_schema)
#     return yaml_schema


if os.environ.get("gcp") == "yes":
    entry_point = Agraffe.entry_point(app)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
