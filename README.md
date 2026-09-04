# Pharmacy Inventory Optimization System — Phase 1

A complete practice implementation of the requested rule-based inventory optimization layer over Microsoft SQL Server ERP data.

## Scope
- Read-only SQL Server ERP integration
- Branch-wise reorder recommendation
- Pending PO and pending GRN consideration
- Historical-sales based average daily sales
- Supplier lead time
- Configurable inventory days/min/max stock/near-expiry threshold
- Excess stock and days-of-inventory reporting
- Batch-level near-expiry reporting
- Dashboard
- Excel/CSV export
- FastAPI backend + React frontend

## Runtime
- Python **3.14.3** (the Python version currently used for this project)
- Node.js 24.x / npm 11.x
- Microsoft SQL Server
- ODBC Driver 18 for SQL Server

## 1. Database
Open SQL Server Management Studio as a user allowed to create databases and run:
1. `sql/01_create_database.sql`
2. `sql/02_seed_data.sql`
3. `sql/03_readonly_views.sql`

The seed script creates a small ERP-like dataset. In a real deployment, do not run the create/seed scripts against the existing ERP. Instead map the repository SQL to the ERP's existing read-only tables/views.

## 2. Backend
PowerShell:
```powershell
cd backend
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```
Edit `.env` for your SQL Server server/database. For Windows Authentication use `DB_TRUSTED_CONNECTION=True`.

Run:
```powershell
python run.py
```
API: `http://127.0.0.1:8000`
Swagger: `http://127.0.0.1:8000/docs`

## 3. Frontend
Open a second terminal:
```powershell
cd frontend
npm install
npm run dev
```
Open the URL Vite displays, normally `http://localhost:5173`.

## API endpoints
- GET `/api/health`
- GET `/api/dashboard/summary`
- GET `/api/reports/reorder`
- GET `/api/reports/excess`
- GET `/api/reports/near-expiry`
- GET `/api/reports/branches`
- GET `/api/reports/export/reorder?format=xlsx`
- GET `/api/reports/export/excess?format=csv`
- GET `/api/reports/export/near-expiry?format=xlsx`
- GET `/api/reports/export/branches?format=xlsx`

## Business logic
Required stock = max(minimum stock, average daily sales × (supplier lead time + configured inventory days))

Available stock = current stock + pending PO + pending GRN

Reorder quantity = max(0, required stock − available stock), capped by the configured maximum stock where applicable.

Days of inventory = current stock / average daily sales.

Excess quantity = max(0, current stock − configured maximum stock).

Near expiry = batch expiry date is within the configured threshold and quantity > 0.

## Production ERP integration
The application is deliberately separated into repository/service/API layers. For an existing ERP, the database is read-only and should not be changed. Replace the repository SQL with SELECTs against the actual ERP schema or approved reporting views.
