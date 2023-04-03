from flask import Blueprint, render_template, request, redirect, sessions
import hashlib
from models.models import *
from models.database import get_session

pages = Blueprint("pages", __name__, template_folder="templates")


@pages.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    login = request.form["login"]
    password = request.form["pass"]
    passw = hashlib.md5(password.encode())
    rendered_pass = passw.hexdigest()
    role = request.form["role"]
    if role == "sheffofprojects":
        db_session = get_session()
        data_workers = (
            db_session.query(Sheffofprojects).filter(Sheffofprojects.Login == login).first()
        )
        print(data_workers.positionsName.positionsName)
        if data_workers.Login == login and data_workers.Pass == rendered_pass and data_workers.positionsName.positionsName == "Администратор":
            return redirect("/admin/reg_shefforg")
        else:
            return render_template("index.html", title='Неверный логин и/или пароль!!!')


@pages.route("/admin/reg_shefforg", methods=["GET", "POST"])
def reg_shefforg():
    if request.method == "GET":
        return render_template("registration.html")
