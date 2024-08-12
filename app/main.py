from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.common.exceptions import RecordNotFoundException
from app.common.exceptions.handler import record_not_found_handler
from app.common.routes.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(router=router)
app.add_exception_handler(RecordNotFoundException, record_not_found_handler)
add_pagination(app)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}
