from fastapi import FastAPI
from .routers import note, provider, model, config, upload_router


def create_app() -> FastAPI:
    app = FastAPI(title="BiliNote")
    app.include_router(note.router, prefix="/api")
    app.include_router(provider.router, prefix="/api")
    app.include_router(model.router,prefix="/api")
    app.include_router(config.router,  prefix="/api")
    app.include_router(upload_router.router, prefix="/api")  # ✅ 新增这行
    return app
