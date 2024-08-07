from fastapi import FastAPI
from app.common.routes.routes import router

app = FastAPI()

app.include_router(router=router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
