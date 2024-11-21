import tkinter as tk

def click(button_text):
    if button_text == "=":
        try:
            result = str(eval(entry.get()))
            entry.delete(0, tk.END)
            entry.insert(tk.END, result)
        except Exception as e:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
    elif button_text == "C":
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, button_text)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Máy tính cơ bản")

# Tạo khung nhập liệu
entry = tk.Entry(root, width=16, font=("Arial", 24), justify="right")
entry.grid(row=0, column=0, columnspan=4)

# Tạo các nút
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    'C', '0', '=', '+'
]

row_value = 1
col_value = 0
for button in buttons:
    action = lambda x=button: click(x)
    tk.Button(root, text=button, width=5, height=2, font=("Arial", 18), command=action).grid(row=row_value, column=col_value)
    col_value += 1
    if col_value > 3:
        col_value = 0
        row_value += 1

# Chạy ứng dụng
root.mainloop()
