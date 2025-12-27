import sqlite3
from pathlib import Path
import csv
import random
ROOT = Path(__file__).resolve().parents[2] # relative to student workdir


print(ROOT)

CSV_FILE = ROOT / "task2/data.csv"
SOLUTION_FILE = ROOT / "task2/solution.sql"


def read_text(file: str) -> str:
        '''Get content of file'''
        path = Path(file)
        return path.read_text('utf-8')

def initialize_table(conn: sqlite3.Connection) -> None:
        with open(ROOT / "task2/data.csv", newline="", encoding="utf-8") as f:
            data = csv.DictReader(f)
            keys = tuple(next(data).keys())
            records = [tuple(d.values()) for d in data]
            random.shuffle(records)
            records = records[:80]
            
            sql_create_table = f'DROP TABLE IF EXISTS sales;CREATE TABLE sales ({", ".join(f"{k} text" for k in keys)});'
            try:
                conn.executescript(sql_create_table)
                sql = f"INSERT INTO sales ({', '.join(k for k in keys)}) VALUES ({','.join('?' for _ in range(len(keys)))})"
                conn.executemany(sql,records)
                conn.commit()
                print("Table created")
            except:
                    raise BaseException("Error While Creating the database table: sales")
            return records

def execute_script(conn: sqlite3.Connection, path:Path):
        sql = path.read_text("utf-8")
        conn.executescript(sql)

def fetchall(conn: sqlite3.Connection, query: str):
        '''Execute a query on the database'''
        try:
                return conn.execute(query).fetchall()         
        except Exception as e:
                print(e)
                return False


def test_users_csv_not_empty():
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
                try:
                        reader = csv.DictReader(f)
                        rows = [tuple(row.values()) for row in reader]
                        assert len(rows) == 100, 'YOU MUST NOT CHANGE task1/users.csv FILE!'
                except Exception:
                        assert False, 'ALTERing task2/data.csv IS NOT PERMITTED!'
                
def test_v_region_sales_summary_exists():
        conn = sqlite3.connect(":memory:")
        try:
                records = initialize_table(conn)
                execute_script(conn, SOLUTION_FILE)
                output = fetchall(conn, "SELECT * FROM v_region_sales_summary;")
                assert output != False, 'NO SUCH VIEW TABLE: v_region_sales_summary'
        finally:
                conn.close()

def test_v_region_sales_columns():
        conn = sqlite3.connect(":memory:")
        try:
                records = initialize_table(conn)
                execute_script(conn, SOLUTION_FILE)
                output = fetchall(conn, "SELECT * FROM v_region_sales_summary;")
                assert len(output[0]) == 3,'v_region_sales_summary should Have three columns'
        finally:
                conn.close()



def test_v_region_sales_summary_count():
        conn = sqlite3.connect(":memory:")
        try:
                records = initialize_table(conn)
                execute_script(conn, SOLUTION_FILE)
                output = fetchall(conn, "SELECT * FROM v_region_sales_summary;")
                counts = {}
                for rec in records:
                        counts[rec[3]] = counts.get(rec[3], 0) + 1 # rec[3] is the Region column
                assert all(count == counts[region] for region,count,*_ in output), 'VALUES OF COLUMN Sales_Count ARE NOT CORRECT'
        finally:
                conn.close()

def test_v_region_sales_summary_revenue():
        conn = sqlite3.connect(":memory:")
        try:
                records = initialize_table(conn)
                execute_script(conn, SOLUTION_FILE)
                output = fetchall(conn, "SELECT * FROM v_region_sales_summary;")
                counts = {}
                for rec in records:
                        counts[rec[3]] = counts.get(rec[3], 0) + float(rec[4]) * float(rec[7]) * (1 - float(rec[8])) # rec[3] is the Region column
                assert all(rev - counts[region] <= 1e-5 for region,_,rev in output), 'VALUES OF COLUMN Total_Revenue ARE NOT CORRECT'
        finally:
                conn.close()


def test_v_region_sales_summary_ordered():
        conn = sqlite3.connect(":memory:")
        try:
                records = initialize_table(conn)
                execute_script(conn, SOLUTION_FILE)
                output = fetchall(conn, "SELECT * FROM v_region_sales_summary;")
                counts = {}
                assert all(v1[2] >= v2[2] for v1,v2 in zip(output, output[1:])), 'RECORDS ARE NOT ORDERED BY Total_Revenue'
        finally:
                conn.close()
