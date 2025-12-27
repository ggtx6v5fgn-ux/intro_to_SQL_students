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
def create_and_populate_table(conn: sqlite3.Connection, table_name: str, csv_file: Path):
        with open(csv_file, newline="", encoding="utf-8") as f:
            data = csv.DictReader(f)
            keys = tuple(next(data).keys())
            records = [tuple(d.values()) for d in data]
            random.shuffle(records)

            try:
                sql_create = f"DROP TABLE IF EXISTS {table_name}; CREATE TABLE {table_name} ({", ".join(f"{k} text" for k in keys)});"
                sql_poplulate = f"INSERT INTO {table_name} ({', '.join(k for k in keys)}) VALUES ({','.join('?' for _ in range(len(keys)))})"

                conn.executescript(sql_create)
                conn.executemany(sql_poplulate,records)
                conn.commit()
            except:
                    raise BaseException("Error while populating the table {table_name}")
            return records



def initialize_tables(conn: sqlite3.Connection) -> list:
        user_recs = create_and_populate_table(conn, "users", ROOT / "task3/users.csv")
        server_recs = create_and_populate_table(conn, "server_logs", ROOT / "task3/server_logs.csv")
        return user_recs, server_recs


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
        files= ["users", "server_logs"]
        lens = [20, 100]
        for i in range(2):
            try: 
                with open(ROOT / f"task3/{files[i]}.csv", newline="", encoding="utf-8") as f:
                        try:
                                reader = csv.DictReader(f)
                                rows = [tuple(row.values()) for row in reader]
                                assert len(rows) == lens[i], f'YOU MUST NOT CHANGE task3/{files[i]} FILE!'
                        except Exception:
                                assert False, 'ALTERING CSV FILES IS NOT PERMITTED!'
            except:
                   assert False, "CSV FILES NOT FOUND IN ./task3/"
                    
def test_new_column_added_to_server_logs():
        conn = sqlite3.connect(":memory:")
        try:
            import datetime
            user_recs, server_recs = initialize_tables(conn)
            execute_script(conn, ROOT/"task3/solution.sql")
            session_durs = fetchall(conn, "SELECT Session_Dur FROM server_logs;")
            assert session_durs, "Column Session_Dur DOES NOT EXIST!"
        finally:
            conn.close()


def test_session_durations_correct():
        conn = sqlite3.connect(":memory:")
        try:
            import datetime
            user_recs, server_recs = initialize_tables(conn)
            execute_script(conn, ROOT/"task3/solution.sql")
            session_durs = fetchall(conn, "SELECT Session_Dur FROM server_logs;")
            for server_rec, dur_rec in zip(server_recs, session_durs):
                    time_dif = (datetime.datetime.strptime(server_rec[3],"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(server_rec[2],"%Y-%m-%d %H:%M:%S")).total_seconds() / 60
                    assert (time_dif - dur_rec[0] < 1e-5)
        finally:
            conn.close()

def test_v_user_activity_exists():
        conn = sqlite3.connect(":memory:")
        try:
            _ = initialize_tables(conn)
            execute_script(conn, ROOT/"task3/solution.sql")
            activity_recs = fetchall(conn, "SELECT * FROM v_users_activity;")
            assert activity_recs, 'VIEW v_users_activity WAS NOT FOUND'
        finally:
            conn.close()

def test_v_users_activity_correct():
        conn = sqlite3.connect(":memory:")
        try:
            import datetime
            user_recs, server_recs = initialize_tables(conn)
            execute_script(conn, ROOT/"task3/solution.sql")
            activity_recs = fetchall(conn, "SELECT * FROM v_users_activity;")
            user_dict = {}
            for rec in server_recs:
                  time_dif = (datetime.datetime.strptime(rec[3],"%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(rec[2],"%Y-%m-%d %H:%M:%S")).total_seconds() / 60
                  user_dict[rec[1]] = user_dict.get(rec[1],[])
                  user_dict[rec[1]].append(time_dif)
            assert all([len(user_dict[rec[0]]) == rec[3] for rec in activity_recs]), 'FOUND INCORRECT Num_Sessions ENTRY'
            assert all([sum(user_dict[rec[0]]) - rec[4] < 1e-5 for rec in activity_recs ]), 'FOUND INCORRECT Total_Session_Time ENTRY'
        finally:
            conn.close()

