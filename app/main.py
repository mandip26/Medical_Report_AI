from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import endpoints
from core.config import settings

app = FastAPI(
    title="Medical Report Visualization API",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router, prefix="/api/v1", tags=["extraction"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=8000,
    reload=False,
    )