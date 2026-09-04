from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Pharmacy Inventory Optimization API"
    app_env: str = "development"
    api_prefix: str = "/api"
    db_driver: str = "ODBC Driver 18 for SQL Server"
    db_server: str = r"localhost\SQLEXPRESS"
    db_name: str = "PharmacyERP"
    db_username: str = ""
    db_password: str = ""
    db_trusted_connection: bool = True
    db_encrypt: bool = False
    db_trust_server_certificate: bool = True
    cors_origins: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_list(self) -> list[str]:
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

    @property
    def database_url(self) -> str:
        from urllib.parse import quote_plus
        if self.db_trusted_connection:
            conn = (
                f"DRIVER={{{self.db_driver}}};SERVER={self.db_server};"
                f"DATABASE={self.db_name};Trusted_Connection=yes;"
                f"Encrypt={'yes' if self.db_encrypt else 'no'};"
                f"TrustServerCertificate={'yes' if self.db_trust_server_certificate else 'no'};"
            )
        else:
            conn = (
                f"DRIVER={{{self.db_driver}}};SERVER={self.db_server};"
                f"DATABASE={self.db_name};UID={self.db_username};PWD={self.db_password};"
                f"Encrypt={'yes' if self.db_encrypt else 'no'};"
                f"TrustServerCertificate={'yes' if self.db_trust_server_certificate else 'no'};"
            )
        return "mssql+pyodbc:///?odbc_connect=" + quote_plus(conn)

settings = Settings()
