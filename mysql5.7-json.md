|MySQL 5.7 supports CRUD operations on JSON data. CRUD stands for Create, Read, Update, and Delete.|
|--------------------------------------------------------------------------------------------------|

**Create**

To create a JSON document in MySQL, you can use the following SQL statement:

```
INSERT INTO table (json_column)
VALUES ('{ "name": "John Doe", "age": 30 }');
```

**Read**

To read a JSON document from MySQL, you can use the following SQL statement:

```
SELECT json_column
FROM table
WHERE id = 1;
```

This will return the following JSON document:

```
{
  "name": "John Doe",
  "age": 30
}
```

**Update**

To update a JSON document in MySQL, you can use the following SQL statement:

```
UPDATE table
SET json_column = JSON_SET(json_column, "$.age", 31)
WHERE id = 1;
```

This will update the age of the JSON document to 31.

**Delete**

To delete a JSON document from MySQL, you can use the following SQL statement:

```
DELETE FROM table
WHERE id = 1;
```

This will delete the JSON document with the ID of 1.

Here are some additional examples of CRUD operations on JSON data in MySQL:

**Create a JSON document with multiple properties**

```
INSERT INTO table (json_column)
VALUES ('{ "name": "John Doe", "age": 30, "address": { "city": "New York", "state": "NY" } }');
```

**Read a specific property from a JSON document**

```
SELECT address.city
FROM table
WHERE id = 1;
```

This will return the city of the JSON document with the ID of 1.

**Update a property in a JSON document**

```
UPDATE table
SET json_column = JSON_SET(json_column, "$.address.city", "Los Angeles")
WHERE id = 1;
```

This will update the city of the JSON document to Los Angeles.

**Delete a property from a JSON document**

```
UPDATE table
SET json_column = JSON_REMOVE(json_column, "$.address.city")
WHERE id = 1;
```

This will delete the city property from the JSON document.


| JSON object in MySQL using the `JSON_SET()` function |
|------------------------------------------------------|

1. First, you need to create a JSON object. You can do this by using the `JSON_OBJECT()` function. For example, the following code will create a JSON object with the key `"name"` and the value `"John Doe"`:

```sql
SELECT JSON_OBJECT('name', 'John Doe');
```

2. Once you have created a JSON object, you can update it by using the `JSON_SET()` function. For example, the following code will update the value of the `"name"` key to `"Jane Doe"`:

```sql
SELECT JSON_SET(
    JSON_OBJECT('name', 'John Doe'),
    "$.name",
    'Jane Doe'
);
```

3. The result of the `JSON_SET()` function is a new JSON object with the value of the `"name"` key updated. For example, the following code will print the new JSON object:

```sql
SELECT JSON_SET(
    JSON_OBJECT('name', 'John Doe'),
    "$.name",
    'Jane Doe'
);
```

The output of the above code will be the following JSON object:

```json
{
  "name": "Jane Doe"
}
```


** Update a JSON object in MySQL using the `JSON_SET()` function:

```sql
SELECT JSON_SET(
    JSON_OBJECT('name', 'John Doe', 'age', 30),
    "$.age",
    40
);
```

The output of the above code will be the following JSON object:

```json
{
  "name": "John Doe",
  "age": 40
}
```

** UPDATE

```
UPDATE mytable SET json_value = JSON_SET(json_value, "$.name", 'Jane Doe');
```

** Append an element to an array of data in MySQL using the `UPDATE` statement

```sql
UPDATE mytable SET array_data = JSON_ARRAY_APPEND(array_data, '$', 'John Doe');
```

The `UPDATE` statement will append the element `John Doe` to the end of the array in the `array_data` column. The new value of the array data is the following array:

```json
["Jane Doe", "John Doe"]
```

|JSON_ARRAY_APPEND|
|-----------------|

```sql
-- Append a value to an array
SELECT JSON_ARRAY_APPEND('[1, 2, 3]', '$', 4) AS 'Result';

-- Append a value to an array that's nested inside another array
SELECT JSON_ARRAY_APPEND('[1, 2, [3, 4]]', '$[2]', 5) AS 'Result';

-- Append a value to a JSON object
SELECT JSON_ARRAY_APPEND('{"name": "John Doe"}', '$.age', 30) AS 'Result';
```

The output of the above queries will be the following JSON values:

```json
[1, 2, 4]
[1, 2, [3, 5]]
{"name": "John Doe", "age": 30}
```

**more examples of how to use the `JSON_ARRAY_APPEND()`:

```sql
-- Append multiple values to an array
SELECT JSON_ARRAY_APPEND('[1, 2, 3]', '$', [4, 5, 6]) AS 'Result';

-- Append a value to an array that's nested inside a JSON object
SELECT JSON_ARRAY_APPEND('{"name": "John Doe", "children": [{"name": "Jane Doe"}, {"name": "Peter Doe"}]}', '$.children[0].name', 'Mary Doe') AS 'Result';

-- Append a value to a JSON object that's nested inside an array
SELECT JSON_ARRAY_APPEND('[{"name": "John Doe"}, {"name": "Jane Doe"}]', '$[0].age', 30) AS 'Result';
```

The output of the above queries will be the following JSON values:

```json
[1, 2, 4, 5, 6]
{"name": "John Doe", "children": [{"name": "Jane Doe"}, {"name": "Peter Doe"}, {"name": "Mary Doe"}]}
{"name": "John Doe", "age": 30}
```


```sql
-- Append multiple values to an array
UPDATE mytable SET array_data = JSON_ARRAY_APPEND(array_data, '$', [5, 6, 7]);

-- Append a value to an array that's nested inside a JSON object
UPDATE mytable SET array_data = JSON_ARRAY_APPEND(array_data, '$.children[0].name', 'Mary Doe');

-- Append a value to a JSON object that's nested inside an array
UPDATE mytable SET array_data = JSON_ARRAY_APPEND(array_data, '$[0].age', 30);
```

```json
[1, 2, 3, 4, 5, 6, 7]
{"name": "John Doe", "children": [{"name": "Jane Doe"}, {"name": "Peter Doe"}, {"name": "Mary Doe"}]}
{"name": "John Doe", "age": 30}
```

|SPLIT|
|-----|

The `SUBSTRING_INDEX()` function in MySQL returns a substring of a string before a specified number of delimiters occur. The function takes three arguments:

* `str`: The string to be searched.
* `delim`: The delimiter to search for.
* `count`: The number of times to search for the delimiter.

If `count` is positive, the function returns the substring of `str` before the first `count` occurrences of `delim`. If `count` is negative, the function returns the substring of `str` after the last `count` occurrences of `delim`. If `count` is 0, the function returns the entire string `str`.

For example, the following query will return the first word in the string `"This is a string"`:

```sql
SELECT SUBSTRING_INDEX("This is a string", " ", 1);
```

The output of the query will be the following string:

```
This
```

The following query will return the last word in the string `"This is a string"`:

```sql
SELECT SUBSTRING_INDEX("This is a string", " ", -1);
```

The output of the query will be the following string:

```
string
```

The following query will return the entire string `"This is a string"`:

```sql
SELECT SUBSTRING_INDEX("This is a string", " ", 0);
```

The output of the query will be the following string:

```
This is a string
```

|advanced MySQL 5 queries|
|------------------------|

* **`JOIN` query:** The following query will join the `customers` table and the `orders` table on the `customer_id` column:

```sql
SELECT *
FROM customers
JOIN orders
ON customers.customer_id = orders.customer_id;
```

The output of the query will be a table that contains all of the rows from the `customers` table and the corresponding rows from the `orders` table.

* **`GROUP BY` query:** The following query will group the `orders` table by the `customer_id` column and calculate the total number of orders for each customer:

```sql
SELECT customer_id, COUNT(*) AS total_orders
FROM orders
GROUP BY customer_id;
```

The output of the query will be a table that contains the `customer_id` column and the `total_orders` column. The `total_orders` column will contain the number of orders for each customer.

* **`HAVING` clause:** The following query will group the `orders` table by the `customer_id` column and calculate the total number of orders for each customer. The query will then filter the results to only include customers who have placed more than 10 orders:

```sql
SELECT customer_id, COUNT(*) AS total_orders
FROM orders
GROUP BY customer_id
HAVING total_orders > 10;
```

The output of the query will be a table that contains the `customer_id` column and the `total_orders` column. The `total_orders` column will contain the number of orders for each customer who has placed more than 10 orders.

* **`SUBQUERY`:** The following query will find the customer who has placed the most orders:

```sql
SELECT customer_id, COUNT(*) AS total_orders
FROM orders
GROUP BY customer_id
ORDER BY total_orders DESC
LIMIT 1;
```

The output of the query will be a table that contains the `customer_id` column and the `total_orders` column. The `customer_id` column will contain the ID of the customer who has placed the most orders.

* **`FUNCTION`:** The following query will find the average order value:

```sql
SELECT AVG(total_price) AS average_order_value
FROM orders;
```

The output of the query will be a single value, which is the average order value.

* **`Stored Procedure:** The following is an example of a stored procedure:

```sql
DELIMITER $$

CREATE PROCEDURE get_customers_by_country(country VARCHAR(255))
BEGIN

SELECT *
FROM customers
WHERE country = @country;

END$$

DELIMITER ;
```

* **Find the top 10 customers who have spent the most money:**
```sql
SELECT customer_id, COUNT(*) AS total_orders, SUM(total_price) AS total_spent
FROM orders
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;
```

* **Find the average order value for each product category:**
```sql
SELECT product_category, AVG(total_price) AS average_order_value
FROM orders
GROUP BY product_category;
```

* **Find the number of orders placed each month:**
```sql
SELECT YEAR(order_date) AS year, MONTH(order_date) AS month, COUNT(*) AS number_of_orders
FROM orders
GROUP BY YEAR(order_date), MONTH(order_date);
```

* **Find the customer who has placed the most orders in the last 30 days:**
```sql
SELECT customer_id, COUNT(*) AS total_orders
FROM orders
WHERE order_date >= CURDATE() - INTERVAL 30 DAY
GROUP BY customer_id
ORDER BY total_orders DESC
LIMIT 1;
```

* **Find the products that have been ordered the most times:**
```sql
SELECT product_id, COUNT(*) AS number_of_orders
FROM orders
GROUP BY product_id
ORDER BY number_of_orders DESC;
```


* **IF statement with multiple conditions:** The following query will return the string "You are an adult" if the value of the `age` column is greater than or equal to 18, the string "You are a teenager" if the value of the `age` column is between 13 and 17, and the string "You are a child" if the value of the `age` column is less than 13:

```sql
SELECT IF(age >= 18, 'You are an adult', IF(age BETWEEN 13 AND 17, 'You are a teenager', 'You are a child'));
```

* **FOR loop:** The following query will print the numbers from 1 to 10:

```sql
FOR i IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10) DO

    SELECT i;

END LOOP;
```

* **Nested FOR loops:** The following query will print the numbers from 1 to 10, and for each number, it will print the number of times that number appears in the table:

```sql
FOR i IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10) DO

    SELECT COUNT(*) AS number_of_occurrences
    FROM numbers
    WHERE number = i;

END LOOP;
```

