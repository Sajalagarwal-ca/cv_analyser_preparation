# PostgreSQL Interview Prep — FAANG & Top Analytics (Data Scientist)

---

## Section 1: Window Functions (Most Heavily Tested)

### Q1 — Running Total of Revenue per Customer (Amazon)
```sql
-- Orders table: order_id, customer_id, order_date, amount
SELECT customer_id, order_date, amount,
       SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS running_total
FROM orders;
```

### Q2 — Rank Employees by Salary Within Department (Meta)
```sql
SELECT department, employee_name, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk,
       DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dense_rnk
FROM employees;
```
**Follow-up:** Explain difference between `RANK()`, `DENSE_RANK()`, and `ROW_NUMBER()`.

### Q3 — Month-over-Month Growth Rate (Tiger Analytics)
```sql
WITH monthly AS (
  SELECT DATE_TRUNC('month', order_date) AS month,
         SUM(amount) AS revenue
  FROM orders
  GROUP BY 1
)
SELECT month, revenue,
       LAG(revenue) OVER (ORDER BY month) AS prev_month,
       ROUND((revenue - LAG(revenue) OVER (ORDER BY month)) * 100.0
             / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 2) AS mom_growth_pct
FROM monthly;
```

### Q4 — Find the Median Salary (Amazon)
```sql
SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) AS median_salary
FROM employees;
```

### Q5 — First and Last Purchase per Customer (Meta)
```sql
SELECT DISTINCT customer_id,
       FIRST_VALUE(product) OVER w AS first_product,
       LAST_VALUE(product) OVER (w ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS last_product
FROM purchases
WINDOW w AS (PARTITION BY customer_id ORDER BY purchase_date);
```

---

## Section 2: CTEs and Subqueries

### Q6 — Customers Who Made Purchases on Consecutive Days (Amazon)
```sql
WITH purchase_days AS (
  SELECT customer_id, order_date,
         LEAD(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS next_date
  FROM orders
)
SELECT DISTINCT customer_id
FROM purchase_days
WHERE next_date - order_date = 1;
```

### Q7 — Second Highest Salary (Classic — all companies)
```sql
-- Method 1: Subquery
SELECT MAX(salary) FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- Method 2: DENSE_RANK
SELECT salary FROM (
  SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
  FROM employees
) t WHERE rnk = 2;
```

### Q8 — Recursive CTE: Employee Hierarchy (Amazon)
```sql
WITH RECURSIVE org AS (
  SELECT employee_id, name, manager_id, 1 AS level
  FROM employees WHERE manager_id IS NULL
  UNION ALL
  SELECT e.employee_id, e.name, e.manager_id, o.level + 1
  FROM employees e JOIN org o ON e.manager_id = o.employee_id
)
SELECT * FROM org ORDER BY level;
```

---

## Section 3: Joins & Set Operations

### Q9 — Users Who Logged In but Never Purchased (Meta)
```sql
SELECT l.user_id
FROM logins l
LEFT JOIN purchases p ON l.user_id = p.user_id
WHERE p.user_id IS NULL;
```

### Q10 — Self Join: Employees Earning More Than Their Manager (Amazon)
```sql
SELECT e.name AS employee, e.salary AS emp_salary,
       m.name AS manager, m.salary AS mgr_salary
FROM employees e
JOIN employees m ON e.manager_id = m.employee_id
WHERE e.salary > m.salary;
```

### Q11 — Find Mutual Friends (Meta/Facebook — very common)
```sql
-- friendships(user_id1, user_id2) — bidirectional
SELECT f1.user_id2 AS mutual_friend
FROM friendships f1
JOIN friendships f2 ON f1.user_id2 = f2.user_id2
WHERE f1.user_id1 = 'Alice'
  AND f2.user_id1 = 'Bob'
  AND f1.user_id2 NOT IN ('Alice', 'Bob');
```

---

## Section 4: Aggregation & Grouping

### Q12 — Products Ordered in Every Month of 2024 (Tiger Analytics)
```sql
SELECT product_id
FROM orders
WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01'
GROUP BY product_id
HAVING COUNT(DISTINCT DATE_TRUNC('month', order_date)) = 12;
```

### Q13 — Top 3 Products by Revenue per Category (Amazon)
```sql
WITH ranked AS (
  SELECT category, product_name, SUM(revenue) AS total_rev,
         ROW_NUMBER() OVER (PARTITION BY category ORDER BY SUM(revenue) DESC) AS rn
  FROM sales
  GROUP BY category, product_name
)
SELECT * FROM ranked WHERE rn <= 3;
```

### Q14 — Retention Rate: Day-1 Retention (Meta/Gaming)
```sql
WITH first_login AS (
  SELECT user_id, MIN(login_date) AS first_date
  FROM logins GROUP BY user_id
)
SELECT f.first_date,
       COUNT(DISTINCT l.user_id)::FLOAT / COUNT(DISTINCT f.user_id) AS day1_retention
FROM first_login f
LEFT JOIN logins l ON f.user_id = l.user_id
                   AND l.login_date = f.first_date + INTERVAL '1 day'
GROUP BY f.first_date;
```

---

## Section 5: Data Manipulation & Conditional Logic

### Q15 — Pivot Table Using CASE (All companies)
```sql
SELECT employee_id,
       SUM(CASE WHEN quarter = 'Q1' THEN revenue END) AS q1,
       SUM(CASE WHEN quarter = 'Q2' THEN revenue END) AS q2,
       SUM(CASE WHEN quarter = 'Q3' THEN revenue END) AS q3,
       SUM(CASE WHEN quarter = 'Q4' THEN revenue END) AS q4
FROM quarterly_sales
GROUP BY employee_id;
```

### Q16 — De-duplicate Rows Keeping Latest (Amazon)
```sql
DELETE FROM events
WHERE ctid NOT IN (
  SELECT DISTINCT ON (user_id, event_type)
         ctid
  FROM events
  ORDER BY user_id, event_type, event_time DESC
);
```

### Q17 — Gap Analysis: Find Missing Dates (Tiger Analytics)
```sql
WITH date_range AS (
  SELECT generate_series(MIN(log_date), MAX(log_date), '1 day'::interval)::date AS d
  FROM daily_logs
)
SELECT d AS missing_date
FROM date_range
LEFT JOIN daily_logs ON log_date = d
WHERE log_date IS NULL;
```

---

## Section 6: Performance & Optimization (Conceptual)

### Q18 — Explain EXPLAIN ANALYZE output
```
Key things interviewers look for:
- Seq Scan vs Index Scan — when does Postgres choose each?
- Cost estimates (startup cost..total cost)
- Actual time vs planned time
- Rows removed by filter → suggests missing index
- Hash Join vs Nested Loop vs Merge Join
```

### Q19 — When Would You Use a Partial Index?
```sql
-- Index only active users (common filter in queries)
CREATE INDEX idx_active_users ON users(email) WHERE is_active = true;
```

### Q20 — Explain Partitioning Strategies
```
- Range partitioning (dates, numeric ranges) — most common for time-series
- List partitioning (region, status)
- Hash partitioning (even distribution)
- In Postgres: PARTITION BY RANGE / LIST / HASH
```

---

## Section 7: Advanced / Tricky Questions

### Q21 — Sessionization: Assign Session IDs to Events (Amazon DS)
```sql
WITH gaps AS (
  SELECT user_id, event_time,
         CASE WHEN event_time - LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time)
                   > INTERVAL '30 minutes'
              THEN 1 ELSE 0 END AS new_session
  FROM events
)
SELECT user_id, event_time,
       SUM(new_session) OVER (PARTITION BY user_id ORDER BY event_time) AS session_id
FROM gaps;
```

### Q22 — Funnel Analysis (Meta)
```sql
WITH funnel AS (
  SELECT user_id,
         MAX(CASE WHEN event = 'page_view' THEN 1 ELSE 0 END) AS step1,
         MAX(CASE WHEN event = 'add_to_cart' THEN 1 ELSE 0 END) AS step2,
         MAX(CASE WHEN event = 'purchase' THEN 1 ELSE 0 END) AS step3
  FROM user_events
  GROUP BY user_id
)
SELECT COUNT(*) AS total_users,
       SUM(step1) AS viewed,
       SUM(step2) AS added_to_cart,
       SUM(step3) AS purchased
FROM funnel;
```

### Q23 — Detecting Fraud: Transactions Within 10 Minutes of Each Other (Amazon)
```sql
SELECT a.txn_id, b.txn_id, a.user_id, a.txn_time, b.txn_time
FROM transactions a
JOIN transactions b
  ON a.user_id = b.user_id
  AND a.txn_id < b.txn_id
  AND b.txn_time - a.txn_time <= INTERVAL '10 minutes';
```

### Q24 — Cumulative Distribution / Percentile Bucket (Tiger Analytics)
```sql
SELECT user_id, total_spend,
       NTILE(10) OVER (ORDER BY total_spend) AS decile,
       CUME_DIST() OVER (ORDER BY total_spend) AS cumulative_pct
FROM (
  SELECT user_id, SUM(amount) AS total_spend
  FROM orders GROUP BY user_id
) t;
```

### Q25 — A/B Test Analysis: Significance Metrics (Meta DS)
```sql
WITH experiment AS (
  SELECT variant,
         COUNT(*) AS n,
         AVG(converted::int) AS conversion_rate,
         STDDEV(converted::int) AS std_dev
  FROM ab_test_results
  GROUP BY variant
)
SELECT *,
       (SELECT conversion_rate FROM experiment WHERE variant = 'treatment')
       - (SELECT conversion_rate FROM experiment WHERE variant = 'control') AS lift
FROM experiment;
```

---

## Section 8: PostgreSQL-Specific Features (Differentiators)

### Q26 — JSONB Queries
```sql
-- Extract nested field
SELECT data->>'name' AS name,
       data->'address'->>'city' AS city
FROM users
WHERE data @> '{"active": true}';

-- Index for JSONB
CREATE INDEX idx_users_data ON users USING GIN (data);
```

### Q27 — Array Operations
```sql
SELECT * FROM products WHERE tags @> ARRAY['electronics', 'sale'];
SELECT UNNEST(tags) AS tag, COUNT(*) FROM products GROUP BY 1 ORDER BY 2 DESC;
```

### Q28 — LATERAL JOIN (Advanced — Amazon/Meta)
```sql
-- Top 3 orders per customer
SELECT c.customer_id, c.name, o.*
FROM customers c
CROSS JOIN LATERAL (
  SELECT order_id, amount, order_date
  FROM orders
  WHERE customer_id = c.customer_id
  ORDER BY amount DESC
  LIMIT 3
) o;
```

### Q29 — DISTINCT ON (PostgreSQL-specific)
```sql
-- Latest order per customer
SELECT DISTINCT ON (customer_id)
       customer_id, order_id, order_date, amount
FROM orders
ORDER BY customer_id, order_date DESC;
```

### Q30 — FILTER Clause
```sql
SELECT
  COUNT(*) FILTER (WHERE status = 'completed') AS completed,
  COUNT(*) FILTER (WHERE status = 'pending') AS pending,
  AVG(amount) FILTER (WHERE status = 'completed') AS avg_completed_amount
FROM orders;
```

---

## Quick Revision: Key Concepts Interviewers Probe

| Topic | What They Ask |
|-------|--------------|
| `NULL` handling | `NULL = NULL` is false; use `IS NULL`, `COALESCE`, `NULLIF` |
| `WHERE` vs `HAVING` | WHERE filters rows before GROUP BY; HAVING filters groups |
| `UNION` vs `UNION ALL` | UNION deduplicates (slower); UNION ALL keeps all rows |
| Index types | B-tree (default), GIN (JSONB/arrays), GiST (geometry), BRIN (sorted large tables) |
| `EXPLAIN` keywords | Seq Scan, Index Scan, Bitmap Heap Scan, Hash Join, Sort |
| Transaction isolation | Read Committed (default), Repeatable Read, Serializable |
| `DELETE` vs `TRUNCATE` | DELETE is logged row-by-row; TRUNCATE is DDL, faster, non-rollbackable in some DBs |
| Temp tables vs CTEs | CTEs are query-scoped; temp tables persist for session; CTEs may be inlined by planner |

---

## Study Plan

1. **Days 1–2:** Window functions (Q1–Q5, Q21) — practice on LeetCode/StrataScratch
2. **Days 3–4:** CTEs, subqueries, recursive (Q6–Q8)
3. **Days 5–6:** Aggregation patterns, retention, funnel (Q12–Q14, Q22)
4. **Day 7:** PostgreSQL-specific (JSONB, LATERAL, DISTINCT ON, FILTER)
5. **Day 8:** Performance (EXPLAIN, indexing, partitioning)
6. **Days 9–10:** Mock interviews — combine concepts (sessionization + window + CTE)

**Practice Platforms:** StrataScratch, LeetCode SQL, DataLemur, HackerRank SQL
