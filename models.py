from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from database import db

basic = db('./users.db')


class User(basic.Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(128))

    def __init__(self, username):
        self.username = username
        self.db_session = basic.db_session

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)





# a = User("endg")
# a.set_password("22w2")
#
# basic.db_session.add(a)
# basic.db_session.commit()

# # 查询表中的所有数据
# users = basic.db_session.query(User).all()
#
# # 打印所有用户信息
# for user in users:
#     print(f"ID: {user.id}, Username: {user.username}, Password Hash: {user.password_hash}")
#
#
# basic.db_session.close()