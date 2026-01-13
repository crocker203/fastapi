# app/main.py
from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, items, auth

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Pet Project",
    description="A simple pet project with FastAPI and PostgreSQL",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include routers
app.include_router(users.router)
app.include_router(items.router)
app.include_router(auth.router)

@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome to FastAPI Pet Project API"}

@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "healthy"}
