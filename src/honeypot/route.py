import httpx
from fastapi import FastAPI, Request, Response
import os

from dotenv import load_dotenv, dotenv_values
from src.utils.logging_config import get_logger

app = FastAPI()

load_dotenv()
logger = get_logger(__name__)

# CONFIG: real server address
REAL_BACKEND = "http://127.0.0.1:8000"

def get_real_url(host: str, port: str) -> str:
    return "http://" + host + ":" + port

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

    # construct URL
    host = os.getenv("REAL_APP_HOST")
    port = os.getenv("REAL_APP_PORT")
    real_app_url = get_real_url(host, port)

    # Forward to real backend
    async with httpx.AsyncClient() as client:
        try:
            real_response = await client.request(
                method=method,
                url=f"{real_app_url}/{full_path}",
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
