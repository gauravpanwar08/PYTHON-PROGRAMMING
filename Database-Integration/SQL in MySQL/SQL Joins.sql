-- A JOIN is used to combine rows from two or more tables based on a related column between them.
-- JOIN → Combines tables

CREATE DATABASE Ecommerce;
USE Ecommerce;
	-- Customers Table
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(50),
    City VARCHAR(50)
);

-- Orders Table
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- Products Table
CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(50),
    Price DECIMAL(10,2)
);

-- OrderDetails Table (Many-to-Many relation between Orders & Products)
CREATE TABLE OrderDetails (
    OrderDetailID INT PRIMARY KEY,
    OrderID INT,
    ProductID INT,
    Quantity INT,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

INSERT INTO Customers VALUES
(1, 'Gaurav', 'Delhi'),
(2, 'Neha', 'Mumbai'),
(3, 'Rahul', 'Pune'),
(4, 'Priya', 'Bangalore'),
(5, 'Anchal', 'Delhi'),
(6, 'Ajay', 'Mumbai');

INSERT INTO Orders VALUES
(101, 1, '2025-09-01'),
(102, 2, '2025-09-02'),
(103, 1, '2025-09-05'),
(104, 3, '2025-09-06');

INSERT INTO Products VALUES
(201, 'Laptop', 60000),
(202, 'Mobile', 25000),
(203, 'Headphones', 3000),
(204, 'Keyboard', 1500);

INSERT INTO OrderDetails VALUES
(1, 101, 201, 1),   -- Gaurav ordered 1 Laptop
(2, 101, 203, 2),   -- Gaurav ordered 2 Headphones
(3, 102, 202, 1),   -- Neha ordered 1 Mobile
(4, 103, 204, 3),   -- Gaurav ordered 3 Keyboards
(5, 104, 201, 1);   -- Rahul ordered 1 Laptop

SELECT * FROM Customers;
SELECT * FROM Orders;
SELECT * FROM Products;
SELECT * FROM OrderDetails;

  -- 1. INNER JOIN (returns only matching records)
SELECT Customers.CustomerName, Orders.OrderID, Orders.OrderDate
FROM Customers
INNER JOIN Orders
ON Customers.CustomerID = Orders.CustomerID;

  -- 2. LEFT JOIN (all records from left, matching from right)
SELECT Customers.CustomerName, Orders.OrderID
FROM Customers
LEFT JOIN Orders
ON Customers.CustomerID = Orders.CustomerID;

  -- 3. RIGHT JOIN (all from right, matching from left)
SELECT Customers.CustomerName, Orders.OrderID
FROM Customers
RIGHT JOIN Orders ON Customers.CustomerID = Orders.CustomerID;

  -- 4. FULL OUTER JOIN (MySQL doesn’t support directly, but can use UNION)
SELECT Customers.CustomerID, Customers.CustomerName, Orders.OrderID, Orders.OrderDate, Customers.City
FROM Customers
LEFT JOIN Orders ON Customers.CustomerID = Orders.CustomerID
UNION
SELECT Customers.CustomerID, Customers.CustomerName, Orders.OrderID, Orders.OrderDate, Customers.City
FROM Customers
RIGHT JOIN Orders ON Customers.CustomerID = Orders.CustomerID;

  -- 5. CROSS JOIN (Cartesian product)
SELECT Customers.CustomerName, Products.ProductName
FROM Customers
CROSS JOIN Products;

  -- 6. SELF JOIN (table joins with itself)
SELECT A.CustomerName AS Customer1, B.CustomerName AS Customer2, A.City
FROM Customers A
INNER JOIN Customers B 
ON A.City = B.City AND A.CustomerID <> B.CustomerID;

  -- e.g. Multi-Table JOIN (Orders + OrderDetails + Products)
SELECT C.CustomerName, O.OrderID, P.ProductName, OD.Quantity, P.Price,
       (OD.Quantity * P.Price) AS TotalAmount
FROM Customers C
JOIN Orders O ON C.CustomerID = O.CustomerID
JOIN OrderDetails OD ON O.OrderID = OD.OrderID
JOIN Products P ON OD.ProductID = P.ProductID;
