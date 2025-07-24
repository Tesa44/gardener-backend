from fastapi import FastAPI
from app.routers import users, resources
from fastapi.middleware.cors import CORSMiddleware
import os


CA_CERT_PATH = "/tmp/ca.pem"

# Pobranie zawartości certyfikatu z ENV i zapisanie do pliku
with open(CA_CERT_PATH, "w") as f:
    f.write(os.environ.get("DB_SSL_CA", ""))

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