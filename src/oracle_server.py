import os
import sys
import oracledb
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Oracle-DB-Server")

def get_connection():
    """Lấy connection từ biến môi trường"""
    return oracledb.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN")
    )

@mcp.tool()
def query_data(sql: str) -> str:
    """
    Query dữ liệu từ Oracle DB.
    
    Args:
        sql: Câu lệnh SELECT
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                if not rows:
                    return "No data found"
                
                columns = [desc[0] for desc in cursor.description]
                col_widths = [len(col) for col in columns]
                
                for row in rows:
                    for i, val in enumerate(row):
                        col_widths[i] = max(col_widths[i], len(str(val)) if val is not None else 4)
                
                header = " | ".join(col.ljust(col_widths[i]) for i, col in enumerate(columns))
                separator = "-+-".join("-" * w for w in col_widths)
                
                result = header + "\n" + separator + "\n"
                for row in rows:
                    result += " | ".join(str(val).ljust(col_widths[i]) if val is not None else "NULL".ljust(col_widths[i]) for i, val in enumerate(row)) + "\n"
                
                return result
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
def insert_data(table: str, columns: str, values: str) -> str:
    """
    Thêm dữ liệu vào table.
    
    Args:
        table: Tên table
        columns: Danh sách cột (vd: "id, name, age")
        values: Giá trị tương ứng (vd: "1, 'John', 30")
    """
    try:
        sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                conn.commit()
                return f"✅ Inserted into {table}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
def update_data(table: str, set_clause: str, where_clause: str) -> str:
    """
    Cập nhật dữ liệu.
    
    Args:
        table: Tên table
        set_clause: Phần SET (vd: "name='Jane', age=25")
        where_clause: Điều kiện WHERE (vd: "id=1")
    """
    try:
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                conn.commit()
                return f"✅ Updated {cursor.rowcount} row(s)"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
def delete_data(table: str, where_clause: str) -> str:
    """
    Xóa dữ liệu.
    
    Args:
        table: Tên table
        where_clause: Điều kiện WHERE (vd: "id=1")
    """
    try:
        sql = f"DELETE FROM {table} WHERE {where_clause}"
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                conn.commit()
                return f"✅ Deleted {cursor.rowcount} row(s)"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
def inspect_table(table_name: str) -> str:
    """
    Xem cấu trúc table.
    
    Args:
        table_name: Tên table
    """
    try:
        sql = f"SELECT column_name, data_type, nullable FROM user_tab_columns WHERE table_name = UPPER('{table_name}')"
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                result = f"Table: {table_name}\n"
                for row in rows:
                    result += f"  {row[0]} {row[1]} {'NULL' if row[2]=='Y' else 'NOT NULL'}\n"
                return result
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
def inspect_package(package_name: str) -> str:
    """
    Xem source code của package.
    
    Args:
        package_name: Tên package
    """
    try:
        sql = f"SELECT text FROM user_source WHERE name = UPPER('{package_name}') AND type = 'PACKAGE' ORDER BY line"
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                result = f"Package: {package_name}\n"
                for row in rows:
                    result += row[0]
                return result
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
def inspect_procedure(procedure_name: str) -> str:
    """
    Xem source code của procedure.
    
    Args:
        procedure_name: Tên procedure
    """
    try:
        sql = f"SELECT text FROM user_source WHERE name = UPPER('{procedure_name}') AND type = 'PROCEDURE' ORDER BY line"
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                result = f"Procedure: {procedure_name}\n"
                for row in rows:
                    result += row[0]
                return result
    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == "__main__":
    sys.stderr.write("Oracle DB MCP Server is running...\n")
    mcp.run()
