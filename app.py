from flask import Flask,render_template,request,url_for
from controllers.database import db
from controllers.config import config
from controllers.model import User
from flask_login import LoginManager
from werkzeug.security import generate_password_hash



app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def create_admin():
    if_exist = User.query.filter_by(is_admin=True).first()
    if not if_exist:
        admin = User(
            username = 'admin123',
            email='admin1234@gmail.com',
            password=generate_password_hash('admin1234'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()

with app.app_context():
    db.create_all()
    create_admin()

@app.route("/")
def home():
    return render_template("Homepage.html")

from controllers.auth_route import *
from controllers.admin_route import *
from controllers.staff_route import *

if __name__ == "__main__":
    app.run(debug=False)