import uvicorn
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter, Response, status, Request
from contextlib import asynccontextmanager

from kafka.conf import kafka_client
from api.routes.tariff import tariff_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await kafka_client.start()
    try:
        yield
    finally:
        await kafka_client.stop()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return


@app.exception_handler(Exception)
async def debug_exception_handler(request: Request, exc: Exception):
    import traceback

    return Response(
        content="".join(
            traceback.format_exception(type(exc), value=exc, tb=exc.__traceback__)
        )
    )


router = APIRouter(prefix="/api")
router.include_router(tariff_router, prefix="/tariff")

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
