from fastapi import FastAPI


def create_app():
    return FastAPI(
        title="Kafka simple chat by youtube",
        docs_url="/api/docs",
        description="A simple kafka ddd",
        debug=True
    )