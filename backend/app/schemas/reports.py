from pydantic import BaseModel
from datetime import date
from typing import Optional

class ReorderItem(BaseModel):
    branch_id: int
    branch_name: str
    product_id: int
    product_code: str
    product_name: str
    current_stock: float
    pending_po: float
    pending_grn: float
    average_daily_sales: float
    lead_time_days: int
    inventory_days: int
    minimum_stock: float
    maximum_stock: float
    required_stock: float
    available_stock: float
    reorder_quantity: float
    estimated_value: float
    recommendation: str

class ExcessItem(BaseModel):
    branch_id: int
    branch_name: str
    product_id: int
    product_code: str
    product_name: str
    current_stock: float
    maximum_stock: float
    excess_quantity: float
    unit_cost: float
    excess_inventory_value: float
    average_daily_sales: float
    days_of_inventory: Optional[float]

class ExpiryItem(BaseModel):
    branch_id: int
    branch_name: str
    product_id: int
    product_code: str
    product_name: str
    batch_no: str
    expiry_date: date
    quantity: float
    unit_cost: float
    inventory_value: float
    days_to_expiry: int

class BranchSummary(BaseModel):
    branch_id: int
    branch_name: str
    total_quantity: float
    inventory_value: float
    product_count: int

class DashboardSummary(BaseModel):
    products_requiring_reorder: int
    reorder_value: float
    excess_stock_value: float
    near_expiry_value: float
    near_expiry_items: int
    total_inventory_value: float
    branches: list[BranchSummary]
