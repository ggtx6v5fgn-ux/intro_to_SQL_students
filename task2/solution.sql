CREATE VIEW v_region_sales_summary AS
SELECT 
    Region,
    COUNT(*) AS Sales_Count,
    SUM(
        CAST(Unit_Price AS REAL) * 
        CAST(Quantity_Sold AS REAL) * 
        (1 - CAST(Discount AS REAL))
    ) AS Total_Revenue
FROM data
GROUP BY Region
ORDER BY Total_Revenue DESC;