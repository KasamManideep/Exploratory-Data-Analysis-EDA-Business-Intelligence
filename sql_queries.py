import pandas as pd;
import sqlite3
# Load CSV file
df = pd.read_csv("ecommerce_sales.csv")
# Create database connection
conn = sqlite3.connect('ecommerce.db')
# Store dataframe into SQL table
df.to_sql('sales', conn, if_exists='replace', index=False)
print("Data inserted successfully")
queries = {
    "Q1: Top 5 products by revenue": """
        SELECT product_name, SUM(revenue) AS total_revenue
        FROM sales GROUP BY product_name
        ORDER BY total_revenue DESC LIMIT 5;
    """,
    "Q2: Monthly revenue trend": """
        SELECT strftime('%Y-%m', date) AS month, SUM(revenue) AS monthly_revenue
        FROM sales GROUP BY month ORDER BY month;
    """,
    "Q3: Revenue by region": """
        SELECT region, SUM(revenue) AS total_revenue, COUNT(*) AS orders
        FROM sales GROUP BY region ORDER BY total_revenue DESC;
    """,
    "Q4: Avg discount by category": """
        SELECT product_category, ROUND(AVG(discount_pct),2) AS avg_discount
        FROM sales GROUP BY product_category;
    """,
    "Q5: Top spending age group": """
        SELECT
            CASE WHEN age < 25 THEN 'Under 25'
                 WHEN age BETWEEN 25 AND 35 THEN '25-35'
                 WHEN age BETWEEN 36 AND 45 THEN '36-45'
                 ELSE '45+' END AS age_group,
            SUM(revenue) AS total_revenue
        FROM sales GROUP BY age_group ORDER BY total_revenue DESC;
    """,
    "Q6: Gender-wise revenue split": """
        SELECT gender, SUM(revenue) AS total_revenue,
               ROUND(100.0 * SUM(revenue) / (SELECT SUM(revenue) FROM sales), 1) AS pct
        FROM sales GROUP BY gender;
    """,
    "Q7: Marketing ROI by category": """
        SELECT product_category,
               SUM(revenue) AS revenue,
               SUM(marketing_spend) AS spend,
               ROUND(SUM(revenue) * 1.0 / SUM(marketing_spend), 2) AS roi
        FROM sales GROUP BY product_category ORDER BY roi DESC;
    """
}

for title, query in queries.items():
    print(f"\n{'='*50}\n{title}\n{'='*50}")
    print(pd.read_sql_query(query, conn).to_string(index=False))