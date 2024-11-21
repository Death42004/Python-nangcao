import psycopg2
from psycopg2 import sql
from tkinter import messagebox  # Import messagebox để sử dụng các thông báo

def connect_db(db_name, user, password, host, port):
    """Hàm kết nối cơ sở dữ liệu PostgreSQL."""
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()
        messagebox.showinfo("Success", "Kêt nối thành công!")
        return conn, cur
    except Exception as e:
        messagebox.showerror("Error", f"Error connecting to the database: {e}")
        return None, None

def load_data(cursor, table_name, text_widget):
    """Hàm tải dữ liệu từ bảng và hiển thị lên Text widget."""
    try:
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
        cursor.execute(query)
        rows = cursor.fetchall()
        text_widget.delete(1.0, 'end')
        for row in rows:
            text_widget.insert('end', f"{row}\n")
    except Exception as e:
        messagebox.showerror("Error", f"Error loading data: {e}")
