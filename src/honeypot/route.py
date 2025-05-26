import httpx
from fastapi import FastAPI, Request, Response

from src.utils.logging_config import get_logger

app = FastAPI()

logger = get_logger(__name__)

# CONFIG: real server address
REAL_BACKEND = "http://127.0.0.1:8000"


def log_request(client_ip, path, method, headers, body):
    logger.info(
        "",
        extra={
            "client_ip": client_ip,
            "log_message": f"{method} {path}\nHeaders: {headers}\nBody: {body}\n",
        },
    )


# it matches all the paths
@app.api_route(
    "/{full_path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"],
)
async def proxy(full_path: str, request: Request):
    client_ip = request.client.host
    method = request.method
    headers = dict(request.headers)
    body = await request.body()

    # Log the request
    log_request(client_ip, full_path, method, headers, body.decode(errors="ignore"))

    # Forward to real backend
    async with httpx.AsyncClient() as client:
        try:
            real_response = await client.request(
                method=method,
                url=f"{REAL_BACKEND}/{full_path}",
                headers=headers,
                content=body,
                timeout=10,
            )
        except httpx.RequestError as e:
            return Response(content=f"Error contacting backend: {e}", status_code=502)

    # Return real response
    return Response(
        content=real_response.content,
        status_code=real_response.status_code,
        headers=dict(real_response.headers),
    )
