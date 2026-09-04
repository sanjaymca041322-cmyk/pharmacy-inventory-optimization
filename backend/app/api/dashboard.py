from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.repositories.inventory_repository import InventoryRepository
from app.services.inventory_service import InventoryService
router=APIRouter(prefix="/dashboard",tags=["Dashboard"])
@router.get("/summary")
def summary(db:Session=Depends(get_db)): return InventoryService(InventoryRepository(db)).dashboard()
