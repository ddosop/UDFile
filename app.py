import os

from flask import Flask, request, send_from_directory, redirect, url_for, session, render_template
from models import User


app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = './files'


@app.route('/', methods=['GET'])
def root():
    return render_template("login.html")


@app.route('/index', methods=['GET'])
def index():
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    try:
        error_message = session.get('index_error')
    except KeyError:
        error_message = None
    return render_template('index.html', uploaded_files=uploaded_files, error_message=error_message)

# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            error_massage = "请注册后登录！"
            return render_template('login.html', error_message=error_massage)
    return render_template('login.html')


# 用户注册
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username)
        new_user.set_password(password)
        new_user.db_session.add(new_user)
        new_user.db_session.commit()
        new_user.db_session.close()
        return redirect(url_for('login'))
    return render_template('signup.html')


# 登出
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


# 检查用户是否登录的装饰器
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/upload', methods=['POST'], endpoint='upload_file')
@login_required
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        session["index_error"] = 'No selected file'
        return redirect(url_for('index'))
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return redirect(url_for('index'))


@app.route('/download/<filename>', methods=['GET'], endpoint='download_file')
@login_required
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)