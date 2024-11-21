from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Cấu hình kết nối tới PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1@localhost:5432/quanlidanhsach'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Dùng cho session
db = SQLAlchemy(app)

# Mô hình User (Sinh viên)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mssv = db.Column(db.String(10), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.name} - {self.mssv}>"

# Trang chọn vai trò (giáo viên hoặc sinh viên)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        code = request.form['code']
        
        if code == '123':  # Giáo viên
            session['is_teacher'] = True
            flash('Đăng nhập với vai trò giáo viên thành công!', 'success')
        elif code == '456':  # Sinh viên
            session['is_teacher'] = False
            flash('Đăng nhập với vai trò sinh viên thành công!', 'success')
        else:
            flash('Mã đăng nhập không đúng, vui lòng thử lại.', 'danger')
            return redirect(url_for('login'))
        
        return redirect(url_for('index'))

    return render_template('login.html')

# Đăng xuất
@app.route('/logout')
def logout():
    session.pop('is_teacher', None)
    flash('Đăng xuất thành công!', 'success')
    return redirect(url_for('login'))

# Trang chủ - Hiển thị danh sách người dùng
@app.route('/')
def index():
    if 'is_teacher' not in session:
        return redirect(url_for('login'))
    
    users = User.query.all()
    if session['is_teacher']:
        return render_template('index_teacher.html', users=users)
    else:
        return render_template('index.html', users=users)

# Thêm người dùng mới (Giáo viên)
@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if 'is_teacher' not in session or not session['is_teacher']:
        flash('Chỉ giáo viên mới có quyền thêm người dùng.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form['name']
        mssv = request.form['mssv']
        new_user = User(name=name, mssv=mssv)
        db.session.add(new_user)
        db.session.commit()
        flash('Người dùng đã được thêm thành công!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_user.html')

# Sửa thông tin người dùng (Giáo viên)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    if 'is_teacher' not in session or not session['is_teacher']:
        flash('Chỉ giáo viên mới có quyền sửa thông tin người dùng.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        user.name = request.form['name']
        user.mssv = request.form['mssv']
        db.session.commit()
        flash('Thông tin người dùng đã được cập nhật!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit_user.html', user=user)

# Xóa người dùng (Giáo viên)
@app.route('/delete/<int:id>')
def delete_user(id):
    if 'is_teacher' not in session or not session['is_teacher']:
        flash('Chỉ giáo viên mới có quyền xóa người dùng.', 'danger')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('Người dùng đã được xóa!', 'success')
    return redirect(url_for('index'))

# Hàm tạo bảng khi ứng dụng bắt đầu
def create_tables():
    with app.app_context():
        db.create_all()

# Chạy ứng dụng Flask và tạo bảng khi bắt đầu
if __name__ == '__main__':
    create_tables()  # Tạo bảng ngay khi ứng dụng bắt đầu
    app.run(debug=True)
