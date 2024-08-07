from fastapi import FastAPI
from app.common.exceptions import RecordNotFoundException
from app.common.exceptions.handler import record_not_found_handler
from app.common.routes.routes import router

app = FastAPI()

app.include_router(router=router)
app.add_exception_handler(RecordNotFoundException, record_not_found_handler)


@app.get("/")
def read_root():
    return {"Hello": "World"}
