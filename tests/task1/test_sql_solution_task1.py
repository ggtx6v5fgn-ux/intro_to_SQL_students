import sqlite3
from pathlib import Path
import csv
import random
ROOT = Path(__file__).resolve().parents[2] # relative to student workdir


print(ROOT)

CSV_FILE = ROOT / "task1/users.csv"
SOLUTION_FILE = ROOT / "task1/solution.sql"


def read_text(file: str) -> str:
        '''Get content of file'''
        path = Path(file)
        return path.read_text('utf-8')

def initialize_table(conn: sqlite3.Connection) -> None:
        '''execute a full script written from file '''
        path = Path(ROOT / "task1/seed.sql")
        sql = path.read_text('utf-8')
        conn.executescript(sql)
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = [(row["first_name"], row["last_name"], row["age"]) for row in reader]
                random.shuffle(rows)
        conn.executemany(
                "INSERT INTO users (first_name, last_name, age) VALUES (?,?,?)",
                rows
        )
        conn.commit()

def execute_script(conn: sqlite3.Connection, path:Path):
        sql = path.read_text("utf-8")
        conn.executescript(sql)

def fetchall(conn: sqlite3.Connection, query: str):
        '''Execute a query on the database'''
        try:
                return conn.execute(query).fetchall()
                
        except Exception:
                return False


def test_users_csv_not_empty():
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
                try:
                        reader = csv.DictReader(f)
                        rows = [(row["first_name"], row["last_name"], row["age"]) for row in reader]
                        assert len(rows) == 20, 'YOU MUST NOT CHANGE task1/users.csv FILE!'
                except Exception:
                        assert False, 'ALTERED task1/users.csv IS NOT PERMITTED!'
                
def test_view_users_age_exists():
        conn = sqlite3.connect(":memory:")
        try:
                records = initialize_table(conn)
                execute_script(conn, SOLUTION_FILE)
                output = fetchall(conn, "SELECT * FROM v_users_age;")
                assert output != False, 'NO SUCH VIEW TABLE: v_users_age'
        finally:
                conn.close()
def test_view_users_age_columns():
        conn = sqlite3.connect(":memory:")
        try:
                records = initialize_table(conn)
                execute_script(conn, SOLUTION_FILE)
                output = fetchall(conn, "SELECT * FROM v_users_age;")
                assert len(output[0]) == 3,'MISSING COLUMNS IN V_USERS_AGE'
        finally:
                conn.close()



def test_view_users_age_age():
        conn = sqlite3.connect(":memory:")
        try:
                initialize_table(conn)
                execute_script(conn, SOLUTION_FILE)
                output = fetchall(conn, "SELECT * FROM v_users_age;")
                age_list = [age for (_,_,age) in output]
                assert all(20 <= age <= 30 for age in age_list), 'FOUND A RECORD NOT MATCHING AGE CONSTRAINTS: 20<=AGE<=30'
        finally:
                conn.close()

def test_view_users_age_sorted():
        conn = sqlite3.connect(":memory:")
        try:
                initialize_table(conn)
                execute_script(conn, SOLUTION_FILE)
                output = fetchall(conn, "SELECT * FROM v_users_age;")
                age_list = [age for (_,_,age) in output]
               
                assert sorted(age_list) == age_list, 'RECORDS SHOULD BE ORDERED BY AGE IN ASCENDING ORDER'

        finally:
                conn.close()
