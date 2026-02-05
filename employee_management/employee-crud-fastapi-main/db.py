# db.py
import os
from typing import Any, Dict, List, Optional

from mysql.connector import pooling, Error

# ---------- Configuration ----------
def _db_config() -> dict:
    return {
        "host": os.getenv("DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "root"),
        "database": os.getenv("DB_NAME", "employee_management"),
        # If you use MySQL 8 with native auth, this is fine; adjust if needed
        "auth_plugin": os.getenv("DB_AUTH_PLUGIN", "mysql_native_password"),
    }

_POOL: Optional[pooling.MySQLConnectionPool] = None


def init_db() -> None:
    """
    Initialize the database and employees table if they don't exist.
    Also initializes the main connection pool for the app.
    """
    cfg = _db_config()
    dbname = cfg["database"]

    # 1) Ensure DB exists (connect without database)
    admin_cfg = cfg.copy()
    admin_cfg.pop("database", None)

    admin_pool = pooling.MySQLConnectionPool(pool_name="admin_pool", pool_size=1, **admin_cfg)
    conn = admin_pool.get_connection()
    try:
        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{dbname}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        cur.execute(f"USE `{dbname}`;")
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INT NOT NULL,
                position VARCHAR(100) NOT NULL,
                department VARCHAR(100) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                salary DECIMAL(10,2) NOT NULL,
                experience INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB;
            """
        )
        conn.commit()
    finally:
        try:
            cur.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass

    # 2) Initialize app pool
    _init_pool()


def _init_pool() -> pooling.MySQLConnectionPool:
    global _POOL
    if _POOL is None:
        cfg = _db_config()
        _POOL = pooling.MySQLConnectionPool(
            pool_name="app_pool",
            pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
            **cfg
        )
    return _POOL


def _get_conn():
    pool = _init_pool()
    return pool.get_connection()


# ---------- Helpers ----------
def _row_to_dict(row: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert MySQL row (which may contain Decimal) to JSON-safe Python types.
    """
    out = dict(row)
    # Ensure salary is float (Decimal -> float)
    if "salary" in out and out["salary"] is not None:
        try:
            out["salary"] = float(out["salary"])
        except Exception:
            pass
    return out


# ---------- CRUD ----------
def fetch_all_employees() -> List[Dict[str, Any]]:
    conn = _get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT id, name, age, position, department, email, salary, experience
            FROM employees
            ORDER BY id ASC;
            """
        )
        rows = cur.fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()


def fetch_employee_by_id(emp_id: int) -> Optional[Dict[str, Any]]:
    conn = _get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT id, name, age, position, department, email, salary, experience
            FROM employees
            WHERE id = %s;
            """,
            (emp_id,),
        )
        row = cur.fetchone()
        return _row_to_dict(row) if row else None
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()


def insert_employee(emp: Dict[str, Any]) -> Dict[str, Any]:
    """
    emp should contain: name, age, position, department, email, salary, experience
    Returns the newly created employee dict.
    """
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO employees (name, age, position, department, email, salary, experience)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            (
                emp["name"],
                emp["age"],
                emp["position"],
                emp["department"],
                emp["email"],
                emp["salary"],
                emp["experience"],
            ),
        )
        conn.commit()
        new_id = cur.lastrowid
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()

    # Fetch back the inserted record
    created = fetch_employee_by_id(new_id)
    assert created is not None
    return created


def update_employee_by_id(emp_id: int, updated: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Full update (PUT-style). Returns the updated employee, or None if not found.
    """
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE employees
            SET name=%s, age=%s, position=%s, department=%s, email=%s, salary=%s, experience=%s
            WHERE id=%s;
            """,
            (
                updated["name"],
                updated["age"],
                updated["position"],
                updated["department"],
                updated["email"],
                updated["salary"],
                updated["experience"],
                emp_id,
            ),
        )
        conn.commit()
        if cur.rowcount == 0:
            return None
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()

    return fetch_employee_by_id(emp_id)


def delete_employee_by_id(emp_id: int) -> bool:
    conn = _get_conn()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM employees WHERE id=%s;", (emp_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        try:
            cur.close()
        except Exception:
            pass
        conn.close()