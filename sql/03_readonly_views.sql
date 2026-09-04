USE PharmacyERP;
GO
-- Optional integration views. In production these should point to existing ERP tables/views.
CREATE OR ALTER VIEW vw_InventoryOptimization_Inventory AS SELECT * FROM Inventory;
GO
CREATE OR ALTER VIEW vw_InventoryOptimization_Sales AS SELECT * FROM Sales;
GO
