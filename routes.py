import hashlib
from flask import Blueprint, render_template, request, redirect, session
from sqlalchemy import text
from models.models import Sheffofprojects, Organizations, Shefforganizations
from models.database import get_session, get_select

pages = Blueprint("pages", __name__, template_folder="templates")


@pages.route("/", methods=["GET", "POST"])  # главная страница
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
        if (
            data_workers.Login == login
            and data_workers.Pass == rendered_pass
            and data_workers.positionsName.positionsName == "Администратор"
        ):
            session["admin"] = [
                data_workers.IDsheffpr,
                data_workers.IDpositions,
                data_workers.sheffprFirstname,
                data_workers.sheffprName,
                data_workers.sheffprFathername,
                data_workers.positionsName.positionsName,
            ]
            return redirect("/admin/reg_shefforg")
        else:
            return render_template("index.html", title="Неверный логин и/или пароль!!!")


@pages.route("/exit", methods=["POST", "GET"])  # кнопка выхода из системы
def exit_page():
    if request.method == "POST":
        session.pop("admin", None)
        return redirect("/")


@pages.route("/admin/reg_shefforg", methods=["GET", "POST"])  # админка-регистрация рук.огранизации
def reg_shefforg():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        select_shefforg = select(Organizations, Shefforganizations).join_from(
            Shefforganizations,
            Organizations,
            Organizations.IDshefforg == Shefforganizations.IDshefforg,
            isouter=True,
        ).order_by(Shefforganizations.FullName)
        shefforg = db_sessions.execute(select_shefforg).all()
        return render_template("registration.html", shefforg=shefforg)
    if request.method == "POST":
        fio_filter = request.form["fioFilter"]
        org_filter = request.form["orgFilter"]
        where_fio_filter = (
            Shefforganizations.FullName.ilike("%" + fio_filter + "%") if fio_filter else text("1=1")
        )
        where_org_filter = (
            Organizations.orgName.ilike("%" + org_filter + "%") if org_filter else text("1=1")
        )
        select = get_select()
        db_sessions = get_session()
        select_shefforg = (
            select(Organizations, Shefforganizations)
            .join_from(
                Shefforganizations,
                Organizations,
                Organizations.IDshefforg == Shefforganizations.IDshefforg,
                isouter=True,
            )
            .where(where_fio_filter)
            .where(where_org_filter)
            .order_by(Shefforganizations.FullName)
        )
        shefforg = db_sessions.execute(select_shefforg).all()
        return render_template("resultTableRegSheffOrg.html", shefforg=shefforg)


@pages.route("/admin/add-shefforg", methods=["GET", "POST"])  # добавление рук.организации
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
            shefforgFirstname=firstname,
            shefforgName=name,
            shefforgFathername=fathername,
            shefforgPositions=pos,
            shefforgDoc=doc,
            shefforgEmail=em,
            shefforgPhone=phone,
            Login=login,
            Pass=passw,
        )
        db_sessions.add(add)
        db_sessions.commit()
        return redirect("/admin/reg_shefforg")


@pages.route("/admin/delsheforg", methods=["GET", "POST"])  # удаление рук.организации
def delshefforg():
    if request.method == "POST":
        db_sessions = get_session()
        idshefforg = int(request.form['delsheforg'])
        db_sessions.query(Shefforganizations).filter(Shefforganizations.IDshefforg == idshefforg).delete()
        db_sessions.commit()
        return redirect("/admin/reg_shefforg")


@pages.route("/admin/redshefforganiz", methods=["GET", "POST"])  # редактирование рук.организации
def redshefforg():
    if request.method == "POST":
        db_sessions = get_session()
        idshefforg = int(request.form['redshefforg'])
        firstname = request.form["redshefforgFirstname"]
        name = request.form["redshefforgName"]
        fathername = request.form["redshefforgFathername"]
        pos = request.form["redshefforgPositions"]
        doc = request.form["redshefforgDoc"]
        em = request.form["redshefforgEmail"]
        phone = request.form["redshefforgPhone"]
        login = request.form["redLogin"]
        password = request.form["redPass"]
        npr = db_sessions.query(Shefforganizations).filter(Shefforganizations.IDshefforg == idshefforg).first()
        if str(firstname) != "":
            npr.shefforgFirstname = str(firstname)
        if str(name) != "":
            npr.shefforgName = str(name)
        if str(fathername) != "":
            npr.shefforgFathername = str(fathername)
        if str(pos) != "":
            npr.shefforgPositions = str(pos)
        if str(doc) != "":
            npr.shefforgDoc = str(doc)
        if str(em) != "":
            npr.shefforgEmail = str(em)
        if str(phone) != "":
            npr.shefforgPhone = str(phone)
        if str(login) != "":
            npr.Login = str(login)
        if str(password) != "":
            password = hashlib.md5(password.encode())
            password = password.hexdigest()
            npr.Pass = str(password)
        db_sessions.commit()
        return redirect("/admin/reg_shefforg")


@pages.route("/admin/organization", methods=["GET", "POST"])  # админка-регистрация организации
def organization():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        select_shefforg = select(Organizations, Shefforganizations.IDshefforg, Shefforganizations.FullName).join_from(
            Shefforganizations,
            Organizations,
            Organizations.IDshefforg == Shefforganizations.IDshefforg,
            isouter=True,
        ).filter(Organizations.IDshefforg.is_(None)).order_by(Shefforganizations.FullName)
        shefforg = db_sessions.execute(select_shefforg).all()
        return render_template("organization.html", shefforg = shefforg)

