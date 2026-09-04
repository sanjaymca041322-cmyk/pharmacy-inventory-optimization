from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, timedelta

class InventoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def inventory_rows(self):
        sql = text("""
        SELECT i.branch_id, b.branch_name, i.product_id, p.product_code, p.product_name,
               i.batch_no, CAST(i.quantity AS float) quantity, CAST(i.unit_cost AS float) unit_cost,
               i.expiry_date, p.supplier_id, s.lead_time_days
        FROM Inventory i
        JOIN Branches b ON b.branch_id=i.branch_id
        JOIN Products p ON p.product_id=i.product_id
        LEFT JOIN Suppliers s ON s.supplier_id=p.supplier_id
        WHERE p.active=1
        """)
        return [dict(r._mapping) for r in self.db.execute(sql).fetchall()]

    def sales_daily(self, history_days: int):
        start = date.today() - timedelta(days=history_days)
        sql = text("""
        SELECT branch_id, product_id, CAST(SUM(quantity) AS float) total_sales,
               COUNT(DISTINCT sale_date) sales_days
        FROM Sales
        WHERE sale_date >= :start_date AND sale_date <= :end_date
        GROUP BY branch_id, product_id
        """)
        return [dict(r._mapping) for r in self.db.execute(sql, {"start_date": start, "end_date": date.today()}).fetchall()]

    def pending_po(self):
        sql = text("""
        SELECT po.branch_id, d.product_id,
               CAST(SUM(CASE WHEN d.ordered_quantity>d.received_quantity
                    THEN d.ordered_quantity-d.received_quantity ELSE 0 END) AS float) pending_po
        FROM PurchaseOrders po
        JOIN PurchaseOrderDetails d ON d.po_id=po.po_id
        WHERE po.status IN ('OPEN','PARTIAL')
        GROUP BY po.branch_id, d.product_id
        """)
        return [dict(r._mapping) for r in self.db.execute(sql).fetchall()]

    def pending_grn(self):
        sql = text("""
        SELECT g.branch_id, d.product_id, CAST(SUM(d.quantity) AS float) pending_grn
        FROM GRNs g
        JOIN GRNDetails d ON d.grn_id=g.grn_id
        WHERE g.status IN ('PENDING','OPEN')
        GROUP BY g.branch_id, d.product_id
        """)
        return [dict(r._mapping) for r in self.db.execute(sql).fetchall()]

    def rules(self):
        sql = text("""
        SELECT rule_id, branch_id, product_id, inventory_days, CAST(minimum_stock AS float) minimum_stock,
               CAST(maximum_stock AS float) maximum_stock, near_expiry_days, sales_history_days
        FROM InventoryRules WHERE active=1
        ORDER BY CASE WHEN product_id IS NOT NULL THEN 0 ELSE 1 END,
                 CASE WHEN branch_id IS NOT NULL THEN 0 ELSE 1 END
        """)
        return [dict(r._mapping) for r in self.db.execute(sql).fetchall()]
