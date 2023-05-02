from datetime import datetime, date
from os import path, remove
import hashlib
import locale
import csv
import re
from docxtpl import DocxTemplate
from flask import Blueprint, render_template, request, redirect, session, send_file, jsonify
from sqlalchemy import text
from pymorphy2 import MorphAnalyzer
from models.models import (
    Sheffofprojects,
    Organizations,
    Shefforganizations,
    Contracts,
    Specializations,
    Formstuding,
    Groups,
    Students,
    Competensions,
    Positions,
    Initiatorsofprojects,
    Projects,
    PassportOfProjects,
    StadiaOfProjects,
    RolesOfProjects,
    SpecializationInProjects,
    CompetensionsInProject,
    StudentsInProjects,
    Applications,
)
from models.database import get_session, get_select

morph = MorphAnalyzer()
locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
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
    db_sessions = get_session()

    if role == "administrator":
        data_workers = (
            db_sessions.query(Sheffofprojects).filter(Sheffofprojects.Login == login).first()
        )
        if not (
            data_workers is not None
            and (data_workers.Login == login and data_workers.Pass == rendered_pass)
            and data_workers.positionsName.positionsName == "Администратор"
        ):
            return render_template("index.html", title="Неверный логин и/или пароль!!!")
        session["fullName"] = [
            data_workers.sheffprFirstname,
            data_workers.sheffprName,
            data_workers.sheffprFathername,
            data_workers.positionsName.positionsName,
        ]
        session["url"] = "admin"
        session["firstNav"] = "Панель администратора"
        return redirect("/admin/reg_shefforg")
    if role == "sheffofprojects":
        data_workers = (
            db_sessions.query(Sheffofprojects).filter(Sheffofprojects.Login == login).first()
        )
        if not (
            data_workers is not None
            and (data_workers.Login == login and data_workers.Pass == rendered_pass)
        ):
            return render_template("index.html", title="Неверный логин и/или пароль!!!")
        session["fullName"] = [
            data_workers.sheffprFirstname,
            data_workers.sheffprName,
            data_workers.sheffprFathername,
            data_workers.positionsName.positionsName,
        ]
        session["url"] = "sheffproj"
        session["firstNav"] = "Панель руководителя"
        session["secondNav"] = "проекта"
        session["user"] = [data_workers.IDsheffpr]
        return redirect("/sheffproj/assignment")
    if role == "shefforganizations":
        data_workers = (
            db_sessions.query(Shefforganizations).filter(Shefforganizations.Login == login).first()
        )
        if not (
            data_workers is not None
            and (data_workers.Login == login and data_workers.Pass == rendered_pass)
        ):
            return render_template("index.html", title="Неверный логин и/или пароль!!!")
        org = (
            db_sessions.query(Organizations)
            .filter(Organizations.IDshefforg == data_workers.IDshefforg)
            .first()
        )
        work = f"{data_workers.shefforgPositions} {org.orgName}"
        session["fullName"] = [
            data_workers.shefforgFirstname,
            data_workers.shefforgName,
            data_workers.shefforgFathername,
        ]
        session["url"] = "shefforg"
        session["pos"] = work
        session["firstNav"] = "Панель руководителя"
        session["secondNav"] = "организации"
        session["email"] = data_workers.shefforgEmail
        session["user"] = [org.IDorg, data_workers.IDshefforg]
        return redirect("/shefforg/reg_shefforg")
    if role == "initiatorsofprojects":
        data_workers = (
            db_sessions.query(Initiatorsofprojects)
            .filter(Initiatorsofprojects.Login == login)
            .first()
        )
        if not (
            data_workers is not None
            and (data_workers.Login == login and data_workers.Pass == rendered_pass)
        ):
            return render_template("index.html", title="Неверный логин и/или пароль!!!")
        org = (
            db_sessions.query(Organizations)
            .filter(Organizations.IDorg == data_workers.IDorg)
            .first()
        )
        work = f"{data_workers.initprPositions} {org.orgName}"
        session["fullName"] = [
            data_workers.initprFirstname,
            data_workers.initprName,
            data_workers.initprFathername,
        ]
        session["url"] = "iniciators"
        session["pos"] = work
        session["firstNav"] = "Панель инициатора"
        session["secondNav"] = "проекта"
        session["email"] = data_workers.initprEmail
        session["user"] = [org.IDorg, data_workers.IDinitpr]
        return redirect("/iniciators/projects")
    if role == "students":
        data_workers = db_sessions.query(Students).filter(Students.Login == login).first()
        if not (
            data_workers is not None
            and (data_workers.Login == login and data_workers.Pass == rendered_pass)
        ):
            return render_template("index.html", title="Неверный логин и/или пароль!!!")
        group = db_sessions.query(Groups).filter(Groups.IDgroups == data_workers.IDgroups).first()
        session["fullName"] = [
            data_workers.studentsFirstname,
            data_workers.studentsName,
            data_workers.studentsFathername,
        ]
        session["url"] = "student"
        session["pos"] = group.groupsName
        session["firstNav"] = "Панель студента"
        session["email"] = data_workers.studentsEmail
        session["user"] = [group.IDgroups, data_workers.IDstudents]
        return redirect("/student/participation_ticket")


@pages.route("/exit", methods=["POST", "GET"])  # кнопка выхода из системы
def exit_page():
    if request.method == "POST":
        session.clear()
        return redirect("/")


@pages.route("/admin/reg_shefforg", methods=["GET", "POST"])  # админка-регистрация рук.огранизации
def reg_shefforg():
    if request.method == "GET":
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
            .order_by(Shefforganizations.FullName)
        )
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
        idshefforg = int(request.form["delsheforg"])
        db_sessions.query(Shefforganizations).filter(
            Shefforganizations.IDshefforg == idshefforg
        ).delete()
        db_sessions.commit()
        return redirect("/admin/reg_shefforg")


@pages.route("/admin/redshefforganiz", methods=["GET", "POST"])  # редактирование рук.организации
def redshefforg():
    if request.method == "POST":
        db_sessions = get_session()
        idshefforg = int(request.form["redshefforg"])
        firstname = request.form["redshefforgFirstname"]
        name = request.form["redshefforgName"]
        fathername = request.form["redshefforgFathername"]
        pos = request.form["redshefforgPositions"]
        doc = request.form["redshefforgDoc"]
        em = request.form["redshefforgEmail"]
        phone = request.form["redshefforgPhone"]
        login = request.form["redLogin"]
        password = request.form["redPass"]
        npr = (
            db_sessions.query(Shefforganizations)
            .filter(Shefforganizations.IDshefforg == idshefforg)
            .first()
        )
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
        select_org = select(Organizations).order_by(Organizations.orgName)
        select_orgsheff = (
            select(
                Organizations,
                Shefforganizations,
            )
            .join_from(
                Shefforganizations,
                Organizations,
                Organizations.IDshefforg == Shefforganizations.IDshefforg,
            )
            .order_by(Organizations.orgName)
        )
        select_shefforg = (
            select(
                Organizations,
                Shefforganizations.IDshefforg,
                Shefforganizations.FullName,
            )
            .join_from(
                Shefforganizations,
                Organizations,
                Organizations.IDshefforg == Shefforganizations.IDshefforg,
                isouter=True,
            )
            .filter(Organizations.IDshefforg.is_(None))
            .order_by(Shefforganizations.FullName)
        )
        shefforg = db_sessions.execute(select_shefforg).all()
        organizations = db_sessions.execute(select_org).all()
        orgsheff = db_sessions.execute(select_orgsheff).all()
        return render_template(
            "organization.html", shefforg=shefforg, organizations=organizations, orgsheff=orgsheff
        )
    if request.method == "POST":
        fio_filters = request.form["fioFilters"]
        org_filters = request.form["orgFilters"]
        yuradress_filters = request.form["yuradressFilters"]
        where_fio_filters = (
            Shefforganizations.FullName.ilike("%" + fio_filters + "%")
            if fio_filters
            else text("1=1")
        )
        where_org_filters = (
            Organizations.orgName.ilike("%" + org_filters + "%") if org_filters else text("1=1")
        )
        where_yuradress_filters = (
            Organizations.orgYuraddress.ilike("%" + yuradress_filters + "%")
            if yuradress_filters
            else text("1=1")
        )
        select = get_select()
        db_sessions = get_session()
        select_orgsheff = (
            select(
                Organizations,
                Shefforganizations,
            )
            .join_from(
                Shefforganizations,
                Organizations,
                Organizations.IDshefforg == Shefforganizations.IDshefforg,
            )
            .where(where_fio_filters)
            .where(where_org_filters)
            .where(where_yuradress_filters)
            .order_by(Organizations.orgName)
        )
        select_org = select(Organizations).order_by(Organizations.orgName)
        select_shefforg = (
            select(
                Organizations,
                Shefforganizations.IDshefforg,
                Shefforganizations.FullName,
            )
            .join_from(
                Shefforganizations,
                Organizations,
                Organizations.IDshefforg == Shefforganizations.IDshefforg,
                isouter=True,
            )
            .filter(Organizations.IDshefforg.is_(None))
            .order_by(Shefforganizations.FullName)
        )
        shefforg = db_sessions.execute(select_shefforg).all()
        organizations = db_sessions.execute(select_org).all()
        orgsheff = db_sessions.execute(select_orgsheff).all()
        return render_template(
            "resultTableOrg.html", shefforg=shefforg, organizations=organizations, orgsheff=orgsheff
        )


@pages.route("/admin/add-org", methods=["GET", "POST"])  # добавление организации
def addorg():
    if request.method == "POST":
        db_sessions = get_session()
        idsheforg = int(request.form["addsheforg"])
        name = str(request.form["orgName"])
        yur = str(request.form["orgYuraddress"])
        adres = str(request.form["orgPostaddress"])
        em = str(request.form["orgEmail"])
        phone = str(request.form["orgPhone"])
        add = Organizations(
            IDshefforg=idsheforg,
            orgName=name,
            orgYuraddress=yur,
            orgPostaddress=adres,
            orgEmail=em,
            orgPhone=phone,
        )
        db_sessions.add(add)
        db_sessions.commit()
        return redirect("/admin/organization")


@pages.route("/admin/delorg", methods=["GET", "POST"])  # удаление организации
def delorg():
    if request.method == "POST":
        db_sessions = get_session()
        idorg = int(request.form["delorg"])
        db_sessions.query(Organizations).filter(Organizations.IDorg == idorg).delete()
        db_sessions.commit()
        return redirect("/admin/organization")


@pages.route("/admin/redorganiz", methods=["GET", "POST"])  # редактирование организации
def redorg():
    if request.method == "POST":
        db_sessions = get_session()
        idorg = int(request.form["redorg"])
        idsheforg = request.form["redsheforg"]
        name = request.form["redorgName"]
        yur = request.form["redorgYuraddress"]
        adres = request.form["redorgPostaddress"]
        em = request.form["redorgEmail"]
        phone = request.form["redorgPhone"]
        npr = db_sessions.query(Organizations).filter(Organizations.IDorg == idorg).first()
        if str(idsheforg) != "":
            npr.IDshefforg = int(idsheforg)
        if str(name) != "":
            npr.orgName = str(name)
        if str(yur) != "":
            npr.orgYuraddress = str(yur)
        if str(adres) != "":
            npr.orgPostaddress = str(adres)
        if str(em) != "":
            npr.orgEmail = str(em)
        if str(phone) != "":
            npr.orgPhone = str(phone)
        db_sessions.commit()
        return redirect("/admin/organization")


@pages.route(
    "/admin/contracts", methods=["GET", "POST"]
)  # Договоры об организации проектного обучения
def route_contracts():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        select_org = select(Organizations).order_by(Organizations.orgName)
        select_contracts = select(Contracts).order_by(
            Contracts.contractsNumber, Contracts.contractsStart
        )
        select_contracts_order = (
            select(Contracts)
            .join(Organizations)
            .order_by(Organizations.orgName, Contracts.contractsNumber, Contracts.contractsStart)
        )
        contracts = db_sessions.execute(select_contracts).all()
        organizations = db_sessions.execute(select_org).all()
        contracts_order = db_sessions.execute(select_contracts_order).all()

        return render_template(
            "contracts.html",
            contracts=contracts,
            organizations=organizations,
            contracts_order=contracts_order,
        )
    if request.method == "POST":
        date_filters = request.form.get("dateContractFilter")
        org_filters = request.form.get("orgFilters")
        number_filters = request.form.get("numberContractFilter")
        where_org_filters = (
            Organizations.orgName.ilike("%" + org_filters + "%") if org_filters else text("1=1")
        )
        where_date_filters = (
            Contracts.contractsStart.ilike(date_filters) if date_filters else text("1=1")
        )
        where_number_filters = (
            Contracts.contractsNumber.ilike("%" + number_filters + "%")
            if number_filters
            else text("1=1")
        )
        select = get_select()
        db_sessions = get_session()
        select_contracts = (
            select(Contracts)
            .join(Organizations)
            .where(where_number_filters)
            .where(where_date_filters)
            .where(where_org_filters)
            .order_by(Contracts.contractsNumber, Contracts.contractsStart)
        )
        contracts = db_sessions.execute(select_contracts).all()
        return render_template("resultTableContracts.html", contracts=contracts)


@pages.route("/admin/addContract", methods=["POST"])  # добавление договора
def add_contract():
    if request.method == "POST":
        db_sessions = get_session()
        id_org = int(request.form["addorg"])
        contract_number = int(request.form["contractNumber"])
        contract_start_date = datetime.strptime(request.form["contractStart"], "%Y-%m-%d").date()
        contract_end_date = datetime.strptime(request.form["contractEnd"], "%Y-%m-%d").date()
        add = Contracts(
            IDorg=id_org,
            contractsNumber=contract_number,
            contractsStart=contract_start_date,
            contractsFinish=contract_end_date,
            contractsPattern="test",
            contractsFull="full",
        )
        db_sessions.add(add)
        db_sessions.commit()
        return redirect("/admin/contracts")


@pages.route("/admin/delContract", methods=["POST"])  # удаление договора
def del_contract():
    if request.method == "POST":
        db_sessions = get_session()
        id_contract = int(request.form["delContract"])
        db_sessions.query(Contracts).filter(Contracts.IDcontracts == id_contract).delete()
        db_sessions.commit()
        return redirect("/admin/contracts")


@pages.route("/admin/modifyContract", methods=["POST"])  # редактирование договора
def modify_contract():
    if request.method == "POST":
        db_sessions = get_session()
        id_contract = int(request.form["modifyContract"])
        id_org = request.form["addorg"]
        contract_number = request.form["contractNumber"]
        contract_start_date = request.form["contractStart"]
        contract_end_date = request.form["contractEnd"]
        npr = db_sessions.query(Contracts).filter(Contracts.IDcontracts == id_contract).first()
        if str(id_org) != "":
            npr.IDorg = int(id_org)
        if str(contract_number) != "":
            npr.contractsNumber = int(contract_number)
        if str(contract_start_date) != "":
            npr.contractsStart = str(contract_start_date)
        if str(contract_end_date) != "":
            npr.contractsFinish = str(contract_end_date)
        db_sessions.commit()
        return redirect("/admin/contracts")


# получение договора
@pages.route("/getContract", methods=["GET"])
def create_and_send_document():
    args = request.args
    id_contract = args.get("idContract")

    db_sessions = get_session()
    select = text(
        """SELECT p.contractsNumber, o.orgName, p.contractsFinish, o.orgYuraddress, o.orgPostaddress, p.contractsStart, s.shefforgDoc, s.shefforgFirstname as firstName, s.shefforgName as name, s.shefforgFathername as surname, s.shefforgPositions
        FROM projectsudycontracts p
            inner join organizations o on ( o.IDorg = p.IDorg )
            inner join shefforganizations s on ( s.IDshefforg = o.IDshefforg)
        WHERE
            p.IDcontracts = :id_contract
        """
    )

    contract = db_sessions.execute(select, {"id_contract": id_contract}).first()

    if not contract:
        return

    context = {}
    context["contract_number"] = contract[0]
    context["org_name"] = contract[1]
    context["contract_end_date"] = get_date(contract[2].strftime("%d.%m.%Y"))
    context["org_ur_address"] = contract[3]
    context["org_postal_address"] = contract[4]
    context["contract_start_date"] = get_date(contract[5].strftime("%d.%m.%Y")) + " г."
    document = (
        [
            value
            for value in morph.parse(contract[6])
            if value.tag.number == "sing" and value.tag.POS == "NOUN"
        ][0]
        .inflect({"gent"})
        .word
    )
    first_name = (
        [
            value
            for value in morph.parse(contract[7])
            if value.tag.number == "sing" and value.tag.POS == "NOUN"
        ][0]
        .inflect({"gent"})
        .word
    )
    name = (
        [
            value
            for value in morph.parse(contract[8])
            if value.tag.number == "sing" and value.tag.POS == "NOUN"
        ][0]
        .inflect({"gent"})
        .word
    )
    sur_name = (
        [
            value
            for value in morph.parse(contract[9])
            if value.tag.number == "sing" and value.tag.POS == "NOUN"
        ][0]
        .inflect({"gent"})
        .word
    )
    position = (
        [
            value
            for value in morph.parse(contract[10])
            if value.tag.number == "sing" and value.tag.POS == "NOUN"
        ][0]
        .inflect({"gent"})
        .word
    )
    context["document"] = document
    context["fio"] = contract[7] + " " + contract[8][0] + ". " + contract[9][0] + "."
    context["position"] = contract[10].capitalize()
    context["position_and_fio"] = (
        position
        + " "
        + first_name.capitalize()
        + " "
        + name.capitalize()
        + " "
        + sur_name.capitalize()
    )
    filename = (
        "Договор "
        + str(contract.contractsNumber)
        + "_"
        + date.today().strftime("%d_%B_%Y")
        + ".doc"
    )
    file_path = path.join("documents", filename)
    doc = DocxTemplate("./documents/contract_template.docx")

    doc.render(context)

    doc.save(file_path)

    return send_file(file_path, mimetype="multipart/form-data", as_attachment=True)


def get_date(date):
    month_list = [
        "Января",
        "Февраля",
        "Марта",
        "Апреля",
        "Мая",
        "Июня",
        "Июля",
        "Августа",
        "Сентября",
        "Октября",
        "Ноября",
        "Декабря",
    ]
    date_list = date.split(".")
    return "«" + date_list[0] + "» " + month_list[int(date_list[1]) - 1] + " " + date_list[2]


# получить подписанный договор
@pages.route("/getContractSigned", methods=["GET"])
def get_document():
    args = request.args
    id_contract = args.get("idContract")

    db_sessions = get_session()
    contract = db_sessions.query(Contracts).filter(Contracts.IDcontracts == id_contract).first()

    if not contract.contractsSigned:
        return "", 404

    return send_file(contract.contractsSigned, mimetype="multipart/form-data", as_attachment=True)


# загрузить подписанный договор
@pages.route("/uploadContractSigned", methods=["POST"])
def upload_document():
    upload_file = request.files.get("file")
    id_contract = request.form.get("contract_id")
    if not upload_file or not id_contract:
        return

    file_path = path.join("documents", upload_file.filename)

    db_sessions = get_session()
    contract = db_sessions.query(Contracts).filter(Contracts.IDcontracts == id_contract).first()
    contract.contractsSigned = file_path
    db_sessions.commit()

    upload_file.save(file_path)

    return redirect("/admin/contracts", code=307)


# удалить подписанный договор
@pages.route("/deleteContractSigned", methods=["POST"])
def delete_document():
    id_contract = request.form.get("idContract")
    if not id_contract:
        return

    db_sessions = get_session()
    contract = db_sessions.query(Contracts).filter(Contracts.IDcontracts == id_contract).first()
    contract.contractsSigned = None
    db_sessions.commit()
    return redirect("/admin/contracts", code=307)


@pages.route("/admin/specializations", methods=["GET", "POST"])  # Специализации
def specializations():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        select_spec = select(Specializations).order_by(
            Specializations.specShifr,
            Specializations.specNapravlenie,
            Specializations.specNapravlennost,
        )
        specializations = db_sessions.execute(select_spec).all()
        return render_template("specializations.html", specializations=specializations)
    if request.method == "POST":
        shifr_filters = request.form.get("shifrFilters")
        napr_filters = request.form.get("naprFilters")
        where_shifr_filters = (
            Specializations.specShifr.ilike("%" + shifr_filters + "%")
            if shifr_filters
            else text("1=1")
        )
        where_napr_filters = (
            Specializations.specNapravlenie.ilike("%" + napr_filters + "%")
            if napr_filters
            else text("1=1")
        )
        select = get_select()
        db_sessions = get_session()
        select_spec = (
            select(Specializations)
            .where(where_shifr_filters)
            .where(where_napr_filters)
            .order_by(
                Specializations.specShifr,
                Specializations.specNapravlenie,
                Specializations.specNapravlennost,
            )
        )
        specializations = db_sessions.execute(select_spec).all()
        return render_template("resultTableSpecializations.html", specializations=specializations)


@pages.route("/admin/addSpecialization", methods=["POST"])  # добавление специализации
def add_spec():
    if request.method == "POST":
        db_sessions = get_session()
        shifr = str(request.form["specShifr"])
        napravlenie = str(request.form["specNapravlenie"])
        napravlennost = str(request.form["specNapravlennost"])
        add = Specializations(
            specShifr=shifr,
            specNapravlenie=napravlenie,
            specNapravlennost=napravlennost,
        )
        db_sessions.add(add)
        db_sessions.commit()
        return redirect("/admin/specializations")


@pages.route("/admin/delSpecialization", methods=["POST"])  # удаление специализации
def del_spec():
    db_sessions = get_session()
    id_spec = int(request.form["delSpecialization"])
    db_sessions.query(Specializations).filter(Specializations.IDspec == id_spec).delete()
    db_sessions.commit()
    return redirect("/admin/specializations")


@pages.route("/admin/modifySpecialization", methods=["POST"])  # редактирование специализации
def modify_spec():
    if request.method == "POST":
        db_sessions = get_session()
        id_spec = int(request.form["modifySpecialization"])
        shifr = request.form["redspecShifr"]
        napr = request.form["redspecNapravlenie"]
        napravlennost = request.form["redspecNapravlennost"]
        npr = db_sessions.query(Specializations).filter(Specializations.IDspec == id_spec).first()
        if str(shifr) != "":
            npr.specShifr = str(shifr)
        if str(napr) != "":
            npr.specNapravlenie = str(napr)
        if str(napravlennost) != "":
            npr.specNapravlennost = str(napravlennost)
        db_sessions.commit()
        return redirect("/admin/specializations")


@pages.route("/admin/groups", methods=["GET", "POST"])  # Группы
def groups():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        select_tablegr = (
            select(Groups, Formstuding.form_stName, Specializations.FullSpec)
            .join(Formstuding)
            .join(Specializations)
            .order_by(
                Specializations.FullSpec,
                Groups.groupsName,
                Groups.groupsYear,
                Formstuding.form_stName,
            )
        )
        select_formst = select(Formstuding).order_by(Formstuding.form_stName)
        select_groups = select(Groups).order_by(Groups.groupsName)
        select_spec = select(Specializations).order_by(
            Specializations.specShifr,
            Specializations.specNapravlenie,
            Specializations.specNapravlennost,
        )
        formst = db_sessions.execute(select_formst).all()
        specializations = db_sessions.execute(select_spec).all()
        groups = db_sessions.execute(select_groups).all()
        groups_table = db_sessions.execute(select_tablegr).all()
        return render_template(
            "groups.html",
            formst=formst,
            specializations=specializations,
            groups=groups,
            groups_table=groups_table,
        )

    if request.method == "POST":
        form_education = request.form.get("formEducation")
        direct_study = request.form.get("directStudy")
        year_study = request.form.get("yearStudy")
        where_form_education = (
            Formstuding.form_stName.ilike("%" + form_education + "%")
            if form_education
            else text("1=1")
        )
        where_direct_study = (
            Specializations.specNapravlenie.ilike("%" + direct_study + "%")
            if direct_study
            else text("1=1")
        )
        where_year_study = (
            Groups.groupsYear.ilike("%" + year_study + "%") if year_study else text("1=1")
        )
        select = get_select()
        db_sessions = get_session()
        select_group = (
            select(Groups, Formstuding.form_stName, Specializations.FullSpec)
            .join(Formstuding)
            .join(Specializations)
            .where(where_form_education)
            .where(where_direct_study)
            .where(where_year_study)
            .order_by(
                Specializations.FullSpec,
                Groups.groupsName,
                Groups.groupsYear,
                Formstuding.form_stName,
            )
        )
        groups_table = db_sessions.execute(select_group).all()
        return render_template("resultTableGroups.html", groups_table=groups_table)


@pages.route("/admin/addGroup", methods=["POST"])  # Добавить группы
def addgroups():
    db_sessions = get_session()
    grname = str(request.form["groupsName"])
    gryear = int(request.form["groupsYear"])
    formst = int(request.form["form_st"])
    spec = int(request.form["spec"])
    add = Groups(
        groupsName=grname,
        groupsYear=gryear,
        IDform_st=formst,
        IDspec=spec,
    )
    db_sessions.add(add)
    db_sessions.commit()
    return redirect("/admin/groups")


@pages.route("/admin/delGroup", methods=["POST"])  # Удалить группы
def delgroups():
    db_sessions = get_session()
    id_gr = int(request.form["delGroup"])
    db_sessions.query(Groups).filter(Groups.IDgroups == id_gr).delete()
    db_sessions.commit()
    return redirect("/admin/groups")


@pages.route("/admin/modifyGroup", methods=["POST"])  # Редактировать группы
def redgroups():
    db_sessions = get_session()
    id_gr = int(request.form["modifyGroups"])
    grname = request.form["redgroupsName"]
    gryear = request.form["redgroupsYear"]
    formst = request.form["redform_st"]
    spec = request.form["redspec"]
    npr = db_sessions.query(Groups).filter(Groups.IDgroups == id_gr).first()
    if str(grname) != "":
        npr.groupsName = str(grname)
    if str(gryear) != "":
        npr.groupsYear = int(gryear)
    if str(formst) != "":
        npr.IDform_st = int(formst)
    if str(spec) != "":
        npr.IDspec = int(spec)
    db_sessions.commit()
    return redirect("/admin/groups")


# Загрузка csv в специализации
@pages.route("/admin/csvSpec", methods=["POST"])
def insert_csv_spec():
    try:
        upload_file = request.files.get("file")
        file_path = path.join("documents", upload_file.filename)
        upload_file.save(file_path)
        with open(file_path, encoding="utf-8") as file:
            db_sessions = get_session()
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                pattern = re.match(r"^[0-9]{2}\.[0-9]{2}\.[0-9]{2}$", row["Шифр"])
                if not pattern:
                    return "Ошибка при валидации шифра " + row["Шифр"], 400
                add = Specializations(
                    specShifr=row["Шифр"],
                    specNapravlenie=row["Направление"],
                    specNapravlennost=row["Направленность"],
                )
                db_sessions.add(add)
                db_sessions.commit()
        return "", 200
    finally:
        remove(file_path)


# Загрузка csv в группы
@pages.route("/admin/csvGroup", methods=["POST"])
def insert_csv_group():
    try:
        upload_file = request.files.get("file")
        file_path = path.join("documents", upload_file.filename)
        upload_file.save(file_path)
        with open(file_path, encoding="utf-8") as file:
            db_sessions = get_session()
            select = get_select()
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                napr = row["Направление"].split("-")
                idform_st = db_sessions.execute(
                    select(Formstuding.IDform_st).where(
                        Formstuding.form_stName == row["Форма обучения"]
                    )
                ).first()
                idspec = db_sessions.execute(
                    select(Specializations.IDspec)
                    .where(Specializations.specShifr == napr[0])
                    .where(Specializations.specNapravlenie == napr[1])
                    .where(Specializations.specNapravlennost == napr[2])
                ).first()
                add = Groups(
                    groupsName=row["Название группы"],
                    groupsYear=row["Год набора"],
                    IDform_st=idform_st[0],
                    IDspec=idspec[0],
                )
                db_sessions.add(add)
                db_sessions.commit()
        return "", 200
    finally:
        remove(file_path)


@pages.route("/admin/students", methods=["GET", "POST"])  # Студенты
def students():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        select_groups = select(Groups).order_by(Groups.groupsName)
        groups = db_sessions.execute(select_groups).all()
        select_student = (
            select(
                Students.IDstudents,
                Students.FullName,
                Students.studentsStudbook,
                Students.studentsPhone,
                Students.studentsEmail,
                Students.Login,
                Groups.groupsName,
            )
            .join_from(
                Students,
                Groups,
                Students.IDgroups == Groups.IDgroups,
                isouter=True,
            )
            .filter(Groups.IDgroups == groups[0].Groups.IDgroups)
            .order_by(Groups.groupsName, Students.FullName)
        )
        select_modify_student = (
            select(Students.IDstudents, Students.FullName, Students.studentsStudbook)
            .join_from(
                Students,
                Groups,
                Students.IDgroups == Groups.IDgroups,
                isouter=True,
            )
            .filter(Groups.IDgroups == groups[0].Groups.IDgroups)
            .order_by(Groups.groupsName, Students.FullName)
        )
        student = db_sessions.execute(select_student).all()
        modify_student = db_sessions.execute(select_modify_student).all()
        return render_template(
            "students.html", student=student, groups=groups, modify_student=modify_student
        )
    if request.method == "POST":
        fio = request.form.get("fio")
        grname = request.form.get("grname")
        where_fio = Students.FullName.ilike("%" + fio + "%") if fio else text("1=1")
        where_grname = Groups.IDgroups == grname if grname else text("1=1")
        select = get_select()
        db_sessions = get_session()
        select_student = (
            select(
                Students.IDstudents,
                Students.FullName,
                Students.studentsStudbook,
                Students.studentsPhone,
                Students.studentsEmail,
                Students.Login,
                Groups.groupsName,
            )
            .join_from(
                Students,
                Groups,
                Students.IDgroups == Groups.IDgroups,
                isouter=True,
            )
            .where(where_fio)
            .where(where_grname)
            .order_by(Groups.groupsName, Students.FullName)
        )
        student = db_sessions.execute(select_student).all()
        return render_template("resultTableStudents.html", student=student)


@pages.route("/admin/addStudents", methods=["POST"])  # Добавить студента
def addstudents():
    if request.method == "POST":
        db_sessions = get_session()
        fname = str(request.form["studentsFirstname"])
        name = str(request.form["studentsName"])
        lname = str(request.form["studentsFathername"])
        book = int(request.form["studentsStudbook"])
        tel = str(request.form["studentsPhone"])
        em = str(request.form["studentsEmail"])
        login = str(request.form["Login"])
        password = str(request.form["Pass"])
        idgroup = int(request.form["group"])
        passw = hashlib.md5(password.encode())
        passw = passw.hexdigest()
        add = Students(
            studentsFirstname=fname,
            studentsName=name,
            studentsFathername=lname,
            IDgroups=idgroup,
            studentsStudbook=book,
            studentsPhone=tel,
            studentsEmail=em,
            Login=login,
            Pass=passw,
        )
        db_sessions.add(add)
        db_sessions.commit()
        return redirect("/admin/students")


@pages.route("/admin/delStudent", methods=["POST"])  # Удалить студента
def delstudents():
    db_sessions = get_session()
    id_st = int(request.form["delStudent"])
    db_sessions.query(Students).filter(Students.IDstudents == id_st).delete()
    db_sessions.commit()
    return redirect("/admin/students")


@pages.route("/admin/modifyStudent", methods=["POST"])  # Редактировать студента
def modifyStudent():
    db_sessions = get_session()
    id_stud = int(request.form["redStudents"])
    fname = request.form["redstudentsFirstname"]
    name = request.form["redstudentsName"]
    lname = request.form["redstudentsFathername"]
    book = request.form["redstudentsStudbook"]
    tel = request.form["redstudentsPhone"]
    em = request.form["redstudentsEmail"]
    login = request.form["redLogin"]
    password = request.form["redPass"]
    idgroup = int(request.form["newGroup"])
    npr = db_sessions.query(Students).filter(Students.IDstudents == id_stud).first()
    if str(fname) != "":
        npr.studentsFirstname = str(fname)
    if str(name) != "":
        npr.studentsName = str(name)
    if str(lname) != "":
        npr.studentsFathername = str(lname)
    if str(book) != "":
        npr.studentsStudbook = int(book)
    if str(tel) != "":
        npr.studentsPhone = str(tel)
    if str(em) != "":
        npr.studentsEmail = str(em)
    if str(login) != "":
        npr.Login = str(login)
    if str(idgroup) != "":
        npr.IDgroups = str(idgroup)
    if str(password) != "":
        password = hashlib.md5(password.encode())
        password = password.hexdigest()
        npr.Pass = str(password)
    db_sessions.commit()
    return redirect("/admin/students")


@pages.route("/admin/csvStud", methods=["POST"])
def insert_csv_stud():
    try:
        upload_file = request.files.get("file")
        file_path = path.join("documents", upload_file.filename)
        upload_file.save(file_path)
        with open(file_path, encoding="utf-8") as file:
            db_sessions = get_session()
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                password = row["Пароль"]
                password = hashlib.md5(password.encode())
                password = password.hexdigest()
                pattern_email = re.match(
                    r"^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$",
                    row["Электронная почта"],
                )
                pattern_phone = re.match(r"^\+7[0-9]{10}$", row["Телефон"])
                pattern_studbook = re.match(r"[0-9]{9}", row["№ зачетной книжки"])
                group = db_sessions.query(Groups).filter(Groups.groupsName == row["Группа"]).first()
                if not pattern_email:
                    return "Неверный формат почты (" + row["Электронная почта"] + ")", 400
                if not pattern_phone:
                    return "Неверный формат телефона (" + row["Телефон"] + ")", 400
                if not pattern_studbook:
                    return "Неверный номер зач. книжки (" + row["№ зачетной книжки"] + ")", 400
                if group is None:
                    return "Группа не найдена (" + row["Группа"] + ")", 400
                add = Students(
                    studentsFirstname=row["Фамилия"],
                    studentsName=row["Имя"],
                    studentsFathername=row["Отчество"],
                    studentsStudbook=row["№ зачетной книжки"],
                    studentsPhone=row["Телефон"],
                    studentsEmail=row["Электронная почта"],
                    IDgroups=group.IDgroups,
                    Login=row["Логин"],
                    Pass=password,
                )
                db_sessions.add(add)
                db_sessions.commit()
        return "", 200
    finally:
        remove(file_path)


@pages.route("/admin/competitions", methods=["GET", "POST"])  # Компетенции учебных планов
def get_competitions():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        select_sp = select(Specializations).order_by(
            Specializations.specShifr,
            Specializations.specNapravlenie,
            Specializations.specNapravlennost,
        )
        spec = db_sessions.execute(select_sp).all()
        idspec = None
        if spec:
            idspec = spec[0].Specializations.IDspec
        select_competitions = (
            select(Competensions, Specializations.FullSpec)
            .join(Specializations)
            .filter(Competensions.IDspec == idspec)
            .order_by(Competensions.competensionsShifr)
        )
        competitions = db_sessions.execute(select_competitions).all()
        return render_template("competitions.html", spec=spec, competitions=competitions)
    if request.method == "POST":
        spec = int(request.form["spec"])
        select = get_select()
        db_sessions = get_session()
        select_competitions = (
            select(Competensions, Specializations.FullSpec)
            .join(Specializations)
            .filter(Competensions.IDspec == spec)
            .order_by(Competensions.competensionsShifr)
        )
        competitions = db_sessions.execute(select_competitions).all()
        return render_template("resultTableCompetitions.html", competitions=competitions)


@pages.route("/admin/addCompetition", methods=["POST"])  # Добавить компетенцию учебного плана
def addcompetitions():
    db_sessions = get_session()
    id_spec = int(request.form["specialization"])
    cod = str(request.form["competensionsShifr"])
    full = str(request.form["competensionsFull"])
    add = Competensions(
        IDspec=id_spec,
        competensionsShifr=cod,
        competensionsFull=full,
    )
    db_sessions.add(add)
    db_sessions.commit()
    return redirect("/admin/competitions")


@pages.route("/admin/modifyCompetition", methods=["POST"])
def modify_competition():
    cod = str(request.form["competensionsShifr"])
    full = str(request.form["competensionsFull"])
    id_comp = int(request.form["competetion"])
    db_sessions = get_session()
    npr = db_sessions.query(Competensions).filter(Competensions.IDcompetensions == id_comp).first()
    if cod != "":
        npr.competensionsShifr = cod
    if full != "":
        npr.competensionsFull = full
    db_sessions.commit()
    return redirect("/admin/competitions")


@pages.route("/admin/deleteCompetition", methods=["POST"])
def delete_competition():
    id_comp = int(request.form["competetion"])
    db_sessions = get_session()
    db_sessions.query(Competensions).filter(Competensions.IDcompetensions == id_comp).delete()
    db_sessions.commit()
    return redirect("/admin/competitions")


@pages.route("/admin/csvComp", methods=["POST"])
def insert_csv_comp():
    try:
        upload_file = request.files.get("file")
        file_path = path.join("documents", upload_file.filename)
        upload_file.save(file_path)
        with open(file_path, encoding="utf-8") as file:
            db_sessions = get_session()
            select = get_select()
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                spec = row["Специализация"]
                code = row["Код"]
                content = row["Содержание"]
                id_spec = db_sessions.execute(
                    select(Specializations.IDspec).where(Specializations.FullSpec == spec)
                ).first()
                add = Competensions(
                    IDspec=id_spec[0], competensionsShifr=code, competensionsFull=content
                )
                db_sessions.add(add)
                db_sessions.commit()
        return "", 200
    finally:
        remove(file_path)


@pages.route("/admin/getStudentsGroup", methods=["GET"])
def get_students_group():
    args = request.args
    id_group = args.get("idGroup")
    select = get_select()
    db_sessions = get_session()
    select_students = (
        select(Students.IDstudents, Students.FullName, Students.studentsStudbook)
        .filter(Students.IDgroups == id_group)
        .order_by(Students.FullName)
    )
    students = db_sessions.execute(select_students).all()
    return jsonify([dict(row._mapping) for row in students]), 200


@pages.route("/admin/getCompetition", methods=["GET"])
def get_competition_on_spec():
    args = request.args
    id_spec = args.get("spec")
    select = get_select()
    db_sessions = get_session()
    select_competition = (
        select(Competensions.competensionsShifr, Competensions.IDcompetensions)
        .filter(Competensions.IDspec == id_spec)
        .order_by(Competensions.competensionsShifr)
    )
    competitions = db_sessions.execute(select_competition).all()
    return jsonify([dict(row._mapping) for row in competitions]), 200


@pages.route("/admin/cafedra", methods=["GET", "POST"])  # Состав кафедры ИВТ
def cafedra():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        select_caf = (
            select(Sheffofprojects, Positions)
            .join(Positions)
            .order_by(Sheffofprojects.FullName, Positions.positionsName)
        )
        select_pos = select(Positions).order_by(Positions.positionsName)
        caf = db_sessions.execute(select_caf).all()
        pos = db_sessions.execute(select_pos).all()
        return render_template("cafedra.html", caf=caf, pos=pos)
    if request.method == "POST":
        fio_filters = request.form.get("cafedraFIO")
        pos_filters = request.form.get("cafedraPos")
        where_fio_filters = (
            Sheffofprojects.FullName.ilike("%" + fio_filters + "%") if fio_filters else text("1=1")
        )
        where_pos_filters = (
            Positions.positionsName.ilike("%" + pos_filters + "%") if pos_filters else text("1=1")
        )
        select = get_select()
        db_sessions = get_session()
        select_caf = (
            select(Sheffofprojects, Positions)
            .join(Positions)
            .where(where_fio_filters)
            .where(where_pos_filters)
            .order_by(Sheffofprojects.FullName, Positions.positionsName)
        )
        select_pos = select(Positions).order_by(Positions.positionsName)
        caf = db_sessions.execute(select_caf).all()
        pos = db_sessions.execute(select_pos).all()
        return render_template("resultTableCafedra.html", caf=caf, pos=pos)


@pages.route("/admin/addCafedra", methods=["POST"])  # добавить сотрудника ИВТ
def addcafedra():
    db_sessions = get_session()
    firstname = str(request.form["sheffprFirstname"])
    name = str(request.form["sheffprName"])
    lastname = str(request.form["sheffprFathername"])
    posit = int(request.form["posName"])
    phone = str(request.form["sheffprPhone"])
    em = str(request.form["sheffprEmail"])
    login = str(request.form["Login"])
    password = str(request.form["Pass"])
    passw = hashlib.md5(password.encode())
    passw = passw.hexdigest()
    add = Sheffofprojects(
        IDpositions=posit,
        sheffprFirstname=firstname,
        sheffprName=name,
        sheffprFathername=lastname,
        sheffprPhone=phone,
        sheffprEmail=em,
        Login=login,
        Pass=passw,
    )
    db_sessions.add(add)
    db_sessions.commit()
    return redirect("/admin/cafedra")


@pages.route("/admin/delCafedra", methods=["POST"])  # удалить сотрудника ИВТ
def delcafedra():
    id_sotr = int(request.form["delsotr"])
    db_sessions = get_session()
    db_sessions.query(Sheffofprojects).filter(Sheffofprojects.IDsheffpr == id_sotr).delete()
    db_sessions.commit()
    return redirect("/admin/cafedra")


@pages.route("/admin/modifyCafedra", methods=["POST"])  # Редактировать сотрудника ИВТ
def modifyCafedra():
    db_sessions = get_session()
    id_sotr = request.form["modifysotr"]
    firstname = request.form["redsheffprFirstname"]
    name = request.form["redsheffprName"]
    lastname = request.form["redsheffprFathername"]
    posit = request.form["redposName"]
    phone = request.form["redsheffprPhone"]
    em = request.form["redsheffprEmail"]
    login = request.form["redLogin"]
    password = request.form["redPass"]
    npr = db_sessions.query(Sheffofprojects).filter(Sheffofprojects.IDsheffpr == id_sotr).first()
    positions = None
    old_name = npr.FullName
    sess_name = f"{session['fullName'][0]} {session['fullName'][1]} {session['fullName'][2]} {session['fullName'][3]}"
    if str(posit) != "":
        npr.IDpositions = int(posit)
        positions = db_sessions.query(Positions).filter(Positions.IDpositions == posit).first()
    if str(firstname) != "":
        npr.sheffprFirstname = str(firstname)
    if str(name) != "":
        npr.sheffprName = str(name)
    if str(lastname) != "":
        npr.sheffprFathername = str(lastname)
    if str(phone) != "":
        npr.sheffprPhone = str(phone)
    if str(em) != "":
        npr.sheffprEmail = str(em)
    if str(login) != "":
        npr.Login = str(login)
    if str(password) != "":
        password = hashlib.md5(password.encode())
        password = password.hexdigest()
        npr.Pass = str(password)
    if sess_name == f"{old_name} {npr.positionsName.positionsName}":
        session.pop("fullName")
        session["fullName"] = [
            firstname if firstname else npr.sheffprFirstname,
            name if name else npr.sheffprName,
            lastname if lastname else npr.sheffprFathername,
            positions.Positions.positionsName if positions else npr.positionsName.positionsName,
        ]
    db_sessions.commit()
    return redirect("/admin/cafedra")


@pages.route("/admin/csvCafedra", methods=["POST"])
def insert_csv_cafedra():
    try:
        upload_file = request.files.get("file")
        file_path = path.join("documents", upload_file.filename)
        upload_file.save(file_path)
        with open(file_path, encoding="utf-8") as file:
            db_sessions = get_session()
            select = get_select()
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                fname = row["Фамилия"]
                name = row["Имя"]
                lname = row["Отчество"]
                posit = row["Должность"]
                login = row["Логин"]
                password = row["Пароль"]
                password = hashlib.md5(password.encode())
                password = password.hexdigest()
                pattern_email = re.match(
                    r"^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$",
                    row["Электронная почта"],
                )
                pattern_phone = re.match(r"^\+7[0-9]{10}$", row["Телефон"])
                if not pattern_email:
                    return "Неверный формат почты (" + row["Электронная почта"] + ")", 400
                if not pattern_phone:
                    return "Неверный формат телефона (" + row["Телефон"] + ")", 400
                id_pos = db_sessions.execute(
                    select(Positions.IDpositions).where(Positions.positionsName == posit)
                ).first()
                if id_pos is None:
                    return "Должность не найдена (" + row["Должность"] + ")", 400
                add = Sheffofprojects(
                    IDpositions=id_pos[0],
                    sheffprFirstname=fname,
                    sheffprName=name,
                    sheffprFathername=lname,
                    sheffprPhone=row["Телефон"],
                    sheffprEmail=row["Электронная почта"],
                    Login=login,
                    Pass=password,
                )
                db_sessions.add(add)
                db_sessions.commit()
                return "", 200
    finally:
        remove(file_path)


@pages.route("/shefforg/organization", methods=["GET", "POST"])  # админка-регистрация организации
def sheff_org_organization():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        id_org = session["user"][0]
        select_orgsheff = (
            select(
                Organizations,
                Shefforganizations,
            )
            .join_from(
                Shefforganizations,
                Organizations,
                Organizations.IDshefforg == Shefforganizations.IDshefforg,
            )
            .where(Organizations.IDorg == id_org)
            .order_by(Organizations.orgName)
        )
        orgsheff = db_sessions.execute(select_orgsheff).all()
        return render_template("sheff_org_organization.html", orgsheff=orgsheff)


@pages.route("/shefforg/redorganiz", methods=["POST"])  # редактирование рук.организации
def sheff_org_redorg():
    if request.method == "POST":
        db_sessions = get_session()
        idorg = session["user"][0]
        name = request.form["redorgName"]
        yur = request.form["redorgYuraddress"]
        adres = request.form["redorgPostaddress"]
        em = request.form["redorgEmail"]
        phone = request.form["redorgPhone"]
        npr = db_sessions.query(Organizations).filter(Organizations.IDorg == idorg).first()
        if str(name) != "":
            npr.orgName = str(name)
        if str(yur) != "":
            npr.orgYuraddress = str(yur)
        if str(adres) != "":
            npr.orgPostaddress = str(adres)
        if str(em) != "":
            npr.orgEmail = str(em)
        if str(phone) != "":
            npr.orgPhone = str(phone)
        db_sessions.commit()
        return redirect("/shefforg/organization")


@pages.route("/shefforg/reg_shefforg", methods=["GET"])  # админка-регистрация рук.огранизации
def shefforg_reg_shefforg():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        idorg = session["user"][0]
        select_shefforg = (
            select(Shefforganizations)
            .join_from(
                Shefforganizations,
                Organizations,
                Organizations.IDshefforg == Shefforganizations.IDshefforg,
                isouter=True,
            )
            .filter(Organizations.IDorg == idorg)
            .order_by(Shefforganizations.FullName)
        )
        shefforg = db_sessions.execute(select_shefforg).all()
        return render_template("sheff_org_registration.html", shefforg=shefforg)


@pages.route("/shefforg/redshefforganiz", methods=["POST"])  # редактирование рук.организации
def shefforg_redshefforg():
    if request.method == "POST":
        db_sessions = get_session()
        idshefforg = session["user"][1]
        firstname = request.form["redshefforgFirstname"]
        name = request.form["redshefforgName"]
        fathername = request.form["redshefforgFathername"]
        pos = request.form["redshefforgPositions"]
        doc = request.form["redshefforgDoc"]
        em = request.form["redshefforgEmail"]
        phone = request.form["redshefforgPhone"]
        npr = (
            db_sessions.query(Shefforganizations)
            .filter(Shefforganizations.IDshefforg == idshefforg)
            .first()
        )
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
        session.pop("fullName")
        session["fullName"] = [
            firstname if firstname else npr.shefforgFirstname,
            name if name else npr.shefforgName,
            fathername if fathername else npr.shefforgFathername,
        ]
        db_sessions.commit()

        return redirect("/shefforg/reg_shefforg")


@pages.route(
    "/shefforg/contracts", methods=["GET", "POST"]
)  # Договоры об организации проектного обучения
def sheff_org_contracts():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        idorg = session["user"][0]
        select_contracts = (
            select(Contracts)
            .filter(Contracts.IDorg == idorg)
            .order_by(Contracts.contractsNumber, Contracts.contractsStart)
        )
        contracts = db_sessions.execute(select_contracts).all()

        return render_template(
            "sheff_org_contracts.html",
            contracts=contracts,
        )


@pages.route(
    "/shefforg/mailadmin", methods=["GET", "POST"]
)  # Договоры об организации проектного обучения
def sheff_org_mailadmin():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        select_admins = (
            select(Sheffofprojects)
            .filter(Sheffofprojects.IDpositions == 1)
            .order_by(Sheffofprojects.FullName)
        )
        admins = db_sessions.execute(select_admins).all()

        return render_template("sheff_org_mail_admin.html", admins=admins)


@pages.route("/shefforg/iniciators", methods=["GET", "POST"])  # Инициаторы проектов
def sheff_org_iniciators():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        idorg = session["user"][0]
        select_inicators = (
            select(Initiatorsofprojects)
            .filter(Initiatorsofprojects.IDorg == idorg)
            .order_by(Initiatorsofprojects.FullName)
        )
        inic = db_sessions.execute(select_inicators).all()
        return render_template("iniciators.html", inic=inic)
    if request.method == "POST":
        select = get_select()
        db_sessions = get_session()
        idorg = session["user"][0]
        fio_filters = request.form["fioFilter"]
        pos_filters = request.form["posFilter"]
        where_fio_filters = (
            Initiatorsofprojects.FullName.ilike("%" + fio_filters + "%")
            if fio_filters
            else text("1=1")
        )
        where_org_filters = (
            Initiatorsofprojects.initprPositions.ilike("%" + pos_filters + "%")
            if pos_filters
            else text("1=1")
        )
        select_inicators = (
            select(Initiatorsofprojects)
            .filter(Initiatorsofprojects.IDorg == idorg)
            .where(where_fio_filters)
            .where(where_org_filters)
            .order_by(Initiatorsofprojects.FullName)
        )
        inic = db_sessions.execute(select_inicators).all()
        return render_template("resultTableInic.html", inic=inic)


@pages.route("/shefforg/addIniciators", methods=["POST"])  # Добавить инициатора проектов
def sheff_org_addiniciators():
    db_sessions = get_session()
    idorg = session["user"][0]
    fname = str(request.form["initprFirstname"])
    name = str(request.form["initprName"])
    lname = str(request.form["initprFathername"])
    pos = str(request.form["initprPositions"])
    em = str(request.form["initprEmail"])
    tel = str(request.form["initprPhone"])
    login = str(request.form["Login"])
    password = str(request.form["Pass"])
    passw = hashlib.md5(password.encode())
    passw = passw.hexdigest()
    add = Initiatorsofprojects(
        IDorg=idorg,
        initprFirstname=fname,
        initprName=name,
        initprFathername=lname,
        initprPositions=pos,
        initprEmail=em,
        initprPhone=tel,
        Login=login,
        Pass=passw,
    )
    db_sessions.add(add)
    db_sessions.commit()
    return redirect("/shefforg/iniciators")


@pages.route("/shefforg/deliniciators", methods=["POST"])  # удалить инициатора проектов
def deliniciators():
    id_sotr = int(request.form["delin"])
    db_sessions = get_session()
    db_sessions.query(Initiatorsofprojects).filter(
        Initiatorsofprojects.IDinitpr == id_sotr
    ).delete()
    db_sessions.commit()
    return redirect("/shefforg/iniciators")


@pages.route("/shefforg/redinitiators", methods=["POST"])  # Редактировать инициатора проектов
def sheff_org_redinitiators():
    db_sessions = get_session()
    idin = int(request.form["redin"])
    fname = request.form["redinitprFirstname"]
    name = request.form["redinitprName"]
    lname = request.form["redinitprFathername"]
    pos = request.form["redinitprPositions"]
    em = request.form["redinitprEmail"]
    tel = request.form["redinitprPhone"]
    login = request.form["redLogin"]
    passw = request.form["password"]
    npr = (
        db_sessions.query(Initiatorsofprojects)
        .filter(Initiatorsofprojects.IDinitpr == idin)
        .first()
    )
    if str(fname) != "":
        npr.initprFirstname = str(fname)
    if str(name) != "":
        npr.initprName = str(name)
    if str(lname) != "":
        npr.initprFathername = str(lname)
    if str(pos) != "":
        npr.initprPositions = str(pos)
    if str(em) != "":
        npr.initprEmail = str(em)
    if str(tel) != "":
        npr.initprPhone = str(tel)
    if str(login) != "":
        npr.Login = str(login)
    if str(passw) != "":
        passw = hashlib.md5(passw.encode())
        passw = passw.hexdigest()
        npr.Pass = str(passw)
    db_sessions.commit()
    return redirect("/shefforg/iniciators")


@pages.route("/admin/csvInic", methods=["POST"])
def insert_csv_inic():
    try:
        upload_file = request.files.get("file")
        file_path = path.join("documents", upload_file.filename)
        upload_file.save(file_path)
        with open(file_path, encoding="utf-8") as file:
            db_sessions = get_session()
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                password = row["Пароль"]
                password = hashlib.md5(password.encode())
                password = password.hexdigest()
                pattern_email = re.match(
                    r"^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$",
                    row["Электронная почта"],
                )
                pattern_phone = re.match(r"^\+7[0-9]{10}$", row["Телефон"])
                if not pattern_email:
                    return "Неверный формат почты (" + row["Электронная почта"] + ")", 400
                if not pattern_phone:
                    return "Неверный формат телефона (" + row["Телефон"] + ")", 400
                add = Initiatorsofprojects(
                    initprFirstname=row["Фамилия"],
                    initprName=row["Имя"],
                    initprFathername=row["Отчество"],
                    IDorg=session["user"][0],
                    initprPositions=row["Должность"],
                    initprPhone=row["Телефон"],
                    initprEmail=row["Электронная почта"],
                    Login=row["Логин"],
                    Pass=password,
                )
                db_sessions.add(add)
                db_sessions.commit()
        return "", 200
    finally:
        remove(file_path)


# Проекты
@pages.route("/iniciators/projects", methods=["GET", "POST"])
def iniciators_project():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        idinitpr = session["user"][1]
        select_stadia = select(StadiaOfProjects).order_by(StadiaOfProjects.IDstadiaofpr)
        select_projects = (
            select(Projects, PassportOfProjects, StadiaOfProjects)
            .join(PassportOfProjects)
            .join(StadiaOfProjects)
            .filter(PassportOfProjects.IDinitpr == idinitpr)
            .order_by(PassportOfProjects.passportName)
        )
        stadia = db_sessions.execute(select_stadia).all()
        projects = db_sessions.execute(select_projects).all()
        return render_template("iniciators_projects.html", projects=projects, stadia=stadia)
    if request.method == "POST":
        select = get_select()
        db_sessions = get_session()
        idinitpr = session["user"][1]
        project_filter = request.form["projectFilter"]
        stadia_filter = request.form["stadiaFilter"]
        where_project_filter = (
            PassportOfProjects.passportName.ilike("%" + project_filter + "%")
            if project_filter
            else text("1=1")
        )
        where_stadia_filter = (
            StadiaOfProjects.IDstadiaofpr == stadia_filter if stadia_filter else text("1=1")
        )
        select_projects = (
            select(Projects, PassportOfProjects, StadiaOfProjects)
            .join(PassportOfProjects)
            .join(StadiaOfProjects)
            .where(where_project_filter)
            .where(where_stadia_filter)
            .filter(PassportOfProjects.IDinitpr == idinitpr)
            .order_by(PassportOfProjects.passportName)
        )
        projects = db_sessions.execute(select_projects).all()
        return render_template("resultAccordionProjects.html", projects=projects)


@pages.route("/iniciators/addProject", methods=["POST"])
def iniciators_add_project():
    db_sessions = get_session()
    idinitpr = session["user"][1]
    project_name = str(request.form["projectName"])
    problem = str(request.form["problem"])
    purpose = str(request.form["purpose"])
    tasks = str(request.form["tasks"])
    result = str(request.form["result"])

    add_passport = PassportOfProjects(
        IDinitpr=idinitpr,
        passportName=project_name,
        passportProblem=problem,
        passportPurpose=purpose,
        passportTasks=tasks,
        passportResults=result,
        passportPattern="",
        passportFull="",
        passportSigned="",
    )
    db_sessions.add(add_passport)
    db_sessions.flush()
    idpassport = add_passport.IDpassport

    add_project = Projects(IDpassport=idpassport, IDstadiaofpr=1)
    db_sessions.add(add_project)
    db_sessions.commit()
    return redirect("/iniciators/projects")


@pages.route("/iniciators/modifyProject", methods=["POST"])
def iniciators_modify_project():
    db_sessions = get_session()
    idprojects = request.form["modifyProject"]
    project_name = request.form["projectName"]
    problem = request.form["problem"]
    purpose = request.form["purpose"]
    tasks = request.form["tasks"]
    result = request.form["result"]
    project = db_sessions.query(Projects).filter(Projects.IDprojects == idprojects).first()
    npr = (
        db_sessions.query(PassportOfProjects)
        .filter(PassportOfProjects.IDpassport == project.IDpassport)
        .first()
    )

    if str(project_name) != "":
        npr.passportName = str(project_name)
    if str(problem) != "":
        npr.passportProblem = str(problem)
    if str(purpose) != "":
        npr.passportPurpose = str(purpose)
    if str(tasks) != "":
        npr.passportTasks = str(tasks)
    if str(result) != "":
        npr.passportResults = str(result)

    db_sessions.commit()
    return redirect("/iniciators/projects")


@pages.route("/admin/projects", methods=["GET", "POST"])
def admin_project():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        select_projects = (
            select(Projects, PassportOfProjects, StadiaOfProjects)
            .join(PassportOfProjects)
            .join(StadiaOfProjects)
            .order_by(PassportOfProjects.passportName)
        )
        select_stadia = (
            select(StadiaOfProjects)
            .filter(StadiaOfProjects.IDstadiaofpr < 3)
            .order_by(StadiaOfProjects.IDstadiaofpr)
        )
        projects = db_sessions.execute(select_projects).all()
        first_project = projects[0]
        # stadia_modify = db_sessions.execute(select(StadiaOfProjects).filter(StadiaOfProjects.IDstadiaofpr == first_project.StadiaOfProjects.IDstadiaofpr)).all()
        stadia = db_sessions.execute(select_stadia).all()
        return render_template(
            "projects.html",
            projects=projects,
            stadia=stadia,
            # stadia_modify=stadia_modify
        )
    if request.method == "POST":
        select = get_select()
        db_sessions = get_session()
        project_filter = request.form["projectFilter"]
        stadia_filter = request.form["stadiaFilter"]
        where_project_filter = (
            PassportOfProjects.passportName.ilike("%" + project_filter + "%")
            if project_filter
            else text("1=1")
        )
        where_stadia_filter = (
            StadiaOfProjects.IDstadiaofpr == stadia_filter if stadia_filter else text("1=1")
        )
        select_projects = (
            select(Projects, PassportOfProjects, StadiaOfProjects)
            .join(PassportOfProjects)
            .join(StadiaOfProjects)
            .where(where_project_filter)
            .where(where_stadia_filter)
            .order_by(PassportOfProjects.passportName)
        )
        projects = db_sessions.execute(select_projects).all()
        return render_template("resultAccordionProjects.html", projects=projects)


@pages.route("/checkStadia", methods=["GET"])
def check_stadia():
    idproject = int(request.args.get("idProject"))
    db_sessions = get_session()
    select = get_select()
    select_project = select(Projects).filter(Projects.IDprojects == idproject)
    project = db_sessions.execute(select_project).first()
    if project[0].IDstadiaofpr < 3:
        stadia = db_sessions.execute(
            select(StadiaOfProjects.IDstadiaofpr, StadiaOfProjects.stadiaofprName)
            .filter(StadiaOfProjects.IDstadiaofpr < 3)
            .order_by(StadiaOfProjects.IDstadiaofpr)
        ).all()
        return jsonify([dict(row._mapping) for row in stadia]), 200
    stadia = db_sessions.execute(
        select(StadiaOfProjects.IDstadiaofpr, StadiaOfProjects.stadiaofprName).filter(
            StadiaOfProjects.IDstadiaofpr == project[0].IDstadiaofpr
        )
    ).first()
    return jsonify(dict(stadia._mapping)), 200


@pages.route("/admin/addProject", methods=["POST"])
def admin_add_project():
    db_sessions = get_session()
    iniciator = int(request.form.get("iniciator"))
    sheffpr = int(request.form["sheffpr"])
    project_name = str(request.form["projectName"])
    problem = str(request.form["problem"])
    purpose = str(request.form["purpose"])
    tasks = str(request.form["tasks"])
    result = str(request.form["result"])
    content = str(request.form.get("content"))
    deadline = str(request.form.get("deadline"))
    stages = str(request.form.get("stages"))
    resource = str(request.form.get("resource"))
    cost = str(request.form.get("cost"))
    criteria = str(request.form.get("criteria"))
    formResult = str(request.form.get("formResult"))

    add_passport = PassportOfProjects(
        IDinitpr=iniciator,
        IDsheffpr=sheffpr,
        passportName=project_name,
        passportProblem=problem,
        passportPurpose=purpose,
        passportTasks=tasks,
        passportResults=result,
        passportContent=content,
        passportDeadlines=deadline,
        passportStages=stages,
        passportResources=resource,
        passportCost=cost,
        passportCriteria=criteria,
        passportFormresults=formResult,
        passportPattern="",
        passportFull="",
        passportSigned="",
    )
    db_sessions.add(add_passport)
    db_sessions.flush()
    idpassport = add_passport.IDpassport

    add_project = Projects(IDpassport=idpassport, IDstadiaofpr=1)
    db_sessions.add(add_project)
    db_sessions.commit()
    return redirect("/admin/projects")


@pages.route("/admin/modifyProject", methods=["POST"])
def admin_modify_project():
    db_sessions = get_session()
    idprojects = request.form["modifyProject"]
    project_name = str(request.form["projectName"])
    problem = str(request.form["problem"])
    purpose = str(request.form["purpose"])
    tasks = str(request.form["tasks"])
    result = str(request.form["result"])
    content = str(request.form["content"])
    deadline = str(request.form["deadline"])
    stages = str(request.form["stages"])
    resource = str(request.form["resource"])
    cost = str(request.form["cost"])
    criteria = str(request.form["criteria"])
    formResult = str(request.form["formResult"])
    stadia = request.form.get("stadia")
    project = db_sessions.query(Projects).filter(Projects.IDprojects == idprojects).first()
    npr = (
        db_sessions.query(PassportOfProjects)
        .filter(PassportOfProjects.IDpassport == project.IDpassport)
        .first()
    )

    if str(project_name) != "":
        npr.passportName = str(project_name)
    if str(problem) != "":
        npr.passportProblem = str(problem)
    if str(purpose) != "":
        npr.passportPurpose = str(purpose)
    if str(tasks) != "":
        npr.passportTasks = str(tasks)
    if str(result) != "":
        npr.passportResults = str(result)
    if str(content) != "":
        npr.passportContent = str(content)
    if str(deadline) != "":
        npr.passportDeadlines = str(deadline)
    if str(stages) != "":
        npr.passportStages = str(stages)
    if str(resource) != "":
        npr.passportResources = str(resource)
    if str(cost) != "":
        npr.passportCost = str(cost)
    if str(criteria) != "":
        npr.passportCriteria = str(criteria)
    if str(formResult) != "":
        npr.passportFormresults = str(formResult)
    if stadia is not None:
        project.IDstadiaofpr = stadia
    db_sessions.commit()
    return redirect("/admin/projects")


@pages.route("/admin/deleteProject", methods=["POST"])  # удалить инициатора проектов
def admin_delete_project():
    idproject = int(request.form["deleteProject"])
    db_sessions = get_session()
    project = db_sessions.query(Projects).filter(Projects.IDprojects == idproject).first()
    db_sessions.query(Projects).filter(Projects.IDprojects == idproject).delete()
    db_sessions.query(PassportOfProjects).filter(
        PassportOfProjects.IDpassport == project.IDpassport
    ).delete()
    db_sessions.commit()
    return redirect("/admin/projects")


@pages.route("/getPassport", methods=["GET"])
def get_passport():
    args = request.args
    idpassport = args.get("idPassport")

    db_sessions = get_session()
    select = get_select()

    select = (
        select(PassportOfProjects, Initiatorsofprojects, Organizations)
        .join_from(
            PassportOfProjects,
            Initiatorsofprojects,
            Initiatorsofprojects.IDinitpr == PassportOfProjects.IDinitpr,
            isouter=True,
        )
        .join_from(
            Initiatorsofprojects,
            Organizations,
            Organizations.IDorg == Initiatorsofprojects.IDorg,
            isouter=True,
        )
        .filter(PassportOfProjects.IDpassport == idpassport)
    )
    record = db_sessions.execute(select).first()
    if not record:
        return

    context = {}
    context["passport_name"] = record.PassportOfProjects.passportName
    context["fio"] = record.Initiatorsofprojects.FullName
    context["pos"] = record.Initiatorsofprojects.initprPositions
    context["work"] = record.Organizations.orgName
    context["phone"] = record.Initiatorsofprojects.initprPhone
    context["email"] = record.Initiatorsofprojects.initprEmail
    context["problem"] = record.PassportOfProjects.passportProblem
    context["purpose"] = record.PassportOfProjects.passportPurpose
    context["task"] = record.PassportOfProjects.passportTasks
    context["result"] = record.PassportOfProjects.passportResults
    context["content"] = record.PassportOfProjects.passportContent or "Не заполнено"
    context["deadline"] = record.PassportOfProjects.passportDeadlines or "Не заполнено"
    context["stages"] = record.PassportOfProjects.passportStages or "Не заполнено"
    context["resources"] = record.PassportOfProjects.passportResources or "Не заполнено"
    context["cost"] = record.PassportOfProjects.passportCost or "Не заполнено"
    context["criteria"] = record.PassportOfProjects.passportCriteria or "Не заполнено"
    context["formresult"] = record.PassportOfProjects.passportFormresults or "Не заполнено"

    filename = (
        "Паспорт "
        + str(record.PassportOfProjects.passportName).replace('"', "")
        + "_"
        + date.today().strftime("%d_%B_%Y")
        + ".doc"
    )
    file_path = path.join("documents", filename)
    doc = DocxTemplate("./documents/passport_template.docx")

    doc.render(context)

    doc.save(file_path)

    return send_file(file_path, mimetype="multipart/form-data", as_attachment=True)


@pages.route("/getPassportSigned", methods=["GET"])
def get_passport_signed():
    args = request.args
    idpassport = args.get("idPassport")

    db_sessions = get_session()
    passport = (
        db_sessions.query(PassportOfProjects)
        .filter(PassportOfProjects.IDpassport == idpassport)
        .first()
    )

    if not passport.passportSigned:
        return "", 404

    return send_file(passport.passportSigned, mimetype="multipart/form-data", as_attachment=True)


# загрузить подписанный договор
@pages.route("/uploadPassportSigned", methods=["POST"])
def upload_passport():
    upload_file = request.files.get("file")
    idpassport = request.form.get("passport_id")
    if not upload_file or not idpassport:
        return

    file_path = path.join("documents", upload_file.filename)

    db_sessions = get_session()
    passport = (
        db_sessions.query(PassportOfProjects)
        .filter(PassportOfProjects.IDpassport == idpassport)
        .first()
    )
    passport.passportSigned = file_path
    db_sessions.commit()

    upload_file.save(file_path)

    return redirect("/admin/contracts", code=307)


# удалить подписанный договор
@pages.route("/deletePassportSigned", methods=["POST"])
def delete_passport():
    idpassport = request.form.get("idPassport")
    if not idpassport:
        return

    db_sessions = get_session()
    passport = (
        db_sessions.query(PassportOfProjects)
        .filter(PassportOfProjects.IDpassport == idpassport)
        .first()
    )
    passport.passportSigned = ""
    db_sessions.commit()
    return redirect("/admin/contracts", code=307)


@pages.route(
    "/iniciators/mailadmin", methods=["GET", "POST"]
)  # Договоры об организации проектного обучения
def iniciators_org_mailadmin():
    return sheff_org_mailadmin()


@pages.route("/sheffproj/projects", methods=["GET", "POST"])
def sheffproj_projects():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        idsheffpr = session["user"][0]
        select_projects = (
            select(Projects, PassportOfProjects, StadiaOfProjects)
            .join(PassportOfProjects)
            .join(StadiaOfProjects)
            # .filter(StadiaOfProjects.IDstadiaofpr == 3)
            .filter(PassportOfProjects.IDsheffpr == idsheffpr)
            .order_by(PassportOfProjects.passportName)
        )
        projects = db_sessions.execute(select_projects).all()
        return render_template("sheffproj_projects.html", projects=projects)


@pages.route("/sheffproj/modifyProject", methods=["POST"])
def sheffproj_modify_project():
    db_sessions = get_session()
    idprojects = request.form["modifyProject"]
    project_name = str(request.form["projectName"])
    problem = str(request.form["problem"])
    purpose = str(request.form["purpose"])
    tasks = str(request.form["tasks"])
    result = str(request.form["result"])
    content = str(request.form["content"])
    deadline = str(request.form["deadline"])
    stages = str(request.form["stages"])
    resource = str(request.form["resource"])
    cost = str(request.form["cost"])
    criteria = str(request.form["criteria"])
    formResult = str(request.form["formResult"])
    project = db_sessions.query(Projects).filter(Projects.IDprojects == idprojects).first()
    npr = (
        db_sessions.query(PassportOfProjects)
        .filter(PassportOfProjects.IDpassport == project.IDpassport)
        .first()
    )

    if str(project_name) != "":
        npr.passportName = str(project_name)
    if str(problem) != "":
        npr.passportProblem = str(problem)
    if str(purpose) != "":
        npr.passportPurpose = str(purpose)
    if str(tasks) != "":
        npr.passportTasks = str(tasks)
    if str(result) != "":
        npr.passportResults = str(result)
    if str(content) != "":
        npr.passportContent = str(content)
    if str(deadline) != "":
        npr.passportDeadlines = str(deadline)
    if str(stages) != "":
        npr.passportStages = str(stages)
    if str(resource) != "":
        npr.passportResources = str(resource)
    if str(cost) != "":
        npr.passportCost = str(cost)
    if str(criteria) != "":
        npr.passportCriteria = str(criteria)
    if str(formResult) != "":
        npr.passportFormresults = str(formResult)
    db_sessions.commit()
    return redirect("/admin/projects")


@pages.route("/sheffproj/assignment", methods=["GET"])
def sheffproj_assignment_project():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        select_projects = (
            select(Projects, PassportOfProjects, StadiaOfProjects)
            .join(PassportOfProjects)
            .join(StadiaOfProjects)
            .filter(StadiaOfProjects.IDstadiaofpr == 2)
            .order_by(PassportOfProjects.passportName)
        )
        projects = db_sessions.execute(select_projects).all()
        return render_template("sheffproj_assignment.html", projects=projects)


@pages.route("/sheffproj/assignSheffProj", methods=["POST"])
def assign_sheff_proj_project():
    if request.method == "POST":
        db_sessions = get_session()
        idproject = request.form["project"]

        project = db_sessions.query(Projects).filter(Projects.IDprojects == idproject).first()
        npr = (
            db_sessions.query(PassportOfProjects)
            .filter(PassportOfProjects.IDpassport == project.IDpassport)
            .first()
        )
        npr.IDsheffpr = session["user"][0]
        project.IDstadiaofpr = 3
        db_sessions.commit()
        return redirect("/sheffproj/assignment")


@pages.route("/admin/stadia", methods=["GET"])
def admin_stadia():
    if request.method == "GET":
        db_sessions = get_session()
        select = get_select()
        select_projects = (
            select(Projects, PassportOfProjects, StadiaOfProjects)
            .join(PassportOfProjects)
            .join(StadiaOfProjects)
            .filter(StadiaOfProjects.IDstadiaofpr == 1)
            .order_by(PassportOfProjects.passportName)
        )
        projects = db_sessions.execute(select_projects).all()
        return render_template("stadia.html", projects=projects)


@pages.route("/admin/changeStadia", methods=["POST"])
def admin_change_stadia():
    if request.method == "POST":
        db_sessions = get_session()
        idproject = request.form["project"]

        project = db_sessions.query(Projects).filter(Projects.IDprojects == idproject).first()
        npr = (
            db_sessions.query(PassportOfProjects)
            .filter(PassportOfProjects.IDpassport == project.IDpassport)
            .first()
        )
        project.IDstadiaofpr = 2
        db_sessions.commit()
        return redirect("/admin/stadia")


@pages.route("/sheffproj/members", methods=["GET", "POST"])
def sheffproj_members():
    if request.method == "GET":
        db_sessions = get_session()
        select = get_select()
        idsheffpr = session["user"][0]
        select_projects = (
            select(
                PassportOfProjects.IDpassport, PassportOfProjects.passportName, Projects.IDprojects
            )
            .join(Projects)
            .filter(PassportOfProjects.IDsheffpr == idsheffpr)
        )
        select_roles = (
            select(RolesOfProjects)
            .join(PassportOfProjects)
            .filter(PassportOfProjects.IDsheffpr == idsheffpr)
        )
        exists_roles = db_sessions.query(RolesOfProjects.IDpassport).distinct().all()

        select_students = (
            select(Students.FullName, StudentsInProjects.IDroles, Groups.groupsName)
            .join(StudentsInProjects)
            .join(Groups)
            .join(Projects)
            .join(PassportOfProjects)
            .filter(PassportOfProjects.IDsheffpr == idsheffpr)
        )
        select_spec = select(SpecializationInProjects.IDroles, Specializations.FullSpec).join(
            Specializations
        )
        select_comp = select(
            CompetensionsInProject.IDroles,
            Competensions.competensionsShifr,
            Competensions.competensionsFull,
        ).join(Competensions)
        select_check_spec = select(Specializations)
        spec = db_sessions.execute(select_spec).all()
        comp = db_sessions.execute(select_comp).all()
        roles = db_sessions.execute(select_roles).all()
        projects = db_sessions.execute(select_projects).all()
        students = db_sessions.execute(select_students).all()
        check_spec = db_sessions.execute(select_check_spec).all()
        return render_template(
            "sheffproj_members.html",
            students=students,
            projects=projects,
            spec=spec,
            comp=comp,
            roles=roles,
        )
    if request.method == "POST":
        db_sessions = get_session()
        select = get_select()
        fio_filter = request.form["projectFioFilter"]
        role_filter = request.form["projectRoleFilter"]
        napr_filter = request.form["projectNaprFilter"]
        idsheffpr = session["user"][0]
        where_fio_filter = (
            Students.FullName.ilike("%" + fio_filter + "%") if fio_filter else text("1=1")
        )
        where_role_filter = (
            RolesOfProjects.rolesRole.ilike("%" + role_filter + "%") if role_filter else text("1=1")
        )
        where_napr_filter = (
            Specializations.FullSpec.ilike("%" + napr_filter + "%") if napr_filter else text("1=1")
        )
        select_projects = (
            select(
                PassportOfProjects.IDpassport, PassportOfProjects.passportName, Projects.IDprojects
            )
            .join(Projects)
            .filter(PassportOfProjects.IDsheffpr == idsheffpr)
        )
        select_roles = (
            select(RolesOfProjects)
            .join(PassportOfProjects)
            .filter(PassportOfProjects.IDsheffpr == idsheffpr)
            .filter(where_role_filter)
        )
        exists_roles = db_sessions.query(RolesOfProjects.IDpassport).distinct().all()

        select_students = (
            select(Students.FullName, StudentsInProjects.IDroles, Groups.groupsName)
            .join(StudentsInProjects)
            .join(Groups)
            .join(Projects)
            .join(PassportOfProjects)
            .filter(PassportOfProjects.IDsheffpr == idsheffpr)
            .filter(where_fio_filter)
        )
        select_spec = (
            select(SpecializationInProjects.IDroles, Specializations.FullSpec)
            .join(Specializations)
            .filter(where_napr_filter)
        )
        select_comp = select(
            CompetensionsInProject.IDroles,
            Competensions.competensionsShifr,
            Competensions.competensionsFull,
        ).join(Competensions)
        select_check_spec = select(Specializations)
        spec = db_sessions.execute(select_spec).all()
        comp = db_sessions.execute(select_comp).all()
        roles = db_sessions.execute(select_roles).all()
        projects = db_sessions.execute(select_projects).all()
        students = db_sessions.execute(select_students).all()
        check_spec = db_sessions.execute(select_check_spec).all()
        return render_template(
            "resultAccordionMembers.html",
            students=students,
            projects=projects,
            spec=spec,
            comp=comp,
            exists_members=exists_roles[0],
            roles=roles,
            check_spec=check_spec,
        )


@pages.route("/admin/mail_shefforg", methods=["GET"])
def admin_mail_shefforg():
    if request.method == "GET":
        db_sessions = get_session()
        select = get_select()
        select_shefforg = (
            select(
                Shefforganizations.shefforgEmail,
                Shefforganizations.FullName + " - " + Organizations.orgName,
            )
            .join(Organizations)
            .order_by(Shefforganizations.FullName)
        )
        shefforg = db_sessions.execute(select_shefforg).all()
        return render_template("mail_shefforg.html", users=shefforg)


@pages.route("/admin/mail_inic", methods=["GET"])
def admin_mail_inic():
    if request.method == "GET":
        db_sessions = get_session()
        select = get_select()
        select_iniciators = (
            select(
                Initiatorsofprojects.initprEmail,
                Initiatorsofprojects.FullName + " - " + Organizations.orgName,
            )
            .join(Organizations)
            .order_by(Initiatorsofprojects.FullName)
        )
        iniciators = db_sessions.execute(select_iniciators).all()
        return render_template("mail_inic.html", users=iniciators)


@pages.route("/getCompetitionsSpec", methods=["GET"])
def get_competitions_spec():
    if request.method == "GET":
        db_sessions = get_session()
        select = get_select()
        idspec = request.args.get("id")
        select_spec = select(
            Competensions.IDcompetensions,
            Competensions.competensionsShifr,
            Competensions.competensionsFull,
        ).filter(Competensions.IDspec == idspec)
        spec = db_sessions.execute(select_spec).all()
        return jsonify([list(el) for el in spec]), 200


@pages.route("/shefforg/projects", methods=["GET", "POST"])
def shefforg_project():
    if request.method == "GET":
        idorg = session["user"][0]
        select = get_select()
        db_sessions = get_session()
        select_stadia = select(StadiaOfProjects).order_by(StadiaOfProjects.IDstadiaofpr)
        select_projects = (
            select(Projects, PassportOfProjects, StadiaOfProjects)
            .join(PassportOfProjects)
            .join(StadiaOfProjects)
            .join(Initiatorsofprojects)
            .filter(Initiatorsofprojects.IDorg == idorg)
            .order_by(PassportOfProjects.passportName)
        )
        stadia = db_sessions.execute(select_stadia).all()
        projects = db_sessions.execute(select_projects).all()
        return render_template("sheff_org_projects.html", projects=projects, stadia=stadia)
    if request.method == "POST":
        idorg = session["user"][0]
        select = get_select()
        db_sessions = get_session()
        project_filter = request.form["projectFilter"]
        stadia_filter = request.form["stadiaFilter"]
        where_project_filter = (
            PassportOfProjects.passportName.ilike("%" + project_filter + "%")
            if project_filter
            else text("1=1")
        )
        where_stadia_filter = (
            StadiaOfProjects.IDstadiaofpr == stadia_filter if stadia_filter else text("1=1")
        )
        select_projects = (
            select(Projects, PassportOfProjects, StadiaOfProjects)
            .join(PassportOfProjects)
            .join(StadiaOfProjects)
            .join(Initiatorsofprojects)
            .filter(Initiatorsofprojects.IDorg == idorg)
            .where(where_project_filter)
            .where(where_stadia_filter)
            .order_by(PassportOfProjects.passportName)
        )
        projects = db_sessions.execute(select_projects).all()
        return render_template("resultAccordionProjects.html", projects=projects)


@pages.route("/sheffproj/roles", methods=["GET"])
def sheffproj_roles():
    if request.method == "GET":
        db_sessions = get_session()
        select = get_select()
        idsheffpr = session["user"][0]
        select_projects = (
            select(
                PassportOfProjects.IDpassport, PassportOfProjects.passportName, Projects.IDprojects
            )
            .join(Projects)
            .filter(PassportOfProjects.IDsheffpr == idsheffpr)
        )
        select_roles = (
            select(RolesOfProjects)
            .join(PassportOfProjects)
            .filter(PassportOfProjects.IDsheffpr == idsheffpr)
        )
        select_spec = select(SpecializationInProjects.IDroles, Specializations.FullSpec).join(
            Specializations
        )
        select_comp = select(
            CompetensionsInProject.IDroles,
            Competensions.competensionsShifr,
            Competensions.competensionsFull,
        ).join(Competensions)

        spec = db_sessions.execute(select_spec).all()
        comp = db_sessions.execute(select_comp).all()
        roles = db_sessions.execute(select_roles).all()
        projects = db_sessions.execute(select_projects).all()
        check_spec = db_sessions.execute(select(Specializations)).all()
        return render_template(
            "sheffproj_roles.html",
            projects=projects,
            spec=spec,
            comp=comp,
            roles=roles,
            check_spec=check_spec,
        )


@pages.route("/sheffproj/addRole", methods=["POST"])
def sheffproj_add_role():
    db_sessions = get_session()
    idpassport = request.form["passport"]
    role = str(request.form["role"])
    amount = request.form["amount"]
    function = str(request.form["function"])
    idspecs = request.form.getlist("spec")
    cost = str(request.form["cost"])
    idcomps = request.form.getlist("comp")
    require = str(request.form["require"])

    add_role = RolesOfProjects(
        IDpassport=idpassport,
        rolesRole=role,
        rolesAmount=amount,
        rolesFunction=function,
        rolesCost=cost,
        rolesRequirements=require,
    )
    db_sessions.add(add_role)
    db_sessions.flush()
    for idspec in idspecs:
        add_spec = SpecializationInProjects(IDroles=add_role.IDroles, IDspec=idspec)
        db_sessions.add(add_spec)
        db_sessions.flush()

    for idcomp in idcomps:
        add_comp = CompetensionsInProject(IDroles=add_role.IDroles, IDcompetensions=idcomp)
        db_sessions.add(add_comp)
        db_sessions.flush()

    db_sessions.commit()
    return redirect("/sheffproj/roles")


@pages.route("/sheffproj/modifyRole", methods=["POST"])
def sheffproj_modify_role():
    db_sessions = get_session()
    select = get_select()
    idrole = request.form["idrole"]
    idpassport = request.form["passport"]
    role = str(request.form["role"])
    amount = request.form["amount"]
    function = str(request.form["function"])
    idspecs = request.form.getlist("spec")
    cost = str(request.form["cost"])
    idcomps = request.form.getlist("comp")
    require = str(request.form["require"])

    rop = db_sessions.execute(
        select(RolesOfProjects).filter(RolesOfProjects.IDroles == idrole)
    ).first()[0]

    if len(idspecs) != 0:
        db_sessions.query(SpecializationInProjects).filter(
            SpecializationInProjects.IDroles == idrole
        ).delete()

    for idspec in idspecs:
        add_spec = SpecializationInProjects(IDroles=idrole, IDspec=idspec)
        db_sessions.add(add_spec)
        db_sessions.flush()

    if len(idcomps) != 0:
        db_sessions.query(CompetensionsInProject).filter(
            CompetensionsInProject.IDroles == idrole
        ).delete()

    for idcomp in idcomps:
        add_comp = CompetensionsInProject(IDroles=idrole, IDcompetensions=idcomp)
        db_sessions.add(add_comp)
        db_sessions.flush()

    if str(idpassport) != "":
        rop.IDpassport = idpassport
    if str(role) != "":
        rop.rolesRole = str(role)
    if str(amount) != "":
        rop.rolesAmount = str(amount)
    if str(function) != "":
        rop.rolesFunction = str(function)
    if str(cost) != "":
        rop.rolesCost = str(cost)
    if str(require) != "":
        rop.rolesRequirements = str(require)

    db_sessions.commit()
    return redirect("/sheffproj/roles")


@pages.route("/sheffproj/deleteRole", methods=["POST"])
def sheffproj_delete_role():
    db_sessions = get_session()
    idrole = request.form["idrole"]

    db_sessions.query(CompetensionsInProject).filter(
        CompetensionsInProject.IDroles == idrole
    ).delete()
    db_sessions.query(SpecializationInProjects).filter(
        SpecializationInProjects.IDroles == idrole
    ).delete()
    db_sessions.query(RolesOfProjects).filter(RolesOfProjects.IDroles == idrole).delete()
    db_sessions.commit()
    return redirect("/sheffproj/roles")


@pages.route("/student/participation_ticket", methods=["GET", "POST"])
def student_participation_ticket():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        idgroup = session["user"][0]
        select_projects = (
            select(Projects, PassportOfProjects, StadiaOfProjects)
            .distinct()
            .join(PassportOfProjects)
            .join(StadiaOfProjects)
            .join(RolesOfProjects)
            .join(SpecializationInProjects)
            .join_from(
                SpecializationInProjects,
                Groups,
                SpecializationInProjects.IDspec == Groups.IDspec,
                isouter=True,
            )
            .filter(Groups.IDgroups == idgroup)
            .filter(Projects.IDstadiaofpr == 3)
            .order_by(PassportOfProjects.passportName)
        )
        projects = db_sessions.execute(select_projects).all()
        first_project = projects[0] if projects else None
        roles = []
        if first_project:
            select_roles = select(
                RolesOfProjects.IDroles, RolesOfProjects.rolesRole, RolesOfProjects.rolesFunction
            ).filter(RolesOfProjects.IDpassport == first_project.PassportOfProjects.IDpassport)
            roles = db_sessions.execute(select_roles).all()
        return render_template("student_partic_tickets.html", projects=projects, roles=roles)
    if request.method == "POST":
        select = get_select()
        db_sessions = get_session()
        project_filter = request.form["projectFilter"]
        where_project_filter = (
            PassportOfProjects.passportName.ilike("%" + project_filter + "%")
            if project_filter
            else text("1=1")
        )
        select_projects = (
            select(Projects, PassportOfProjects, StadiaOfProjects)
            .distinct()
            .join(PassportOfProjects)
            .join(StadiaOfProjects)
            .join(RolesOfProjects)
            .join(SpecializationInProjects)
            .join_from(
                SpecializationInProjects,
                Groups,
                SpecializationInProjects.IDspec == Groups.IDspec,
                isouter=True,
            )
            .filter(Groups.IDgroups == idgroup)
            .filter(Projects.IDstadiaofpr == 3)
            .where(where_project_filter)
            .order_by(PassportOfProjects.passportName)
        )
        projects = db_sessions.execute(select_projects).all()
        return render_template("resultAccordionProjects.html", projects=projects)


@pages.route("/student/getRoles", methods=["GET"])
def student_get_roles():
    args = request.args
    idpassport = args.get("id")
    select = get_select()
    db_sessions = get_session()
    select_roles = select(
        RolesOfProjects.IDroles, RolesOfProjects.rolesRole, RolesOfProjects.rolesFunction
    ).filter(RolesOfProjects.IDpassport == idpassport)
    roles = db_sessions.execute(select_roles).all()
    return jsonify([dict(row._mapping) for row in roles]), 200


@pages.route("/student/addTicket", methods=["POST"])
def student_add_ticket():
    db_sessions = get_session()
    idproject = request.form["project"]
    idrole = request.form["role"]
    courseYear = request.form["courseYear"]
    reason = str(request.form["reason"])
    idstudent = session["user"][1]

    add_application = Applications(
        IDprojects=idproject,
        IDstudents=idstudent,
        applicationsCourse=courseYear,
        IDroles=idrole,
        applicationsPurpose=reason,
        applicationsPattern="",
        applicationsFull="",
        applicationsSigned="",
    )
    db_sessions.add(add_application)
    db_sessions.commit()

    return redirect("/student/participation_ticket")


@pages.route("/student/tickets", methods=["GET"])
def student_tickets():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        idgroup = session["user"][0]
        select_applications = (
            select(
                Applications,
            )
            .distinct()
            .join(PassportOfProjects)
            .join(StadiaOfProjects)
            .join(RolesOfProjects)
            .join(SpecializationInProjects)
            .join_from(
                SpecializationInProjects,
                Groups,
                SpecializationInProjects.IDspec == Groups.IDspec,
                isouter=True,
            )
            .filter(Groups.IDgroups == idgroup)
            .filter(Projects.IDstadiaofpr == 3)
            .order_by(PassportOfProjects.passportName)
        )
        projects = db_sessions.execute(select_projects).all()
        first_project = projects[0] if projects else None
        roles = []
        if first_project:
            select_roles = select(
                RolesOfProjects.IDroles, RolesOfProjects.rolesRole, RolesOfProjects.rolesFunction
            ).filter(RolesOfProjects.IDpassport == first_project.PassportOfProjects.IDpassport)
            roles = db_sessions.execute(select_roles).all()
        return render_template("student_partic_tickets.html", projects=projects, roles=roles)
