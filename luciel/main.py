from unicodedata import name
from fastapi import FastAPI

import routes.archives as archives
from settings.config import settings


app = FastAPI(name=settings.APP_NAME)
app.include_router(archives.router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
