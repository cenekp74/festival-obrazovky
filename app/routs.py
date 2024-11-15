from app import app, bcrypt
from flask import flash, render_template, redirect, url_for, jsonify, abort, request
import requests
from app.utils import hash_sha256
from flask_login import login_required, login_user, logout_user, current_user
from app.forms import LoginForm
from app.db_classes import User


latest_responses = { # posledni odpovedi main serveru ve formatu {patro: {den: odpoved}}
    0: {},
    1: {},
    2: {},
    3: {},
    4: {}
}

@app.route('/patro/<floor>')
def patro(floor):
    if not floor.isdigit(): abort(400)
    floor = int(floor)
    if not floor in [0, 1, 2, 3, 4]: abort(400)
    try:
        response = requests.get(app.config["DB_SERVER"]+f"/api/query/program_items/floor/{floor}?day={app.config["CURRENT_DAY"]}")
    except requests.exceptions.RequestException as e:
        if app.config["CURRENT_DAY"] in latest_responses[floor]:
            response = latest_responses[floor][app.config["CURRENT_DAY"]]
        else:
            return f"Error - server ({app.config["DB_SERVER"]}) is unreachable - {e}"
    if not response.status_code == 200:
        if app.config["CURRENT_DAY"] in latest_responses[floor]:
            response = latest_responses[floor][app.config["CURRENT_DAY"]]
        else:
            return f"Error - status code {response.status_code} received from server ({app.config["DB_SERVER"]})"
    latest_responses[floor][app.config["CURRENT_DAY"]] = response
    program = response.json()
    rooms = set()
    for item in program:
        rooms.add(item["room"])
    rooms = list(rooms)
    return render_template("floor.html", floor=floor, day=app.config["CURRENT_DAY"], program=program, rooms=rooms)

@app.route('/change_current_day', methods=["POST", "GET"])
@login_required
def change_current_day():
    if request.method == "POST":
        if not "day" in request.form:
            abort(403)
        day = request.form["day"]
        
        app.config["CURRENT_DAY"] = day
        return f"Changed current day to {day}"
    return render_template("change_current_day.html")

#region login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect('/')
        flash('Přihlášení se nezdařilo - zkontrolujte username a heslo', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
#endregion login