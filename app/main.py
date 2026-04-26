from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.legaldoc.router import router as legaldoc_router
from app.gitlab.router import router as gitlab_router
from app.rag.router import router as rag_router

load_dotenv()

app = FastAPI(title="Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://projects-showcase-neon.vercel.app",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(legaldoc_router)
app.include_router(gitlab_router)
app.include_router(rag_router)
