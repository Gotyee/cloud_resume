from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for security in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Replace with your database connection setup
DATABASE = "visit_counter.db"


# Helper function to interact with the database
def get_visit_count() -> int:
    return 3


def increment_visit_count() -> None:
    raise NotImplementedError


@app.get("/visits")
async def read_visits():
    count = get_visit_count()
    return {"count": count}


@app.post("/visits/increment")
async def increment_visits():
    # increment_visit_count()
    count = get_visit_count()
    return {"count": count}
