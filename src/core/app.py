from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .router import core_router
from src.auth.router import auth_router,user_router
from src.auth.seed import auth_dev_router
from src.rbac.router import rbac_router
from src.rbac.seed import rbac_dev_router
from src.libratech.router import libra_router
from src.libratech.seed import dev_router


@asynccontextmanager
async def lifespan(application: FastAPI):
    # startup
    yield
    # shutdown


app = FastAPI(lifespan=lifespan,
              )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://{settings.run.host}:{settings.run.port}", f"http://localhost:{settings.run.port}"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(core_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(rbac_router)
app.include_router(libra_router)
app.include_router(rbac_dev_router)
app.include_router(dev_router)
app.include_router(auth_dev_router)

