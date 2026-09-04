# Installation Guide

## Prerequisites
1. Python 3.14.3
2. Node.js 24.x and npm 11.x
3. SQL Server
4. SQL Server Management Studio (recommended)
5. Microsoft ODBC Driver 18 for SQL Server

## Verify versions
```powershell
py -3.14 --version
node --version
npm --version
```

## SQL Server
Run the scripts in order for the demo database. If SQL Server Express is installed, your server is commonly `localhost\SQLEXPRESS`, but use the exact server name shown in SSMS.

## Backend
```powershell
cd backend
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
python run.py
```

If PowerShell blocks activation, use:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run.py
```

## Frontend
```powershell
cd frontend
npm install
npm run dev
```

## Troubleshooting
- `No module named app`: run backend from the `backend` directory.
- `Login failed`: check server name, authentication mode, username/password.
- `Data source name not found`: install Microsoft ODBC Driver 18 and ensure `DB_DRIVER` matches the installed driver.
- CORS errors: verify `VITE_API_URL` and `CORS_ORIGINS`.
