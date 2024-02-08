from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from app.api.api_events import event_router
from app.api.api_users import user_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=event_router, prefix="/events")
app.include_router(router=user_router, prefix="/users")


@app.get("/")
async def root():
    return {"message": "OK"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=9009, use_colors=True)
