import mysql.connector
import os

# Ścieżka do tymczasowego pliku
CA_CERT_PATH = "/tmp/ca.pem"

# Pobranie zawartości certyfikatu z ENV i zapisanie do pliku
with open(CA_CERT_PATH, "w") as f:
    f.write(os.environ.get("CA_CERT", ""))  # zakładamy, że cert jest w ENV


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_ca=CA_CERT_PATH )

