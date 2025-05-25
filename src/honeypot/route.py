from fastapi import FastAPI, Request, Response
import httpx
import uvicorn
import logging

app = FastAPI()

# CONFIG: real server address
REAL_BACKEND = "http://<REAL_SERVER_IP>:8000"

# Setup logger
logging.basicConfig(
    filename="honeypot.log",
    level=logging.INFO,
    format="%(asctime)s - %(client_ip)s - %(message)s",
)


def log_request(client_ip, path, method, headers, body):
    logging.info(
        "",
        extra={
            "client_ip": client_ip,
            "message": f"{method} {path}\nHeaders: {headers}\nBody: {body}\n",
        },
    )


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


if __name__ == "__main__":
    uvicorn.run("honeypot:app", host="0.0.0.0", port=80)
