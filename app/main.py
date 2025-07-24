from fastapi import FastAPI
from routers import users, resources
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Rejestracja routerów
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(resources.router, prefix="/resources", tags=["Resources"])

@app.get("/")
def root():
    return {"message": "Gardener API is running"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # lub ["*"] do testów
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)