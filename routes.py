from flask import Blueprint, render_template, request, redirect, session
import hashlib
from models.models import *
from models.database import get_session, get_select

pages = Blueprint("pages", __name__, template_folder="templates")


@pages.route("/", methods=["GET", "POST"]) #главная страница
def index():
    if request.method == "GET":
        return render_template("index.html")
    login = request.form["login"]
    password = request.form["pass"]
    passw = hashlib.md5(password.encode())
    rendered_pass = passw.hexdigest()
    role = request.form["role"]
    if role == "sheffofprojects":
        db_sessions = get_session()
        data_workers = (
            db_sessions.query(Sheffofprojects).filter(Sheffofprojects.Login == login).first()
        )
        if data_workers.Login == login and data_workers.Pass == rendered_pass and data_workers.positionsName.positionsName == "Администратор":
            session['admin'] = [data_workers.IDsheffpr, data_workers.IDpositions, data_workers.sheffprFirstname, data_workers.sheffprName, data_workers.sheffprFathername, data_workers.positionsName.positionsName]
            return redirect("/admin/reg_shefforg")
        else:
            return render_template("index.html", title='Неверный логин и/или пароль!!!')


@pages.route('/exit', methods=['POST', 'GET']) #кнопка выхода из системы
def exit_page():
    if request.method == "POST":
        session.pop('admin', None)
        return redirect('/')


@pages.route("/admin/reg_shefforg", methods=["GET", "POST"]) #админка-регистрация рук.огранизации
def reg_shefforg():
    if request.method == "GET":
        select = get_select()
        shefforg = select(Organizations.orgName, Shefforganizations).join_from(Shefforganizations, Organizations,
                                                                        Organizations.IDshefforg == Shefforganizations.IDshefforg,
                                                                        isouter=True)
        return render_template("registration.html", shefforg = shefforg)


@pages.route("/admin/add-shefforg", methods=["GET", "POST"]) #добавление рук.организации
def addshefforg():
    if request.method == "POST":
        db_sessions = get_session()
        firstname = str(request.form["shefforgFirstname"])
        name = str(request.form["shefforgName"])
        fathername = str(request.form["shefforgFathername"])
        pos = str(request.form["shefforgPositions"])
        doc = str(request.form["shefforgDoc"])
        em = str(request.form["shefforgEmail"])
        phone = str(request.form["shefforgPhone"])
        login = str(request.form["Login"])
        password = str(request.form["Pass"])
        passw = hashlib.md5(password.encode())
        passw = passw.hexdigest()
        add = Shefforganizations(
            shefforgFirstname = firstname, shefforgName = name, shefforgFathername = fathername,
            shefforgPositions = pos, shefforgDoc = doc, shefforgEmail = em, shefforgPhone = phone,
            Login = login, Pass = passw)
        db_sessions.add(add)
        db_sessions.commit()
        return redirect('/admin/reg_shefforg')
