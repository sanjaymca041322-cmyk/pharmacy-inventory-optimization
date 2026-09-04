USE PharmacyERP;
GO
INSERT INTO Branches VALUES (1,'LKO','Lucknow Main','Lucknow',1),(2,'KNP','Kanpur Main','Kanpur',1),(3,'AGR','Agra Main','Agra',1);
INSERT INTO Suppliers VALUES (1,'SUP001','ABC Pharma Distributors',7),(2,'SUP002','HealthCare Supplies',10),(3,'SUP003','Medico Wholesale',5);
INSERT INTO Products VALUES (1,'MED001','Paracetamol 500mg','Analgesic',1,2.50,1),(2,'MED002','Amoxicillin 500mg','Antibiotic',2,8.00,1),(3,'MED003','Cetirizine 10mg','Antihistamine',1,1.75,1),(4,'MED004','Azithromycin 500mg','Antibiotic',3,12.50,1),(5,'MED005','Pantoprazole 40mg','Gastro',2,6.25,1),(6,'MED006','ORS Sachet','Nutrition',1,4.00,1);
INSERT INTO Inventory(branch_id,product_id,batch_no,quantity,expiry_date,unit_cost) VALUES
(1,1,'P001',120,DATEADD(day,240,GETDATE()),2.50),(1,2,'A001',40,DATEADD(day,50,GETDATE()),8),(1,3,'C001',600,DATEADD(day,35,GETDATE()),1.75),(1,4,'AZ001',80,DATEADD(day,300,GETDATE()),12.5),(1,5,'PA001',300,DATEADD(day,200,GETDATE()),6.25),(1,6,'O001',1000,DATEADD(day,180,GETDATE()),4),
(2,1,'P002',500,DATEADD(day,220,GETDATE()),2.5),(2,2,'A002',160,DATEADD(day,250,GETDATE()),8),(2,3,'C002',90,DATEADD(day,45,GETDATE()),1.75),(2,4,'AZ002',700,DATEADD(day,280,GETDATE()),12.5),(2,5,'PA002',100,DATEADD(day,60,GETDATE()),6.25),(2,6,'O002',300,DATEADD(day,150,GETDATE()),4),
(3,1,'P003',80,DATEADD(day,20,GETDATE()),2.5),(3,2,'A003',450,DATEADD(day,270,GETDATE()),8),(3,3,'C003',250,DATEADD(day,120,GETDATE()),1.75),(3,4,'AZ003',70,DATEADD(day,40,GETDATE()),12.5),(3,5,'PA003',80,DATEADD(day,25,GETDATE()),6.25),(3,6,'O003',120,DATEADD(day,365,GETDATE()),4);
DECLARE @d INT=1; WHILE @d<=90 BEGIN
 INSERT INTO Sales(branch_id,product_id,sale_date,quantity) VALUES
 (1,1,DATEADD(day,-@d,CAST(GETDATE() AS DATE)),15),(1,2,DATEADD(day,-@d,CAST(GETDATE() AS DATE)),8),(1,3,DATEADD(day,-@d,CAST(GETDATE() AS DATE)),4),(1,5,DATEADD(day,-@d,CAST(GETDATE() AS DATE)),6),(2,1,DATEADD(day,-@d,CAST(GETDATE() AS DATE)),10),(2,2,DATEADD(day,-@d,CAST(GETDATE() AS DATE)),5),(2,4,DATEADD(day,-@d,CAST(GETDATE() AS DATE)),3),(2,5,DATEADD(day,-@d,CAST(GETDATE() AS DATE)),4),(3,1,DATEADD(day,-@d,CAST(GETDATE() AS DATE)),12),(3,2,DATEADD(day,-@d,CAST(GETDATE() AS DATE)),4),(3,3,DATEADD(day,-@d,CAST(GETDATE() AS DATE)),5),(3,4,DATEADD(day,-@d,CAST(GETDATE() AS DATE)),4); SET @d+=1; END;
INSERT INTO PurchaseOrders VALUES (1001,1,1,DATEADD(day,-3,GETDATE()),DATEADD(day,4,GETDATE()),'OPEN'),(1002,1,2,DATEADD(day,-2,GETDATE()),DATEADD(day,6,GETDATE()),'PARTIAL'),(1003,2,3,DATEADD(day,-4,GETDATE()),DATEADD(day,1,GETDATE()),'OPEN');
INSERT INTO PurchaseOrderDetails VALUES (1,1001,1,200,50),(2,1002,2,100,20),(3,1003,1,100,0);
INSERT INTO GRNs VALUES (2001,1001,1,DATEADD(day,-1,GETDATE()),'PENDING'),(2002,1002,1,DATEADD(day,-1,GETDATE()),'OPEN');
INSERT INTO GRNDetails VALUES (1,2001,1,150),(2,2002,2,80);
INSERT INTO InventoryRules(branch_id,product_id,inventory_days,minimum_stock,maximum_stock,near_expiry_days,sales_history_days) VALUES
(NULL,NULL,30,0,500,90,90),(1,NULL,30,20,500,90,90),(2,NULL,30,20,600,90,90),(3,NULL,30,20,500,90,90),(NULL,1,30,50,500,60,90),(NULL,2,30,30,300,90,90),(NULL,3,30,40,400,90,90),(NULL,4,30,30,400,90,90),(NULL,5,30,30,300,90,90);
GO
