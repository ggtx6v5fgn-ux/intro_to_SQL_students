# How to submit Solution
This homework will be automatically validated using CI workflows in github.
To work correctly:
1. Fork this repository to your github account, then clone the forked repo to your local machine.
2. In your github repository, go to the tab "Actions" and enable them to be able to check your solution status.
3. Solve all the tasks. You can check the correctness of each solution by using `pytest` [you need to install pytest if not already installed], just run `pytest -x task1/` for task1 validation, `pytest -x task2/` for task2, and so on.
4. After solving all the tasks, commit your local changes and push them to your remote account using the command : `git push`. Make sure you are pushing as the same owner of the remote repo which you forked. 
5. Whenever you push the local repo, an automated test will validate your solution inside github, go to actions tab and check the correctness of your solution. A green check means all tests passed successfully and your solution is 100% correct.


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




Your task is to write an SQL query which will grab all users whose ages are between 20 and 30 (inclusive), ordered by age in ascending order. You must drop the attribute "id" of the table `users`, and only include three attributes : first_name, last_name, age. Also, your query must be wrapped in a  "view" object. 
A view is a virtual table whose contents are defined by a SELECT query.
It does not store data.
It stores the query.


### Hints:
1. To create a new view, type:
`CREATE VIEW {view_name} AS 
{QUERY};`
by executing the previous command, you will have a view object named {view_name} which contains the result of running {QUERY}.
2. Checkout the command `ORDER BY` to sort the records according to ages.

3. You should write your solution inside `task1/solution.sql` file. Do not change other files in the repo.

4. Upon solving the task, you can check your solution by running:
> pytest -q -x task1/