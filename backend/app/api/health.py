from fastapi import APIRouter
from app.database.connection import test_connection
router=APIRouter(tags=["Health"])
@router.get('/health')
def health():
    try: return {'status':'ok','database':test_connection()}
    except Exception as e: return {'status':'error','database':False,'detail':str(e)}
