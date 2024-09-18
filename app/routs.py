from app import app
from flask import flash, render_template, redirect, url_for, jsonify, abort, request
import requests

CURRENT_DAY = 1 # docasne

@app.route('/patro/<floor>')
def patro(floor):
    try:
        response = requests.get(app.config["DB_SERVER"]+f"/api/query/program_items/floor/{floor}?day={CURRENT_DAY}")
    except requests.exceptions.RequestException as e:
        return f"Error - server ({app.config["DB_SERVER"]}) is unreachable - {e}"
    if not response.status_code == 200:
        return f"Error - status code {response.status_code} received from server ({app.config["DB_SERVER"]})"
    return render_template("floor.html", floor=floor, day=CURRENT_DAY, program=response.json())