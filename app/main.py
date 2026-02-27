from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
from app.modules.pessoas.pessoas_controller import router as pessoas_router

PORT = 3000
app = FastAPI()

class HealthResponse(BaseModel):
    status: str
    date: datetime

@app.get("/", response_model=HealthResponse, tags=["Status"])
def status():
    return HealthResponse(
        date=datetime.now(),
        status= "Alive"
    )

app.include_router(pessoas_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True
    )