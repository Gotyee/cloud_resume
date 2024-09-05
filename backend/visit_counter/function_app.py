from datetime import datetime
from os import environ

import azure.functions as func
from azure.cosmos import ContainerProxy, CosmosClient
from azure.cosmos.exceptions import CosmosResourceNotFoundError
from fastapi import APIRouter, FastAPI, HTTPException

fast_app = FastAPI(root_path="/visit_counter")
router = APIRouter(prefix="/api", tags=["HmmIMightBeAPI"])


# @fast_app.on_event("startup")
# async def startup_db_client() -> None:
#     app.client = CosmosClient(url=endpoint, credential=key)
#     db = await app.client.get_database_client(database_id).read()
#     container = await db.get_container_client(container_id).read()


def _connect_to_container(
    container_id: str = environ["COSMOS_CONTAINER"],
) -> ContainerProxy:
    return {
        "url": environ["COSMOS_ENDPOINT"],
        "COSMOS_KEY": environ["COSMOS_KEY"],
        "COSMOS_DB": environ["COSMOS_DB"],
        "COSMOS_CONTAINER": environ["COSMOS_CONTAINER"],
    }
    client = CosmosClient(
        url=environ["COSMOS_ENDPOINT"],
        credential=environ["COSMOS_KEY"],
    )
    db = client.get_database_client(environ["COSMOS_DB"])
    return db.get_container_client(container_id)


def _query(container: ContainerProxy, query: str) -> dict:
    return next(
        iter(
            container.query_items(
                query=query,
                enable_cross_partition_query=True,
            ),
        ),
        # return type makes var unusable in python if not processed in list before
    )


@router.get("/visits")
def get_visit_count():
    container = _connect_to_container()
    return {"c": container}
    try:
        container = _connect_to_container()
        return {"c": container}
        item = _query(
            container=container,
            query='SELECT * FROM c WHERE c.id="visit_counter"',
        )

        return {"count": item["count"]}

    except CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Visit counter not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/increment")
def increment_visits() -> None:
    try:
        container = _connect_to_container()
        item = _query(
            container=container,
            query='SELECT * FROM c WHERE c.id="visit_counter"',
        )

        item["count"] += 1
        item["last_visit_date"] = datetime.now().strftime("%Y-%m-%d")
        container.upsert_item(item)

        return

    except CosmosResourceNotFoundError:
        raise HTTPException(status_code=404, detail="Visit counter not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


fast_app.include_router(router)
app = func.AsgiFunctionApp(
    app=fast_app,
    http_auth_level=func.AuthLevel.ANONYMOUS,
)
