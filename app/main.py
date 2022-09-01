from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from app.route import mongo
from app.config import settings
from app.config.mongo import db

app = FastAPI()


@app.on_event("shutdown")
def shutdown_event():
    print("Disconnecting Mongo....")
    client, data = db()
    client.close()
    print("ShutDown")


@app.get("/", include_in_schema=False)
def redirect():
    return RedirectResponse("/docs")


app.include_router(mongo.app, prefix="/mongo", tags=['mongo'])

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
