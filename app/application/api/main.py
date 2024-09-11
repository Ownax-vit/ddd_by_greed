from fastapi import FastAPI
import uvicorn

from application.api.config import APIConfig
from application.api.messages.handlers import router as message_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Kafka simple chat by youtube",
        docs_url="/api/docs",
        description="A simple kafka ddd",
        debug=True,
    )
    app.include_router(router=message_router, prefix="/chat")

    return app


async def run_api(app: FastAPI, api_config: APIConfig) -> None:
    config = uvicorn.Config(app=app, host=api_config.host, port=api_config.port)
    server = uvicorn.Server(config=config)
    await server.serve()
