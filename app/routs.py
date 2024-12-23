from app import app, bcrypt
from flask import flash, render_template, redirect, url_for, jsonify, abort, request
import requests
from flask_login import login_required, login_user, logout_user, current_user
from app.forms import LoginForm
from app.db_classes import User
from app.utils import reset_reload_file_in_60s
import os
from werkzeug.utils import secure_filename
import threading

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html")

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
    api_route = f"/api/query/program_items/floor/{floor}?day={app.config["CURRENT_DAY"]}"
    if floor == 3:
        api_route = f"/api/get_kavarna_cajovna_items" # ve tretim patre je kavarna a cajovna ne filmy, ale stejne chci response serveru ulozit do latest_responses proto takhle

    try:
        response = requests.get(app.config["DB_SERVER"]+api_route)
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

    files = os.listdir(f"app/static/slideshow/{app.config["CURRENT_DAY"]}")
    files.sort()

    if floor == 3:
        kavarna_cajovna_items = response.json()
        return render_template("kavarna_cajovna_floor.html", floor=floor, day=app.config["CURRENT_DAY"], slideshow=files,
                                kavarna_items=kavarna_cajovna_items["kavarna"], cajovna_items=kavarna_cajovna_items["cajovna"])

    program = response.json()
    rooms = set()
    for item in program:
        rooms.add(item["room"])
    rooms = list(rooms)

    return render_template("floor.html", floor=floor, day=app.config["CURRENT_DAY"], program=program, rooms=rooms, slideshow=files)

@app.route('/change_current_day', methods=["POST", "GET"])
@login_required
def change_current_day():
    if request.method == "POST":
        if not "day" in request.form:
            abort(403)
        day = request.form["day"]
        
        app.config["CURRENT_DAY"] = day
        flash(f"Changed current day to {day}")
        return redirect(url_for('index'))
    return render_template("change_current_day.html")

@app.route('/edit_slideshow/day/<dayn>')
@login_required
def edit_slideshow_day(dayn):
    if not dayn.isdigit(): abort(404)
    dayn = int(dayn)
    if dayn not in [1,2,3]: abort(404)

    files = os.listdir(f"app/static/slideshow/{dayn}")
    return render_template("edit_slideshow_day.html", dayn=dayn, files=files)

@app.post('/edit_slideshow/day/<dayn>')
@login_required
def add_slides(dayn):
    if not dayn.isdigit(): abort(404)
    dayn = int(dayn)
    if dayn not in [1,2,3]: abort(404)

    if not request.files:
        flash("No files received")
        return redirect(url_for("edit_slideshow_day", dayn=dayn))

    for file in request.files.getlist("files"):
        fn = secure_filename(file.filename)

        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        if not fn.lower().endswith(".jpg"):
            flash(f"File {fn} není .jpg soubor - doporučuju používat jenom to")
        if file_size > 20 * 1024 * 1024:
            flash(f"File {fn} je moc velká - maximum 20MB - ignoring")
            continue
        if file_size < .5 * 1024 * 1024:
            flash(f"File {fn} má nízkou kvalitu - doporučuju používat vyšší")

        flash(f"File {fn} uploaded successfully")
        file.save(f"app/static/slideshow/{dayn}/{fn}")
    return redirect(url_for("edit_slideshow_day", dayn=dayn))

@app.route('/edit_slideshow/delete/<dayn>/<filename>')
@login_required
def delete_slide(dayn, filename):
    if not dayn.isdigit(): abort(404)
    dayn = int(dayn)
    if dayn not in [1,2,3]: abort(404)

    os.remove(f"app/static/slideshow/{dayn}/{filename}")
    return redirect(url_for("edit_slideshow_day", dayn=dayn))

@app.route('/should-i-reload')
def should_i_reload():
    if not "reload.txt" in os.listdir("instance"):
        with open("instance/reload.txt", "w") as f:
            f.write("0")
    return open("instance/reload.txt", "r").read()

@app.route('/reload')
@login_required
def reload():
    if should_i_reload() == "1":
        flash("Obrazovky jsou právě v procesu reloadování - prosím počkejte minutu")
        return redirect(url_for('index'))
    with open("instance/reload.txt", "w") as f:
        f.write("1")
    thread = threading.Thread(target=reset_reload_file_in_60s)
    thread.start()
    flash("Obrazovky se reloadují do 1 minuty. Prosím počkejte alespoň minutu před dalším pokusem o reload, jinak nebude registrován.")
    return redirect(url_for('index'))

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