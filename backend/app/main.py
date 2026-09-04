from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.api import reports,dashboard,health
app=FastAPI(title=settings.app_name,version='1.0.0',description='Rule-based pharmacy inventory optimization over a read-only SQL Server ERP layer.')
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_list,allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
app.include_router(health.router,prefix=settings.api_prefix)
app.include_router(dashboard.router,prefix=settings.api_prefix)
app.include_router(reports.router,prefix=settings.api_prefix)
@app.get('/')
def root(): return {'application':settings.app_name,'docs':'/docs'}
