from flask import Flask, render_template
from flask_login import LoginManager
from flask_login import login_required, login_user, logout_user
from flask import request, redirect, url_for
from flask_login import current_user
import config

# from models.mockdbhelper import MockDbHelper as DbHelper
if config.test:
    from models.mockdbhelper import MockDBHelper as DBHelper
else:
    from models.dbhelper import DBHelper

from models.user import User
from passwordhelper import PasswordHelper
from datetime import datetime

from forms import RegistrationForm
from forms import LoginForm
from forms import CreateTableForm

DB = DBHelper()
PH = PasswordHelper()

app = Flask(__name__)
app.secret_key = "afakewoik234llc*%$3odooserfefease12"

login_manager = LoginManager(app)

@app.route("/")
def home():
    # registrationForm = RegistrationForm()
    # return render_template("home.html", registrationform=registrationForm)
    return render_template("home.html", loginform=LoginForm(), registrationform=RegistrationForm())


@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/register", methods=["POST"])
def register():
    form = RegistrationForm(request.form)
    if form.validate():
        if DB.get_user(form.email.data):
            form.email.errors.append("Email address already registered")
            return render_template("home.html", loginform=LoginForm(), registrationform=form)
        salt = PH.get_salt()
        hashed = PH._get_hash(form.password2.data + salt)
        DB.add_user(form.email.data, salt, hashed)
        return render_template("home.html", loginform=LoginForm(), registrationform=form, onloadmessage="Registration successful. Please log in.")
    return render_template("home.html", loginform=LoginForm(), registrationform=form)


@app.route("/dashboard")
@login_required
def dashboard():
    now = datetime.now()
    requests = DB.get_requests(current_user.get_id())
    for req in requests:
        deltaseconds = (now- req['time']).seconds
        req['wait_minutes'] = "{}.{}".format((deltaseconds/60), str(deltaseconds % 60).zfill(2))
        

    return render_template("dashboard.html", requests=requests)

@app.route("/account")
@login_required
def account():
    tables = DB.get_tables(current_user.get_id())
    return render_template("account.html", createtableform=CreateTableForm(), tables=tables)

@app.route("/login", methods=["POST"])
def login():
    form = LoginForm(request.form)
    if form.validate():
        stored_user = DB.get_user(form.loginemail.data)
        if stored_user and PH.validate_password(form.loginpassword.data, stored_user['salt'], stored_user['hashed']):
            user = User(form.loginemail.data)
            login_user(user, remember=True)
            return redirect(url_for('account'))
        form.loginemail.errors.append("Email or password invalid")
    return render_template("home.html", loginform=form, registrationform=RegistrationForm())


@app.route("/account/createtable", methods=["POST"])
@login_required
def account_createtable():
  form = CreateTableForm(request.form)
  if form.validate():
    tableid = DB.add_table(form.tablenumber.data, current_user.get_id())
    new_url = config.base_url + "newrequest/" + str(tableid)
    DB.update_table(tableid, new_url)
    return redirect(url_for('account'))

  return render_template("account.html", createtableform=form, tables=DB.get_tables(current_user.get_id()))

@app.route("/account/deletetable")
@login_required
def account_deletetable():
  tableid = request.args.get("tableid")
  DB.delete_table(tableid)
  return redirect(url_for('account'))

@app.route("/newrequest/<tid>")
def new_request(tid):
    DB.add_request(tid, datetime.now())
    return "Your request has been logged and waiter will be withyou shortly"

@app.route("/dashboard/resolve")
@login_required
def dashboard_resolve():
  request_id = request.args.get("request_id")
  DB.delete_request(request_id)
  return redirect(url_for('dashboard'))


if __name__=="__main__":
    app.run()