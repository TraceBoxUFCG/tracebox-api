from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.common.exceptions import RecordNotFoundException
from app.common.exceptions.handler import record_not_found_handler
from app.common.routes.routes import router

app = FastAPI()

app.include_router(router=router)
app.add_exception_handler(RecordNotFoundException, record_not_found_handler)
add_pagination(app)


@app.get("/")
def read_root():
    return {"Hello": "World"}
