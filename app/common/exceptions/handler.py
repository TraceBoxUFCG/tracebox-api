from fastapi import Request
from fastapi.responses import JSONResponse
from app.common.exceptions import RecordNotFoundException


async def record_not_found_handler(
    request: Request, exc: RecordNotFoundException
) -> JSONResponse:
    """
    This is a wrapper to the default HTTPException handler of FastAPI.
    This function will be called when a HTTPException is explicitly raised.
    """
    headers = getattr(exc, "headers", None)
    return JSONResponse(
        {"detail": "Entity not found", "code": exc.__class__.__name__},
        status_code=404,
        headers=headers,
    )
