import asyncio

from application.api.config import APIConfig
from application.api.main import create_app, run_api


async def main() -> None:
    app = create_app()
    await run_api(app, APIConfig())

if __name__ == "__main__":
    asyncio.run(main())
