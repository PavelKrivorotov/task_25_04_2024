import uvicorn

from app import settings
from app.app import app


if __name__ == '__main__':
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT
    )

