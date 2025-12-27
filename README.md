# How to submit Solution
This homework will be automatically validated using CI workflows in github.
To work correctly:
1. Fork this repository to your github account, then clone the forked repo to your local machine.
2. In your github repository, go to the tab "Actions" and enable them to be able to check your solution status.
3. Solve all the tasks. You should validate your solution by creating unit tests. This will not affect the final score, but it is recommended before submitting your solution.
4. After solving all the tasks, commit your local changes and push them to your remote account using the command : `git push`. Make sure you are pushing as the same owner of the remote repo which you forked. 
5. Whenever you push the local repo, an automated test will validate your solution inside github, go to actions tab and check the correctness of your solution. A green check means all tests passed successfully and your solution is 100% correct. Otherwise, You will get an error message, which means that your solution didn't pass all tests.


# Tasks desctiptions
## Task 1:
In this task you will write SQL query to extract information from a database table.
You are given a table with the name `users`, with the following schema:
` CREATE TABLE users (
    id integer PRIMARY KEY,
    first_name text,
    last_name text,
    age integer
);`




Your task is to write an SQL query which will grab all users whose ages are between 20 and 30 (inclusive), ordered by age in ascending order. You must drop the attribute "id" of the table `users`, and only include three attributes : first_name, last_name, age. Also, your query must be wrapped in a  "view" object named "v_users_age". 
A view is a virtual table whose contents are defined by a SELECT query.
It does not store data.
It stores the query.


### Hints:
1. To create a new view, type:
`CREATE VIEW {view_name} AS 
{QUERY};`
by executing the previous command, you will have a view object named {view_name} which contains the result of running {QUERY}.
2. Checkout the command `ORDER BY` to sort the records according to ages.

You should write your solution inside `task1/solution.sql` file. Do not change other files in the repo.



## Task 2:
You are given a database which contains sales records for multiple products. data are provided in the file task2/data.csv , The database is already generated with the following schema: 

`CREATE TABLE sales (Product_ID text, Sale_Date text, Sales_Rep text, Region text, Quantity_Sold text, Product_Category text, Unit_Cost text, Unit_Price text, Discount text);`

You will be asked to perform the following Queries on the database:
1. Create a view named "v_region_sales_summary" that contains the following columns (in the  same order):
Region
Sales_Count — number of sales in that Region
Total_Revenue — total some of Prices after discount 
The view must include all Regions present in the table, ordered by total_revenue from largest to lowest.

Write your SQL code inside `task2/solution.sql`

## Task 3:
In this task you will use SQL Commands : `HAVING`, `JOIN`.
Suppose you were asked to provide information about the activity of users during workign hours. You are provided with two databases: users, and server_logs.
`users` contain simple data about empolyees in the company, such as name, and Id .. 
`server_logs` contains inforamtion about logins to the server:
- Log_ID: primary key
- Session_Start : the exact time a sessions has started.
- Session_End : the time at which the session was closed.
- User_ID : the ID of the user who logged in during this session.

You were asked to create the following :
1. Create a new column in `server_logs` named : `Session_Dur`, which contains the amount  of time (in minutes) the session was open. You can convert the date into days using SQL function `julianday())`.
2. Create a view named `v_users_activity`, containing the following fields: 
- `User_ID`
- `First_Name`
- `Last_Name`
- `Num_Sessions`: Total Number of sessions that were opened by the user.
- `Total_Session_Time` : Total time (in minutes) the user worked on a sesssion.
and ordered by `Total_Session_Time` descending.

You will need to implement LEFT JOIN between `users` and `server_logs`.

Your solution for the two tasks should be written inside `task3/solution.sql`.