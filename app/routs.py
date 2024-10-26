from app import app
from flask import flash, render_template, redirect, url_for, jsonify, abort, request
import requests
from app.utils import hash_sha256

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
def change_current_day():
    if request.method == "POST":
        if not "token" in request.form or not "day" in request.form:
            abort(403)
        token = request.form["token"]
        day = request.form["day"]
        
        token_hash = hash_sha256(token)
        if token_hash != app.config["ADMIN_TOKEN_HASH"]:
            return "Bad token"
        
        app.config["CURRENT_DAY"] = day
        return f"Changed current day to {day}"
    return render_template("change_current_day.html")
