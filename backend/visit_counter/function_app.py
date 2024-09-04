import azure.functions as func
from fastapi import APIRouter, FastAPI

fast_app = FastAPI(root_path="/visit_counter")
router = APIRouter(prefix="/api", tags=["HmmIMightBeAPI"])


@router.get("/visits")
async def read_visits():
    return {"count": 3}


@router.post("/visits/increment")
async def increment_visits():
    return {"increments"}


fast_app.include_router(router)
app = func.AsgiFunctionApp(
    app=fast_app,
    http_auth_level=func.AuthLevel.ANONYMOUS,
)
