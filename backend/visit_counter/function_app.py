from datetime import datetime

import azure.functions as func
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosResourceNotFoundError
from fastapi import APIRouter, FastAPI, HTTPException

fast_app = FastAPI(root_path="/visit_counter")
router = APIRouter(prefix="/api", tags=["HmmIMightBeAPI"])


endpoint = "https://clpud-resume-glbs.documents.azure.com:443/"
container_id = "cloud_resume_container"
database_id = "cloud_resume_database"
key = "jPyFiP7XYEbZYhLCh5PaJYeP0j7yjndhJ6XjOlRTzakwYKZRPlaYK77tvEY3EKVdZZxyT5vIQlHDACDbFDWrHg=="
partition_key = "/id"
client = CosmosClient(url=endpoint, credential=key)


# @fast_app.on_event("startup")
# async def startup_db_client() -> None:
#     app.client = CosmosClient(url=endpoint, credential=key)
#     db = await app.client.get_database_client(database_id).read()
#     container = await db.get_container_client(container_id).read()


@router.get("/visits")
def get_visit_count() -> dict:
    try:
        client = CosmosClient(url=endpoint, credential=key)
        db = client.get_database_client(database_id)
        container = db.get_container_client(container_id)
        item = next(
            iter(
                container.query_items(
                    query='SELECT * FROM c WHERE c.id="visit_counter"',
                    enable_cross_partition_query=True,
                ),
            ),
        )  # return type makes var unusable in python if not processed in list before

        return {"count": item["count"]}

    except CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Visit counter not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/increment")
def increment_visits():
    try:
        client = CosmosClient(url=endpoint, credential=key)
        db = client.get_database_client(database_id)
        container = db.get_container_client(container_id)

        item = next(
            iter(
                container.query_items(
                    query='SELECT * FROM c WHERE c.id="visit_counter"',
                    enable_cross_partition_query=True,
                ),
            ),
        )
        item["count"] += 1
        item["last_visit_date"] = datetime.now().strftime("%Y-%m-%d")
        container.upsert_item(item)

        return {"success": item}

    except CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Visit counter not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


fast_app.include_router(router)
app = func.AsgiFunctionApp(
    app=fast_app,
    http_auth_level=func.AuthLevel.ANONYMOUS,
)
