from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_connection
from app.auth import get_current_user
from pydantic import BaseModel
router = APIRouter()


class Resource(BaseModel):
    name: str
    description: str
    category: str
    quantity: int
    status: str  # np. Available, Low Stock, Out of Stock

# 🔽 1. Dodaj nowy zasób
@router.post("/")
def create_resource(resource: Resource, db=Depends(get_connection), user=Depends(get_current_user)):
    cursor = db.cursor()
    query = """
        INSERT INTO resources (name, description, category, quantity, status, date_added, last_updated, user_id)
        VALUES (%s, %s, %s, %s, %s, NOW(), NOW(), %s)
    """
    cursor.execute(query, (
        resource.name,
        resource.description,
        resource.category,
        resource.quantity,
        resource.status,
        user["id"]
    ))
    db.commit()
    return {"msg": "Resource added"}

# 🔽 2. Pobierz wszystkie zasoby użytkownika
@router.get("/")
def get_resources(db=Depends(get_connection), user=Depends(get_current_user)):
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM resources WHERE user_id = %s"
    cursor.execute(query, (user["id"],))
    results = cursor.fetchall()
    return results

# 🔽 3. Zaktualizuj zasób
@router.put("/{resource_id}")
def update_resource(resource_id: int, updated: Resource, db=Depends(get_connection), user=Depends(get_current_user)):
    cursor = db.cursor()
    query = """
        UPDATE resources SET name=%s, description=%s, category=%s, quantity=%s, status=%s, last_updated=NOW()
        WHERE id=%s AND user_id=%s
    """
    cursor.execute(query, (
        updated.name,
        updated.description,
        updated.category,
        updated.quantity,
        updated.status,
        resource_id,
        user["id"]
    ))
    db.commit()

    # Jeśli nie zaktualizowano żadnego rekordu
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Resource not found")

    # Pobierz nową datę last_updated z bazy
    cursor.execute("SELECT last_updated FROM resources WHERE id=%s", (resource_id,))
    updated_row = cursor.fetchone()
    cursor.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Resource not found")
    return {"msg": "Resource updated", "last_updated": updated_row[0] }

# 🔽 4. Usuń zasób
@router.delete("/{resource_id}")
def delete_resource(resource_id: int, db=Depends(get_connection), user=Depends(get_current_user)):
    cursor = db.cursor()
    query = "DELETE FROM resources WHERE id = %s AND user_id = %s"
    cursor.execute(query, (resource_id, user["id"]))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Resource not found")
    return {"msg": "Resource deleted"}
