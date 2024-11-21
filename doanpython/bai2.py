import tkinter as tk
from tkinter import messagebox
import csv
from d import connect_db  # Import kết nối cơ sở dữ liệu từ file d.py

class LMSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Learning Management System")

        # Phần đăng nhập
        self.db_name = tk.StringVar(value='quanly')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='1')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='students')

        # Biến lưu trữ kết nối và con trỏ cơ sở dữ liệu
        self.conn = None
        self.cur = None

        # Tạo giao diện người dùng
        self.create_widgets()

    def create_widgets(self):
        # Frame cập nhật
        update_frame = tk.Frame(self.root)
        update_frame.pack(pady=10)

        tk.Label(update_frame, text="MSSV:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(update_frame, textvariable=self.mssv, width=30).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(update_frame, text="Họ tên:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(update_frame, textvariable=self.name, width=30).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(update_frame, text="Khóa học:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(update_frame, textvariable=self.course, width=30).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(update_frame, text="Điểm:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(update_frame, textvariable=self.grade, width=30).grid(row=3, column=1, padx=5, pady=5)

        # Nút chức năng
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Thêm", command=self.add_data).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Xóa", command=self.delete_data).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Sửa", command=self.update_data).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="Xuất CSV", command=self.export_to_csv).grid(row=0, column=3, padx=5, pady=5)

        # Phần hiển thị dữ liệu
        self.data_display = tk.Text(self.root, height=10, width=80)
        self.data_display.pack(pady=10)

        self.load_data()

    def add_data(self):
        mssv, name, course = self.mssv.get(), self.name.get(), self.course.get()
        try:
            grade = float(self.grade.get())
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Điểm phải là số hợp lệ!")
            return

        query = "INSERT INTO students (mssv, name, course, grade) VALUES (%s, %s, %s, %s)"
        try:
            self.cur.execute(query, (mssv, name, course, grade))
            self.conn.commit()
            messagebox.showinfo("Thông báo", "Thêm mới thành công!")
            self.clear_entries()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi khi thêm dữ liệu: {str(e)}")

    def delete_data(self):
        mssv = self.mssv.get()
        if not mssv:
            messagebox.showerror("Lỗi", "Vui lòng nhập MSSV để xóa!")
            return

        try:
            self.cur.execute("DELETE FROM students WHERE mssv = %s", (mssv,))
            self.conn.commit()
            messagebox.showinfo("Thông báo", "Dữ liệu đã được xóa!")
            self.clear_entries()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi khi xóa dữ liệu: {str(e)}")

    def update_data(self):
        mssv, name, course = self.mssv.get(), self.name.get(), self.course.get()
        try:
            grade = float(self.grade.get())
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Điểm phải là số hợp lệ!")
            return

        query = "UPDATE students SET name = %s, course = %s, grade = %s WHERE mssv = %s"
        try:
            self.cur.execute(query, (name, course, grade, mssv))
            self.conn.commit()
            messagebox.showinfo("Thông báo", "Cập nhật thành công!")
            self.clear_entries()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi khi cập nhật dữ liệu: {str(e)}")

    def load_data(self):
        self.cur.execute("SELECT * FROM students")
        rows = self.cur.fetchall()
        self.data_display.delete(1.0, tk.END)
        for row in rows:
            self.data_display.insert(tk.END, f"{row}\n")

    def export_to_csv(self):
        self.cur.execute("SELECT * FROM students")
        rows = self.cur.fetchall()
        filename = "students_data.csv"
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["MSSV", "Name", "Course", "Grade"])
            writer.writerows(rows)
        messagebox.showinfo("Thông báo", f"Dữ liệu đã được xuất ra file {filename}")

    def clear_entries(self):
        self.mssv.set("")
        self.name.set("")
        self.course.set("")
        self.grade.set("")

# Chạy ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = LMSApp(root)
    root.mainloop()
