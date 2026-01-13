from fastapi import FastAPI
from core.router import router
app = FastAPI(title="RESUME analyzer bot")


app.include_router(router)

@app.get("/health")
def get_health():
    return {"status":"Server started"}