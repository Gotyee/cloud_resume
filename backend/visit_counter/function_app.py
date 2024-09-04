import azure.functions as func
from azure.cosmos import CosmosClient
from fastapi import APIRouter, FastAPI, exceptions

fast_app = FastAPI(root_path="/visit_counter")
router = APIRouter(prefix="/api", tags=["HmmIMightBeAPI"])


endpoint = "https://clpud-resume-glbs.documents.azure.com:443/"
container_id = "cloud_resume_db"
database_id = "cloud_resume_db_id"
key = "jPyFiP7XYEbZYhLCh5PaJYeP0j7yjndhJ6XjOlRTzakwYKZRPlaYK77tvEY3EKVdZZxyT5vIQlHDACDbFDWrHg=="
partition_key = "/id"
client = CosmosClient(url=endpoint, credential=key)
database = client.get_database_client(database_id)
container = database.get_container_client(container_id)


@router.get("/visits")
async def read_visits() -> str:
    try:
        return container.read_item("visit_counter", partition_key=partition_key)
    except exceptions.CosmosResourceNotFoundError:
        return {"nop"}


@router.post("/increment")
async def increment_visits():
    return {"increments success"}


fast_app.include_router(router)
app = func.AsgiFunctionApp(
    app=fast_app,
    http_auth_level=func.AuthLevel.ANONYMOUS,
)
