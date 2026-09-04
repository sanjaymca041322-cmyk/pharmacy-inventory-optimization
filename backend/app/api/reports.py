from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.repositories.inventory_repository import InventoryRepository
from app.services.inventory_service import InventoryService
from app.exports.report_exporter import to_excel,to_csv

router=APIRouter(prefix="/reports",tags=["Reports"])

def service(db:Session): return InventoryService(InventoryRepository(db))

@router.get("/reorder")
def reorder(db:Session=Depends(get_db)): return service(db).reorder()
@router.get("/excess")
def excess(db:Session=Depends(get_db)): return service(db).excess()
@router.get("/near-expiry")
def near_expiry(db:Session=Depends(get_db)): return service(db).near_expiry()
@router.get("/branches")
def branches(db:Session=Depends(get_db)): return service(db).branch_summary()

@router.get("/export/{report_name}")
def export_report(report_name:str,format:str=Query('xlsx',pattern='^(xlsx|csv)$'),db:Session=Depends(get_db)):
    svc=service(db); data={'reorder':svc.reorder(),'excess':svc.excess(),'near-expiry':svc.near_expiry(),'branches':svc.branch_summary()}.get(report_name)
    if data is None: from fastapi import HTTPException; raise HTTPException(404,'Unknown report')
    if format=='xlsx':
        stream=to_excel(data,report_name.replace('-','_')); return StreamingResponse(stream,media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',headers={'Content-Disposition':f'attachment; filename={report_name}.xlsx'})
    stream=to_csv(data); return StreamingResponse(stream,media_type='text/csv',headers={'Content-Disposition':f'attachment; filename={report_name}.csv'})
