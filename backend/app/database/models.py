from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Date, DateTime, Numeric, Boolean
from datetime import date, datetime

class Base(DeclarativeBase):
    pass

# These models mirror the demo ERP schema. In a real ERP integration, map queries to the
# existing read-only tables/views instead of modifying the ERP schema.
class Branch(Base):
    __tablename__ = "Branches"
    branch_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    branch_code: Mapped[str] = mapped_column(String(30))
    branch_name: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(100))
    active: Mapped[bool] = mapped_column(Boolean, default=True)

class Product(Base):
    __tablename__ = "Products"
    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_code: Mapped[str] = mapped_column(String(50))
    product_name: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(100))
    supplier_id: Mapped[int] = mapped_column(Integer)
    unit_cost: Mapped[float] = mapped_column(Numeric(18,2))
    active: Mapped[bool] = mapped_column(Boolean, default=True)

class Supplier(Base):
    __tablename__ = "Suppliers"
    supplier_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    supplier_code: Mapped[str] = mapped_column(String(50))
    supplier_name: Mapped[str] = mapped_column(String(200))
    lead_time_days: Mapped[int] = mapped_column(Integer)

class Inventory(Base):
    __tablename__ = "Inventory"
    inventory_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    branch_id: Mapped[int] = mapped_column(Integer)
    product_id: Mapped[int] = mapped_column(Integer)
    batch_no: Mapped[str] = mapped_column(String(80))
    quantity: Mapped[float] = mapped_column(Numeric(18,2))
    expiry_date: Mapped[date] = mapped_column(Date)
    unit_cost: Mapped[float] = mapped_column(Numeric(18,2))

class Sale(Base):
    __tablename__ = "Sales"
    sale_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    branch_id: Mapped[int] = mapped_column(Integer)
    product_id: Mapped[int] = mapped_column(Integer)
    sale_date: Mapped[date] = mapped_column(Date)
    quantity: Mapped[float] = mapped_column(Numeric(18,2))

class PurchaseOrder(Base):
    __tablename__ = "PurchaseOrders"
    po_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    branch_id: Mapped[int] = mapped_column(Integer)
    supplier_id: Mapped[int] = mapped_column(Integer)
    po_date: Mapped[date] = mapped_column(Date)
    expected_date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(30))

class PurchaseOrderDetail(Base):
    __tablename__ = "PurchaseOrderDetails"
    po_detail_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    po_id: Mapped[int] = mapped_column(Integer)
    product_id: Mapped[int] = mapped_column(Integer)
    ordered_quantity: Mapped[float] = mapped_column(Numeric(18,2))
    received_quantity: Mapped[float] = mapped_column(Numeric(18,2))

class GRN(Base):
    __tablename__ = "GRNs"
    grn_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    po_id: Mapped[int] = mapped_column(Integer)
    branch_id: Mapped[int] = mapped_column(Integer)
    grn_date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(30))

class GRNDetail(Base):
    __tablename__ = "GRNDetails"
    grn_detail_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    grn_id: Mapped[int] = mapped_column(Integer)
    product_id: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[float] = mapped_column(Numeric(18,2))

class InventoryRule(Base):
    __tablename__ = "InventoryRules"
    rule_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    branch_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    product_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    inventory_days: Mapped[int] = mapped_column(Integer)
    minimum_stock: Mapped[float] = mapped_column(Numeric(18,2))
    maximum_stock: Mapped[float] = mapped_column(Numeric(18,2))
    near_expiry_days: Mapped[int] = mapped_column(Integer)
    sales_history_days: Mapped[int] = mapped_column(Integer)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
