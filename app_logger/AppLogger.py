import httpx

from fastapi import FastAPI, Request
from starlette.responses import StreamingResponse


class AppLogger:
    def __init__(self, log_file: str):
        self.log_file = log_file

        with open(self.log_file, "w") as log_file:
            log_file.write("=" * 50 + "\n")
            log_file.write("AppLogger" + "\n")
            log_file.write("=" * 50 + "\n")

    def log(self, message: str):

        with open(self.log_file, "a") as log_file:
            log_file.write(message + "\n")
        print(message)


app = FastAPI(title="LLM API Logger")
logger = AppLogger("llm.log")


@app.post("/chat/completions")
async def chat_completions(request: Request):

    body = await request.body()
    body_str = body.decode("utf-8")
    logger.log(body_str)
    body_json = await request.json()

    logger.log("模型返回")

    async def response_stream():
        async with httpx.AsyncClient() as client:
            response = await client.stream(
                "http://localhost:8000/chat/completions",
                json=body_json,
                headers={
                    "Content-Type": "application/json",
                    "accept": "text/event-stream",
                    "Authorization": request.headers["Authorization"],
                },
            )
            async for chunk in response.aiter_lines():
                logger.log(chunk)
                yield chunk + "\n"

    return StreamingResponse(response_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
