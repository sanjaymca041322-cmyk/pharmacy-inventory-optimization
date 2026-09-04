IF DB_ID('PharmacyERP') IS NULL CREATE DATABASE PharmacyERP;
GO
USE PharmacyERP;
GO

CREATE TABLE Branches(branch_id INT PRIMARY KEY,branch_code VARCHAR(30) NOT NULL,branch_name VARCHAR(100) NOT NULL,location VARCHAR(100),active BIT NOT NULL DEFAULT 1);
CREATE TABLE Suppliers(supplier_id INT PRIMARY KEY,supplier_code VARCHAR(50) NOT NULL,supplier_name VARCHAR(200) NOT NULL,lead_time_days INT NOT NULL);
CREATE TABLE Products(product_id INT PRIMARY KEY,product_code VARCHAR(50) NOT NULL,product_name VARCHAR(200) NOT NULL,category VARCHAR(100),supplier_id INT NOT NULL,unit_cost DECIMAL(18,2) NOT NULL,active BIT NOT NULL DEFAULT 1,FOREIGN KEY(supplier_id) REFERENCES Suppliers(supplier_id));
CREATE TABLE Inventory(inventory_id INT IDENTITY PRIMARY KEY,branch_id INT NOT NULL,product_id INT NOT NULL,batch_no VARCHAR(80) NOT NULL,quantity DECIMAL(18,2) NOT NULL,expiry_date DATE NOT NULL,unit_cost DECIMAL(18,2) NOT NULL,FOREIGN KEY(branch_id) REFERENCES Branches(branch_id),FOREIGN KEY(product_id) REFERENCES Products(product_id));
CREATE TABLE Sales(sale_id INT IDENTITY PRIMARY KEY,branch_id INT NOT NULL,product_id INT NOT NULL,sale_date DATE NOT NULL,quantity DECIMAL(18,2) NOT NULL);
CREATE TABLE PurchaseOrders(po_id INT PRIMARY KEY,branch_id INT NOT NULL,supplier_id INT NOT NULL,po_date DATE NOT NULL,expected_date DATE NOT NULL,status VARCHAR(30) NOT NULL);
CREATE TABLE PurchaseOrderDetails(po_detail_id INT PRIMARY KEY,po_id INT NOT NULL,product_id INT NOT NULL,ordered_quantity DECIMAL(18,2) NOT NULL,received_quantity DECIMAL(18,2) NOT NULL);
CREATE TABLE GRNs(grn_id INT PRIMARY KEY,po_id INT NOT NULL,branch_id INT NOT NULL,grn_date DATE NOT NULL,status VARCHAR(30) NOT NULL);
CREATE TABLE GRNDetails(grn_detail_id INT PRIMARY KEY,grn_id INT NOT NULL,product_id INT NOT NULL,quantity DECIMAL(18,2) NOT NULL);
CREATE TABLE InventoryRules(rule_id INT IDENTITY PRIMARY KEY,branch_id INT NULL,product_id INT NULL,inventory_days INT NOT NULL,minimum_stock DECIMAL(18,2) NOT NULL,maximum_stock DECIMAL(18,2) NOT NULL,near_expiry_days INT NOT NULL,sales_history_days INT NOT NULL,active BIT NOT NULL DEFAULT 1);
GO
