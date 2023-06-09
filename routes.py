from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from os import path, remove
import hashlib
import locale
import csv
import re
from docxtpl import DocxTemplate
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    send_file,
    jsonify,
    url_for,
)
from sqlalchemy import text, func
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
    Confirmation,
    Levels,
    StadiaOfWorks,
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
    db_session = get_session()

    if role == "administrator":
        data_workers = (
            db_session.query(Sheffofprojects).filter(Sheffofprojects.Login == login).first()
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
        session["pos"] = "Администратор системы"
        session["email"] = data_workers.sheffprEmail
        session["firstNav"] = "Панель администратора"
        return redirect("/admin/reg_shefforg")
    if role == "sheffofprojects":
        data_workers = (
            db_session.query(Sheffofprojects).filter(Sheffofprojects.Login == login).first()
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
        session["pos"] = data_workers.positionsName.positionsName
        session["firstNav"] = "Панель руководителя"
        session["secondNav"] = "проекта"
        session["email"] = data_workers.sheffprEmail
        session["user"] = [data_workers.IDsheffpr]
        return redirect("/sheffproj/assignment")
    if role == "shefforganizations":
        data_workers = (
            db_session.query(Shefforganizations).filter(Shefforganizations.Login == login).first()
        )
        if not (
            data_workers is not None
            and (data_workers.Login == login and data_workers.Pass == rendered_pass)
        ):
            return render_template("index.html", title="Неверный логин и/или пароль!!!")
        org = (
            db_session.query(Organizations)
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
            db_session.query(Initiatorsofprojects)
            .filter(Initiatorsofprojects.Login == login)
            .first()
        )
        if not (
            data_workers is not None
            and (data_workers.Login == login and data_workers.Pass == rendered_pass)
        ):
            return render_template("index.html", title="Неверный логин и/или пароль!!!")
        org = (
            db_session.query(Organizations)
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
        data_workers = db_session.query(Students).filter(Students.Login == login).first()
        if not (
            data_workers is not None
            and (data_workers.Login == login and data_workers.Pass == rendered_pass)
        ):
            return render_template("index.html", title="Неверный логин и/или пароль!!!")
        group = db_session.query(Groups).filter(Groups.IDgroups == data_workers.IDgroups).first()
        session["fullName"] = [
            data_workers.studentsFirstname,
            data_workers.studentsName,
            data_workers.studentsFathername,
        ]
        session["url"] = "student"
        session["pos"] = group.groupsName
        session["firstNav"] = "Панель студента"
        session["email"] = data_workers.studentsEmail
        cur_date = datetime.now() + relativedelta(months=7)
        session["user"] = [
            group.IDgroups,
            data_workers.IDstudents,
            cur_date.year - group.groupsYear,
        ]
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
        db_session = get_session()
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
        shefforg = db_session.execute(pagination(select_shefforg)).all()
        shefforg_edit = db_session.execute(select_shefforg).all()
        count = db_session.execute(count_records(select_shefforg, Shefforganizations.IDshefforg)).scalar_one()
        db_session.commit()
        return render_template("registration.html", shefforg=shefforg, shefforg_edit=shefforg_edit, count=count, page=0, function="applyorgFilters")
    if request.method == "POST":
        fio_filter = request.form["fioFilter"]
        org_filter = request.form["orgFilter"]
        page = (request.form.get("page") and int(request.form.get("page"))) or 0
        where_fio_filter = (
            Shefforganizations.FullName.ilike("%" + fio_filter + "%") if fio_filter else text("1=1")
        )
        where_org_filter = (
            Organizations.orgName.ilike("%" + org_filter + "%") if org_filter else text("1=1")
        )
        select = get_select()
        db_session = get_session()
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
        shefforg = db_session.execute(pagination(select_shefforg, page)).all()
        count = db_session.execute(count_records(select_shefforg, Shefforganizations.IDshefforg)).scalar_one()
        db_session.commit()
        return render_template("resultTableRegSheffOrg.html", shefforg=shefforg, count=count,
            page=page,
            function="applyFilters")


@pages.route("/admin/add-shefforg", methods=["GET", "POST"])  # добавление рук.организации
def addshefforg():
    if request.method == "POST":
        db_session = get_session()
        firstname = str(request.form["shefforgFirstname"])
        name = str(request.form["shefforgName"])
        fathername = str(request.form["shefforgFathername"])
        pos = str(request.form.get("shefforgPositions"))
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
        db_session.add(add)
        db_session.commit()
        return redirect("/admin/reg_shefforg")


@pages.route("/admin/delsheforg", methods=["GET", "POST"])  # удаление рук.организации
def delshefforg():
    if request.method == "POST":
        db_session = get_session()
        idshefforg = int(request.form["delsheforg"])
        db_session.query(Shefforganizations).filter(
            Shefforganizations.IDshefforg == idshefforg
        ).delete()
        db_session.commit()
        return redirect("/admin/reg_shefforg")


@pages.route("/admin/redshefforganiz", methods=["GET", "POST"])  # редактирование рук.организации
def redshefforg():
    if request.method == "POST":
        db_session = get_session()
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
            db_session.query(Shefforganizations)
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
        db_session.commit()
        return redirect("/admin/reg_shefforg")


@pages.route("/admin/organization", methods=["GET", "POST"])  # админка-регистрация организации
def organization():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
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
            .distinct()
            .join_from(
                Shefforganizations,
                Organizations,
                Organizations.IDshefforg == Shefforganizations.IDshefforg,
                isouter=True,
            )
            .order_by(Shefforganizations.FullName)
        )
        shefforg = db_session.execute(select_shefforg).all()
        organizations = db_session.execute(select_org).all()
        orgsheff = db_session.execute(pagination(select_orgsheff)).all()
        count = db_session.execute(count_records(select_orgsheff, Shefforganizations.IDshefforg)).scalar_one()
        db_session.commit()
        return render_template(
            "organization.html", shefforg=shefforg, organizations=organizations, orgsheff=orgsheff, count=count,
            page=0,
            function="applyorgFilters"
        )
    if request.method == "POST":
        fio_filters = request.form["fioFilters"]
        org_filters = request.form["orgFilters"]
        yuradress_filters = request.form["yuradressFilters"]
        page = (request.form.get("page") and int(request.form.get("page"))) or 0
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
        db_session = get_session()
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
        shefforg = db_session.execute(pagination(select_shefforg, page)).all()
        organizations = db_session.execute(select_org).all()
        orgsheff = db_session.execute(select_orgsheff).all()
        count = db_session.execute(count_records(select_shefforg, Shefforganizations.IDshefforg)).scalar_one()
        db_session.commit()
        return render_template(
            "resultTableOrg.html", shefforg=shefforg, organizations=organizations, orgsheff=orgsheff, count=count, page=page, function="applyorgFilters"
        )


@pages.route("/admin/add-org", methods=["GET", "POST"])  # добавление организации
def addorg():
    if request.method == "POST":
        db_session = get_session()
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
        db_session.add(add)
        db_session.commit()
        return redirect("/admin/organization")


@pages.route("/admin/delorg", methods=["GET", "POST"])  # удаление организации
def delorg():
    if request.method == "POST":
        db_session = get_session()
        idorg = int(request.form["delorg"])
        db_session.query(Organizations).filter(Organizations.IDorg == idorg).delete()
        db_session.commit()
        return redirect("/admin/organization")


@pages.route("/admin/redorganiz", methods=["GET", "POST"])  # редактирование организации
def redorg():
    if request.method == "POST":
        db_session = get_session()
        idorg = int(request.form["redorg"])
        idsheforg = request.form["redsheforg"]
        name = request.form["redorgName"]
        yur = request.form["redorgYuraddress"]
        adres = request.form["redorgPostaddress"]
        em = request.form["redorgEmail"]
        phone = request.form["redorgPhone"]
        npr = db_session.query(Organizations).filter(Organizations.IDorg == idorg).first()
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
        db_session.commit()
        return redirect("/admin/organization")


@pages.route(
    "/admin/contracts", methods=["GET", "POST"]
)  # Договоры об организации проектного обучения
def route_contracts():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
        select_org = select(Organizations).order_by(Organizations.orgName)
        select_contracts = select(Contracts).order_by(
            Contracts.contractsNumber, Contracts.contractsStart
        )
        select_contracts_order = (
            select(Contracts)
            .join(Organizations)
            .order_by(Organizations.orgName, Contracts.contractsNumber, Contracts.contractsStart)
        )
        contracts = db_session.execute(pagination(select_contracts)).all()
        organizations = db_session.execute(select_org).all()
        contracts_order = db_session.execute(select_contracts_order).all()
        count = db_session.execute(count_records(select_contracts, Contracts.IDcontracts)).scalar_one()

        db_session.commit()
        return render_template(
            "contracts.html",
            contracts=contracts,
            organizations=organizations,
            contracts_order=contracts_order,
            count=count,
            page=0,
            function="applyContractsFilters"
        )
    if request.method == "POST":
        date_filters = request.form.get("dateContractFilter")
        org_filters = request.form.get("orgFilters")
        number_filters = request.form.get("numberContractFilter")
        page = (request.form.get("page") and int(request.form.get("page"))) or 0
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
        db_session = get_session()
        select_contracts = (
            select(Contracts)
            .join(Organizations)
            .where(where_number_filters)
            .where(where_date_filters)
            .where(where_org_filters)
            .order_by(Contracts.contractsNumber, Contracts.contractsStart)
        )
        contracts = db_session.execute(pagination(select_contracts, page)).all()
        count = db_session.execute(count_records(select_contracts, Contracts.IDcontracts)).scalar_one()
        db_session.commit()
        return render_template("resultTableContracts.html", contracts=contracts, count=count, page=0, function="applyContractsFilters")


@pages.route("/admin/addContract", methods=["POST"])  # добавление договора
def add_contract():
    if request.method == "POST":
        db_session = get_session()
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
        db_session.add(add)
        db_session.commit()
        return redirect("/admin/contracts")


@pages.route("/admin/delContract", methods=["POST"])  # удаление договора
def del_contract():
    if request.method == "POST":
        db_session = get_session()
        id_contract = int(request.form["delContract"])
        db_session.query(Contracts).filter(Contracts.IDcontracts == id_contract).delete()
        db_session.commit()
        return redirect("/admin/contracts")


@pages.route("/admin/modifyContract", methods=["POST"])  # редактирование договора
def modify_contract():
    if request.method == "POST":
        db_session = get_session()
        id_contract = int(request.form["modifyContract"])
        id_org = request.form["addorg"]
        contract_number = request.form["contractNumber"]
        contract_start_date = request.form["contractStart"]
        contract_end_date = request.form["contractEnd"]
        npr = db_session.query(Contracts).filter(Contracts.IDcontracts == id_contract).first()
        if str(id_org) != "":
            npr.IDorg = int(id_org)
        if str(contract_number) != "":
            npr.contractsNumber = int(contract_number)
        if str(contract_start_date) != "":
            npr.contractsStart = str(contract_start_date)
        if str(contract_end_date) != "":
            npr.contractsFinish = str(contract_end_date)
        db_session.commit()
        return redirect("/admin/contracts")


# получение договора
@pages.route("/getContract", methods=["GET"])
def create_and_send_document():
    args = request.args
    id_contract = args.get("idContract")

    db_session = get_session()
    select = text(
        """SELECT p.contractsNumber, o.orgName, p.contractsFinish, o.orgYuraddress, o.orgPostaddress, p.contractsStart, s.shefforgDoc, s.shefforgFirstname as firstName, s.shefforgName as name, s.shefforgFathername as surname, s.shefforgPositions
        FROM projectsudycontracts p
            inner join organizations o on ( o.IDorg = p.IDorg )
            inner join shefforganizations s on ( s.IDshefforg = o.IDshefforg)
        WHERE
            p.IDcontracts = :id_contract
        """
    )

    contract = db_session.execute(select, {"id_contract": id_contract}).first()

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

    db_session = get_session()
    contract = db_session.query(Contracts).filter(Contracts.IDcontracts == id_contract).first()

    if not contract.contractsSigned:
        return "", 404

    return send_file(contract.contractsSigned, mimetype="multipart/form-data", as_attachment=True)


# загрузить подписанный договор
@pages.route("/admin/uploadContractSigned", methods=["POST"])
def upload_document():
    upload_file = request.files.get("file")
    id_contract = request.form.get("contract_id")
    if not upload_file or not id_contract:
        return

    file_path = path.join("documents", upload_file.filename)

    db_session = get_session()
    contract = db_session.query(Contracts).filter(Contracts.IDcontracts == id_contract).first()
    contract.contractsSigned = file_path
    db_session.commit()

    upload_file.save(file_path)

    return redirect("/admin/contracts", code=307)


# загрузить подписанный договор
@pages.route("/shefforg/uploadContractSigned", methods=["POST"])
def upload_shefforg_document():
    upload_file = request.files.get("file")
    id_contract = request.form.get("contract_id")
    if not upload_file or not id_contract:
        return

    file_path = path.join("documents", upload_file.filename)

    db_session = get_session()
    contract = db_session.query(Contracts).filter(Contracts.IDcontracts == id_contract).first()
    contract.contractsSigned = file_path
    db_session.commit()

    upload_file.save(file_path)

    return redirect("/shefforg/contracts", code=307)


# удалить подписанный договор
@pages.route("/admin/deleteContractSigned", methods=["POST"])
def delete_document():
    id_contract = request.form.get("idContract")
    if not id_contract:
        return

    db_session = get_session()
    contract = db_session.query(Contracts).filter(Contracts.IDcontracts == id_contract).first()
    contract.contractsSigned = None
    db_session.commit()
    return redirect("/admin/contracts", code=307)


# удалить подписанный договор
@pages.route("/shefforg/deleteContractSigned", methods=["POST"])
def delete_shefforg_document():
    id_contract = request.form.get("idContract")
    if not id_contract:
        return

    db_session = get_session()
    contract = db_session.query(Contracts).filter(Contracts.IDcontracts == id_contract).first()
    contract.contractsSigned = None
    db_session.commit()
    return redirect("/shefforg/contracts", code=307)


@pages.route("/admin/specializations", methods=["GET", "POST"])  # Специализации
def specializations():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
        select_spec = select(Specializations).order_by(
            Specializations.specShifr,
            Specializations.specNapravlenie,
            Specializations.specNapravlennost,
        )
        specializations = db_session.execute(select_spec).all()
        db_session.commit()
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
        db_session = get_session()
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
        specializations = db_session.execute(select_spec).all()
        db_session.commit()
        return render_template("resultTableSpecializations.html", specializations=specializations)


@pages.route("/admin/addSpecialization", methods=["POST"])  # добавление специализации
def add_spec():
    if request.method == "POST":
        db_session = get_session()
        shifr = str(request.form["specShifr"])
        napravlenie = str(request.form["specNapravlenie"])
        napravlennost = str(request.form["specNapravlennost"])
        add = Specializations(
            specShifr=shifr,
            specNapravlenie=napravlenie,
            specNapravlennost=napravlennost,
        )
        db_session.add(add)
        db_session.commit()
        return redirect("/admin/specializations")


@pages.route("/admin/delSpecialization", methods=["POST"])  # удаление специализации
def del_spec():
    db_session = get_session()
    id_spec = int(request.form["delSpecialization"])
    db_session.query(Specializations).filter(Specializations.IDspec == id_spec).delete()
    db_session.commit()
    return redirect("/admin/specializations")


@pages.route("/admin/modifySpecialization", methods=["POST"])  # редактирование специализации
def modify_spec():
    if request.method == "POST":
        db_session = get_session()
        id_spec = int(request.form["modifySpecialization"])
        shifr = request.form["redspecShifr"]
        napr = request.form["redspecNapravlenie"]
        napravlennost = request.form["redspecNapravlennost"]
        npr = db_session.query(Specializations).filter(Specializations.IDspec == id_spec).first()
        if str(shifr) != "":
            npr.specShifr = str(shifr)
        if str(napr) != "":
            npr.specNapravlenie = str(napr)
        if str(napravlennost) != "":
            npr.specNapravlennost = str(napravlennost)
        db_session.commit()
        return redirect("/admin/specializations")


@pages.route("/admin/groups", methods=["GET", "POST"])  # Группы
def groups():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
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
        formst = db_session.execute(select_formst).all()
        specializations = db_session.execute(select_spec).all()
        groups = db_session.execute(select_groups).all()
        groups_table = db_session.execute(select_tablegr).all()
        db_session.commit()
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
        name_group = request.form.get("nameGroup")
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
        where_name_group = (
            Groups.groupsName.ilike("%" + name_group + "%") if name_group else text("1=1")
        )
        select = get_select()
        db_session = get_session()
        select_group = (
            select(Groups, Formstuding.form_stName, Specializations.FullSpec)
            .join(Formstuding)
            .join(Specializations)
            .where(where_form_education)
            .where(where_direct_study)
            .where(where_year_study)
            .where(where_name_group)
            .order_by(
                Specializations.FullSpec,
                Groups.groupsName,
                Groups.groupsYear,
                Formstuding.form_stName,
            )
        )
        groups_table = db_session.execute(select_group).all()
        db_session.commit()
        return render_template("resultTableGroups.html", groups_table=groups_table)


@pages.route("/admin/addGroup", methods=["POST"])  # Добавить группы
def addgroups():
    db_session = get_session()
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
    db_session.add(add)
    db_session.commit()
    return redirect("/admin/groups")


@pages.route("/admin/delGroup", methods=["POST"])  # Удалить группы
def delgroups():
    db_session = get_session()
    id_gr = int(request.form["delGroup"])
    db_session.query(Groups).filter(Groups.IDgroups == id_gr).delete()
    db_session.commit()
    return redirect("/admin/groups")


@pages.route("/admin/modifyGroup", methods=["POST"])  # Редактировать группы
def redgroups():
    db_session = get_session()
    id_gr = int(request.form["modifyGroups"])
    grname = request.form["redgroupsName"]
    gryear = request.form["redgroupsYear"]
    formst = request.form["redform_st"]
    spec = request.form["redspec"]
    npr = db_session.query(Groups).filter(Groups.IDgroups == id_gr).first()
    if str(grname) != "":
        npr.groupsName = str(grname)
    if str(gryear) != "":
        npr.groupsYear = int(gryear)
    if str(formst) != "":
        npr.IDform_st = int(formst)
    if str(spec) != "":
        npr.IDspec = int(spec)
    db_session.commit()
    return redirect("/admin/groups")


# Загрузка csv в специализации
@pages.route("/admin/csvSpec", methods=["POST"])
def insert_csv_spec():
    try:
        upload_file = request.files.get("file")
        file_path = path.join("documents", upload_file.filename)
        upload_file.save(file_path)
        with open(file_path, encoding="utf-8") as file:
            db_session = get_session()
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
                db_session.add(add)
                db_session.commit()
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
            db_session = get_session()
            select = get_select()
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                napr = row["Направление"].split("-")
                idform_st = db_session.execute(
                    select(Formstuding.IDform_st).where(
                        Formstuding.form_stName == row["Форма обучения"]
                    )
                ).first()
                idspec = db_session.execute(
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
                db_session.add(add)
                db_session.commit()
        return "", 200
    finally:
        remove(file_path)


@pages.route("/admin/students", methods=["GET", "POST"])  # Студенты
def students():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
        select_groups = select(Groups).order_by(Groups.groupsName)
        groups = db_session.execute(select_groups).all()
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
        student = db_session.execute(select_student).all()
        modify_student = db_session.execute(select_modify_student).all()
        db_session.commit()
        return render_template(
            "students.html", student=student, groups=groups, modify_student=modify_student
        )
    if request.method == "POST":
        fio = request.form.get("fio")
        grname = request.form.get("grname")
        where_fio = Students.FullName.ilike("%" + fio + "%") if fio else text("1=1")
        where_grname = Groups.IDgroups == grname if grname else text("1=1")
        select = get_select()
        db_session = get_session()
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
        student = db_session.execute(select_student).all()
        db_session.commit()
        return render_template("resultTableStudents.html", student=student)


@pages.route("/admin/addStudents", methods=["POST"])  # Добавить студента
def addstudents():
    if request.method == "POST":
        db_session = get_session()
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
        db_session.add(add)
        db_session.commit()
        return redirect("/admin/students")


@pages.route("/admin/delStudent", methods=["POST"])  # Удалить студента
def delstudents():
    db_session = get_session()
    id_st = int(request.form["delStudent"])
    db_session.query(Students).filter(Students.IDstudents == id_st).delete()
    db_session.commit()
    return redirect("/admin/students")


@pages.route("/admin/modifyStudent", methods=["POST"])  # Редактировать студента
def modifyStudent():
    db_session = get_session()
    id_stud = int(request.form["redStudents"])
    fname = request.form["redstudentsFirstname"]
    name = request.form["redstudentsName"]
    lname = request.form["redstudentsFathername"]
    book = request.form["redstudentsStudbook"]
    tel = request.form["redstudentsPhone"]
    em = request.form["redstudentsEmail"]
    login = request.form["redLogin"]
    password = request.form["redPass"]
    idgroup = request.form["newGroup"]
    npr = db_session.query(Students).filter(Students.IDstudents == id_stud).first()
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
    db_session.commit()
    return redirect("/admin/students")


@pages.route("/admin/csvStud", methods=["POST"])
def insert_csv_stud():
    try:
        upload_file = request.files.get("file")
        file_path = path.join("documents", upload_file.filename)
        upload_file.save(file_path)
        with open(file_path, encoding="utf-8") as file:
            db_session = get_session()
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
                group = db_session.query(Groups).filter(Groups.groupsName == row["Группа"]).first()
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
                db_session.add(add)
                db_session.commit()
        return "", 200
    finally:
        remove(file_path)


@pages.route(
    "/admin/competitions/",
    defaults={"error": 0},
    methods=["GET", "POST"],
)  # Компетенции учебных планов
@pages.route(
    "/admin/competitions/<error>",
    methods=["GET", "POST"],
)  # Компетенции учебных планов
def get_competitions(error):
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
        select_sp = select(Specializations).order_by(
            Specializations.specShifr,
            Specializations.specNapravlenie,
            Specializations.specNapravlennost,
        )
        spec = db_session.execute(select_sp).all()
        idspec = None
        if spec:
            idspec = spec[0].Specializations.IDspec
        select_competitions = (
            select(Competensions, Specializations.FullSpec)
            .join(Specializations)
            .filter(Competensions.IDspec == idspec)
            .order_by(Competensions.competensionsShifr)
        )
        competitions = db_session.execute(select_competitions).all()
        db_session.commit()
        return render_template(
            "competitions.html", spec=spec, competitions=competitions, error=error
        )
    if request.method == "POST":
        spec = int(request.form["spec"])
        shifr = request.form.get("shifrFilter")
        full = request.form.get("fullFilter")
        where_shifr = (
            Competensions.competensionsShifr.ilike("%" + shifr + "%") if shifr else text("1=1")
        )
        where_full = (
            Competensions.competensionsFull.ilike("%" + full + "%") if full else text("1=1")
        )
        select = get_select()
        db_session = get_session()
        select_competitions = (
            select(Competensions, Specializations.FullSpec)
            .join(Specializations)
            .filter(Competensions.IDspec == spec)
            .filter(where_full)
            .filter(where_shifr)
            .order_by(Competensions.competensionsShifr)
        )
        competitions = db_session.execute(select_competitions).all()
        db_session.commit()
        return render_template("resultTableCompetitions.html", competitions=competitions)


@pages.route(
    "/admin/competitions/addCompetition", methods=["POST"]
)  # Добавить компетенцию учебного плана
def addcompetitions():
    db_session = get_session()
    id_spec = int(request.form["specialization"])
    cod = str(request.form["competensionsShifr"])
    full = str(request.form["competensionsFull"])
    add = Competensions(
        IDspec=id_spec,
        competensionsShifr=cod,
        competensionsFull=full,
    )
    db_session.add(add)
    db_session.commit()
    return redirect("/admin/competitions")


@pages.route("/admin/competitions/modifyCompetition", methods=["POST"])
def modify_competition():
    cod = str(request.form["competensionsShifr"])
    full = str(request.form["competensionsFull"])
    id_comp = int(request.form["competetion"])
    db_session = get_session()
    npr = db_session.query(Competensions).filter(Competensions.IDcompetensions == id_comp).first()
    if cod != "":
        npr.competensionsShifr = cod
    if full != "":
        npr.competensionsFull = full
    db_session.commit()
    return redirect("/admin/competitions")


@pages.route("/admin/competitions/deleteCompetition", methods=["POST"])
def delete_competition():
    try:
        id_comp = int(request.form["competetion"])
        db_session = get_session()
        db_session.query(Competensions).filter(Competensions.IDcompetensions == id_comp).delete()
        db_session.commit()
        return redirect("/admin/competitions")
    except:
        return redirect(url_for("pages.get_competitions", error=1))


@pages.route("/admin/csvComp", methods=["POST"])
def insert_csv_comp():
    try:
        upload_file = request.files.get("file")
        file_path = path.join("documents", upload_file.filename)
        upload_file.save(file_path)
        with open(file_path, encoding="utf-8") as file:
            db_session = get_session()
            select = get_select()
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                spec = row["Специализация"]
                code = row["Код"]
                content = row["Содержание"]
                id_spec = db_session.execute(
                    select(Specializations.IDspec).where(Specializations.FullSpec == spec)
                ).first()
                add = Competensions(
                    IDspec=id_spec[0], competensionsShifr=code, competensionsFull=content
                )
                db_session.add(add)
                db_session.commit()
        return "", 200
    finally:
        remove(file_path)


@pages.route("/admin/getStudentsGroup", methods=["GET"])
def get_students_group():
    args = request.args
    id_group = args.get("idGroup")
    select = get_select()
    db_session = get_session()
    select_students = (
        select(Students.IDstudents, Students.FullName, Students.studentsStudbook)
        .filter(Students.IDgroups == id_group)
        .order_by(Students.FullName)
    )
    students = db_session.execute(select_students).all()
    return jsonify([dict(row._mapping) for row in students]), 200


@pages.route("/admin/getCompetition", methods=["GET"])
def get_competition_on_spec():
    args = request.args
    id_spec = args.get("spec")
    select = get_select()
    db_session = get_session()
    select_competition = (
        select(Competensions.competensionsShifr, Competensions.IDcompetensions)
        .filter(Competensions.IDspec == id_spec)
        .order_by(Competensions.competensionsShifr)
    )
    competitions = db_session.execute(select_competition).all()
    return jsonify([dict(row._mapping) for row in competitions]), 200


@pages.route("/admin/cafedra", methods=["GET", "POST"])  # Состав кафедры ИВТ
def cafedra():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
        select_caf = (
            select(Sheffofprojects, Positions)
            .join(Positions)
            .order_by(Sheffofprojects.FullName, Positions.positionsName)
        )
        select_pos = select(Positions).order_by(Positions.positionsName)
        caf = db_session.execute(select_caf).all()
        pos = db_session.execute(select_pos).all()
        db_session.commit()
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
        db_session = get_session()
        select_caf = (
            select(Sheffofprojects, Positions)
            .join(Positions)
            .where(where_fio_filters)
            .where(where_pos_filters)
            .order_by(Sheffofprojects.FullName, Positions.positionsName)
        )
        select_pos = select(Positions).order_by(Positions.positionsName)
        caf = db_session.execute(select_caf).all()
        pos = db_session.execute(select_pos).all()
        db_session.commit()
        return render_template("resultTableCafedra.html", caf=caf, pos=pos)


@pages.route("/admin/addCafedra", methods=["POST"])  # добавить сотрудника ИВТ
def addcafedra():
    db_session = get_session()
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
    db_session.add(add)
    db_session.commit()
    return redirect("/admin/cafedra")


@pages.route("/admin/delCafedra", methods=["POST"])  # удалить сотрудника ИВТ
def delcafedra():
    id_sotr = int(request.form["delsotr"])
    db_session = get_session()
    db_session.query(Sheffofprojects).filter(Sheffofprojects.IDsheffpr == id_sotr).delete()
    db_session.commit()
    return redirect("/admin/cafedra")


@pages.route("/admin/modifyCafedra", methods=["POST"])  # Редактировать сотрудника ИВТ
def modifyCafedra():
    db_session = get_session()
    id_sotr = request.form["modifysotr"]
    firstname = request.form["redsheffprFirstname"]
    name = request.form["redsheffprName"]
    lastname = request.form["redsheffprFathername"]
    posit = request.form["redposName"]
    phone = request.form["redsheffprPhone"]
    em = request.form["redsheffprEmail"]
    login = request.form["redLogin"]
    password = request.form["redPass"]
    npr = db_session.query(Sheffofprojects).filter(Sheffofprojects.IDsheffpr == id_sotr).first()
    positions = None
    old_name = npr.FullName
    sess_name = f"{session['fullName'][0]} {session['fullName'][1]} {session['fullName'][2]} {session['fullName'][3]}"
    if str(posit) != "":
        npr.IDpositions = int(posit)
        positions = db_session.query(Positions).filter(Positions.IDpositions == posit).first()
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
            positions.positionsName if positions else npr.positionsName.positionsName,
        ]
    db_session.commit()
    return redirect("/admin/cafedra")


@pages.route("/admin/csvCafedra", methods=["POST"])
def insert_csv_cafedra():
    try:
        upload_file = request.files.get("file")
        file_path = path.join("documents", upload_file.filename)
        upload_file.save(file_path)
        with open(file_path, encoding="utf-8") as file:
            db_session = get_session()
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
                id_pos = db_session.execute(
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
                db_session.add(add)
                db_session.commit()
                return "", 200
    finally:
        remove(file_path)


@pages.route("/shefforg/organization", methods=["GET", "POST"])  # админка-регистрация организации
def sheff_org_organization():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
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
        orgsheff = db_session.execute(pagination(select_orgsheff)).all()
        count = db_session.execute(count_records(select_orgsheff, Shefforganizations.IDshefforg)).scalar_one()
        db_session.commit()
        return render_template("sheff_org_organization.html", orgsheff=orgsheff, count=count,
            page=0,
            function="applyorgFilters")
    if request.method == "POST":
        select = get_select()
        db_session = get_session()
        id_org = session["user"][0]
        page = (request.form.get("page") and int(request.form.get("page"))) or 0
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
        orgsheff = db_session.execute(pagination(select_orgsheff, page)).all()
        count = db_session.execute(count_records(select_orgsheff, Shefforganizations.IDshefforg)).scalar_one()
        db_session.commit()
        return render_template("resultTableOrg.html", orgsheff=orgsheff, count=count,
            page=0,
            function="applyorgFilters")


@pages.route("/shefforg/redorganiz", methods=["POST"])  # редактирование рук.организации
def sheff_org_redorg():
    if request.method == "POST":
        db_session = get_session()
        idorg = session["user"][0]
        name = request.form["redorgName"]
        yur = request.form["redorgYuraddress"]
        adres = request.form["redorgPostaddress"]
        em = request.form["redorgEmail"]
        phone = request.form["redorgPhone"]
        npr = db_session.query(Organizations).filter(Organizations.IDorg == idorg).first()
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
        db_session.commit()
        return redirect("/shefforg/organization")


@pages.route("/shefforg/reg_shefforg", methods=["GET"])  # админка-регистрация рук.огранизации
def shefforg_reg_shefforg():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
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
        shefforg = db_session.execute(select_shefforg).all()
        db_session.commit()
        return render_template("sheff_org_registration.html", shefforg=shefforg)


@pages.route("/shefforg/redshefforganiz", methods=["POST"])  # редактирование рук.организации
def shefforg_redshefforg():
    if request.method == "POST":
        db_session = get_session()
        idshefforg = session["user"][1]
        firstname = request.form["redshefforgFirstname"]
        name = request.form["redshefforgName"]
        fathername = request.form["redshefforgFathername"]
        pos = request.form["redshefforgPositions"]
        doc = request.form["redshefforgDoc"]
        em = request.form["redshefforgEmail"]
        phone = request.form["redshefforgPhone"]
        npr = (
            db_session.query(Shefforganizations)
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
        db_session.commit()

        return redirect("/shefforg/reg_shefforg")


@pages.route(
    "/shefforg/contracts", methods=["GET", "POST"]
)  # Договоры об организации проектного обучения
def sheff_org_contracts():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
        idorg = session["user"][0]
        select_contracts = (
            select(Contracts)
            .filter(Contracts.IDorg == idorg)
            .order_by(Contracts.contractsNumber, Contracts.contractsStart)
        )
        contracts = db_session.execute(pagination(select_contracts)).all()
        count = db_session.execute(count_records(select_contracts, Contracts.IDcontracts)).scalar_one()

        db_session.commit()
        return render_template(
            "sheff_org_contracts.html",
            contracts=contracts,
            count=count,
            page=0,
            function="applyContractsFilters"
        )
    if request.method == "POST":
        select = get_select()
        db_session = get_session()
        idorg = session["user"][0]
        page = (request.form.get("page") and int(request.form.get("page"))) or 0
        select_contracts = (
            select(Contracts)
            .filter(Contracts.IDorg == idorg)
            .order_by(Contracts.contractsNumber, Contracts.contractsStart)
        )
        contracts = db_session.execute(pagination(select_contracts)).all()
        count = db_session.execute(count_records(select_contracts, Contracts.IDcontracts)).scalar_one()

        db_session.commit()
        return render_template(
            "resultTableContracts.html",
            contracts=contracts,
            count=count,
            page=page,
            function="applyContractsFilters"
        )


@pages.route("/shefforg/mailadmin", methods=["GET", "POST"])
def sheff_org_mailadmin():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
        select_admins = (
            select(Sheffofprojects)
            .filter(Sheffofprojects.IDpositions == 1)
            .order_by(Sheffofprojects.FullName)
        )
        admins = db_session.execute(select_admins).all()

        db_session.commit()
        return render_template("sheff_org_mail_admin.html", admins=admins)


@pages.route("/shefforg/iniciators", methods=["GET", "POST"])  # Инициаторы проектов
def sheff_org_iniciators():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
        idorg = session["user"][0]
        select_inicators = (
            select(Initiatorsofprojects)
            .filter(Initiatorsofprojects.IDorg == idorg)
            .order_by(Initiatorsofprojects.FullName)
        )
        inic = db_session.execute(select_inicators).all()
        db_session.commit()
        return render_template("iniciators.html", inic=inic)
    if request.method == "POST":
        select = get_select()
        db_session = get_session()
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
        inic = db_session.execute(select_inicators).all()
        db_session.commit()
        return render_template("resultTableInic.html", inic=inic)


@pages.route("/shefforg/addIniciators", methods=["POST"])  # Добавить инициатора проектов
def sheff_org_addiniciators():
    db_session = get_session()
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
    db_session.add(add)
    db_session.commit()
    return redirect("/shefforg/iniciators")


@pages.route("/shefforg/deliniciators", methods=["POST"])  # удалить инициатора проектов
def deliniciators():
    id_sotr = int(request.form["delin"])
    db_session = get_session()
    db_session.query(Initiatorsofprojects).filter(
        Initiatorsofprojects.IDinitpr == id_sotr
    ).delete()
    db_session.commit()
    return redirect("/shefforg/iniciators")


@pages.route("/shefforg/redinitiators", methods=["POST"])  # Редактировать инициатора проектов
def sheff_org_redinitiators():
    db_session = get_session()
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
        db_session.query(Initiatorsofprojects)
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
    db_session.commit()
    return redirect("/shefforg/iniciators")


@pages.route("/admin/csvInic", methods=["POST"])
def insert_csv_inic():
    try:
        upload_file = request.files.get("file")
        file_path = path.join("documents", upload_file.filename)
        upload_file.save(file_path)
        with open(file_path, encoding="utf-8") as file:
            db_session = get_session()
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
                db_session.add(add)
                db_session.commit()
        return "", 200
    finally:
        remove(file_path)


# Проекты
@pages.route("/iniciators/projects", methods=["GET", "POST"])
def iniciators_project():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
        idinitpr = session["user"][1]
        select_stadia = select(StadiaOfProjects).order_by(StadiaOfProjects.IDstadiaofpr)
        select_projects = (
            select(
                Projects,
                PassportOfProjects,
                StadiaOfProjects,
                Initiatorsofprojects,
                Organizations,
                Sheffofprojects,
                Positions,
            )
            .join_from(
                Projects, PassportOfProjects, Projects.IDpassport == PassportOfProjects.IDpassport
            )
            .join(Sheffofprojects, isouter=True)
            .join(Positions, isouter=True)
            .join(Initiatorsofprojects)
            .join(StadiaOfProjects)
            .join(Organizations)
            .filter(PassportOfProjects.IDinitpr == idinitpr)
            .order_by(PassportOfProjects.passportName)
        )
        select_projects_count = (
            select(Projects)
            .join_from(
                Projects, PassportOfProjects, Projects.IDpassport == PassportOfProjects.IDpassport
            )
            .join(Sheffofprojects, isouter=True)
            .join(Positions, isouter=True)
            .join(Initiatorsofprojects)
            .join(StadiaOfProjects)
            .join(Organizations)
            .filter(PassportOfProjects.IDinitpr == idinitpr)
            .order_by(PassportOfProjects.passportName)
        )
        count_projects = db_session.execute(count_records(select_projects_count, Projects.IDprojects)).scalar_one()

        stadia = db_session.execute(select_stadia).all()
        projects = db_session.execute(pagination(select_projects)).all()
        projects_edit = db_session.execute(select_projects).all()
        db_session.commit()
        return render_template(
            "iniciators_projects.html",
            projects=projects,
            projects_edit=projects_edit,
            stadia=stadia,
            count=count_projects,
            page=0,
            function="applyProjectFilters",
        )
    if request.method == "POST":
        select = get_select()
        db_session = get_session()
        idinitpr = session["user"][1]
        project_filter = request.form["projectFilter"]
        stadia_filter = request.form["stadiaFilter"]
        sheff_proj_filter = request.form["sheffProjFilter"]
        page = (request.form.get("page") and int(request.form.get("page"))) or 0
        where_project_filter = (
            PassportOfProjects.passportName.ilike("%" + project_filter + "%")
            if project_filter
            else text("1=1")
        )
        where_stadia_filter = (
            StadiaOfProjects.IDstadiaofpr == stadia_filter if stadia_filter else text("1=1")
        )
        where_sheff_proj_filter = (
            Sheffofprojects.FullName.ilike("%" + sheff_proj_filter + "%")
            if sheff_proj_filter
            else text("1=1")
        )
        select_projects = (
            select(
                Projects,
                PassportOfProjects,
                StadiaOfProjects,
                Initiatorsofprojects,
                Organizations,
                Sheffofprojects,
                Positions,
            )
            .join_from(
                Projects, PassportOfProjects, Projects.IDpassport == PassportOfProjects.IDpassport
            )
            .join(Sheffofprojects, isouter=True)
            .join(Positions, isouter=True)
            .join(Initiatorsofprojects)
            .join(StadiaOfProjects)
            .join(Organizations)
            .where(where_project_filter)
            .where(where_stadia_filter)
            .where(where_sheff_proj_filter)
            .filter(PassportOfProjects.IDinitpr == idinitpr)
            .order_by(PassportOfProjects.passportName)
        )
        select_projects_count = (
            select(Projects)
            .join_from(
                Projects, PassportOfProjects, Projects.IDpassport == PassportOfProjects.IDpassport
            )
            .join(Sheffofprojects, isouter=True)
            .join(Positions, isouter=True)
            .join(Initiatorsofprojects)
            .join(StadiaOfProjects)
            .join(Organizations)
            .where(where_project_filter)
            .where(where_stadia_filter)
            .where(where_sheff_proj_filter)
            .filter(PassportOfProjects.IDinitpr == idinitpr)
        )

        count_projects = db_session.execute(count_records(select_projects_count, Projects.IDprojects)).scalar_one()
        projects = db_session.execute(pagination(select_projects, page)).all()
        db_session.commit()
        return render_template(
            "resultAccordionProjects.html",
            count=count_projects,
            page=page,
            projects=projects,
            function="applyProjectFilters",
        )


@pages.route("/iniciators/addProject", methods=["POST"])
def iniciators_add_project():
    db_session = get_session()
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
    db_session.add(add_passport)
    db_session.flush()
    idpassport = add_passport.IDpassport

    add_project = Projects(IDpassport=idpassport, IDstadiaofpr=1)
    db_session.add(add_project)
    db_session.commit()
    return redirect("/iniciators/projects")


@pages.route("/iniciators/modifyProject", methods=["POST"])
def iniciators_modify_project():
    db_session = get_session()
    idprojects = request.form["modifyProject"]
    project_name = request.form["projectName"]
    problem = request.form["problem"]
    purpose = request.form["purpose"]
    tasks = request.form["tasks"]
    result = request.form["result"]
    project = db_session.query(Projects).filter(Projects.IDprojects == idprojects).first()
    npr = (
        db_session.query(PassportOfProjects)
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

    db_session.commit()
    return redirect("/iniciators/projects")


@pages.route("/admin/projects", methods=["GET", "POST"])
def admin_project():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
        select_projects = (
            select(
                Projects,
                PassportOfProjects,
                StadiaOfProjects,
                Initiatorsofprojects,
                Organizations,
                Sheffofprojects,
                Positions,
            )
            .join_from(
                Projects, PassportOfProjects, Projects.IDpassport == PassportOfProjects.IDpassport
            )
            .join(Sheffofprojects, isouter=True)
            .join(Positions, isouter=True)
            .join(Initiatorsofprojects)
            .join(StadiaOfProjects)
            .join(Organizations)
            .order_by(PassportOfProjects.passportName)
        )
        select_stadia = select(StadiaOfProjects).order_by(StadiaOfProjects.IDstadiaofpr)
        count_projects = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        projects = db_session.execute(pagination(select_projects)).all()
        stadia = db_session.execute(select_stadia).all()
        db_session.commit()
        return render_template("projects.html", projects=projects, stadia=stadia, count=count_projects, page=0, function="applyProjectFilters")
    if request.method == "POST":
        select = get_select()
        db_session = get_session()
        project_filter = request.form["projectFilter"]
        stadia_filter = request.form["stadiaFilter"]
        org_filter = request.form["orgFilter"]
        inic_filter = request.form["inicFilter"]
        sheffproj_filter = request.form["sheffProjFilter"]
        page = (request.form.get("page") and int(request.form.get("page"))) or 0

        where_project_filter = (
            PassportOfProjects.passportName.ilike("%" + project_filter + "%")
            if project_filter
            else text("1=1")
        )
        where_stadia_filter = (
            StadiaOfProjects.IDstadiaofpr == stadia_filter if stadia_filter else text("1=1")
        )
        where_org_filter = (
            Organizations.orgName.ilike("%" + org_filter + "%") if org_filter else text("1=1")
        )
        where_inic_filter = (
            Initiatorsofprojects.FullName.ilike("%" + inic_filter + "%")
            if inic_filter
            else text("1=1")
        )
        where_sheffproj_filter = (
            Sheffofprojects.FullName.ilike("%" + sheffproj_filter + "%")
            if sheffproj_filter
            else text("1=1")
        )
        select_projects = (
            select(
                Projects,
                PassportOfProjects,
                StadiaOfProjects,
                Initiatorsofprojects,
                Organizations,
                Sheffofprojects,
                Positions,
            )
            .join_from(
                Projects, PassportOfProjects, Projects.IDpassport == PassportOfProjects.IDpassport
            )
            .join(Sheffofprojects, isouter=True)
            .join(Positions, isouter=True)
            .join(Initiatorsofprojects)
            .join(StadiaOfProjects)
            .join(Organizations)
            .where(where_org_filter)
            .where(where_inic_filter)
            .where(where_sheffproj_filter)
            .where(where_project_filter)
            .where(where_stadia_filter)
            .order_by(PassportOfProjects.passportName)
        )
        count_projects = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        projects = db_session.execute(pagination(select_projects, page)).all()
        db_session.commit()
        return render_template("resultAccordionProjects.html", projects=projects, count=count_projects, page=page, function="applyProjectFilters")


@pages.route("/checkStadia", methods=["GET"])
def check_stadia():
    idproject = int(request.args.get("idProject"))
    db_session = get_session()
    select = get_select()
    select_project = select(Projects).filter(Projects.IDprojects == idproject)
    project = db_session.execute(select_project).first()
    if project[0].IDstadiaofpr < 3:
        stadia = db_session.execute(
            select(StadiaOfProjects.IDstadiaofpr, StadiaOfProjects.stadiaofprName)
            .filter(StadiaOfProjects.IDstadiaofpr < 3)
            .order_by(StadiaOfProjects.IDstadiaofpr)
        ).all()
        return jsonify([dict(row._mapping) for row in stadia]), 200
    stadia = db_session.execute(
        select(StadiaOfProjects.IDstadiaofpr, StadiaOfProjects.stadiaofprName).filter(
            StadiaOfProjects.IDstadiaofpr == project[0].IDstadiaofpr
        )
    ).first()
    return jsonify(dict(stadia._mapping)), 200


@pages.route("/admin/addProject", methods=["POST"])
def admin_add_project():
    db_session = get_session()
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
    db_session.add(add_passport)
    db_session.flush()
    idpassport = add_passport.IDpassport

    add_project = Projects(IDpassport=idpassport, IDstadiaofpr=1)
    db_session.add(add_project)
    db_session.commit()
    return redirect("/admin/projects")


@pages.route("/admin/modifyProject", methods=["POST"])
def admin_modify_project():
    db_session = get_session()
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
    project = db_session.query(Projects).filter(Projects.IDprojects == idprojects).first()
    npr = (
        db_session.query(PassportOfProjects)
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
    db_session.commit()
    return redirect("/admin/projects")


@pages.route("/admin/deleteProject", methods=["POST"])  # удалить инициатора проектов
def admin_delete_project():
    idproject = int(request.form["deleteProject"])
    db_session = get_session()
    db_session.query(PassportOfProjects).filter(
        PassportOfProjects.IDpassport == idproject
    ).delete()
    db_session.commit()
    return redirect("/admin/projects")


@pages.route("/getPassport", methods=["GET"])
def get_passport():
    args = request.args
    idpassport = args.get("idPassport")

    db_session = get_session()
    select = get_select()

    select_passport = (
        select(PassportOfProjects, Initiatorsofprojects, Organizations, Sheffofprojects, Positions)
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
        .join(Sheffofprojects)
        .join(Positions)
        .filter(PassportOfProjects.IDpassport == idpassport)
    )
    record = db_session.execute(select_passport).first()
    if not record:
        return
    splitted_fio = record.Initiatorsofprojects.FullName.split(" ")
    if len(splitted_fio) == 3:
        init_fio = splitted_fio[1][0] + ". " + splitted_fio[2][0] + ". " + splitted_fio[0]
    splitted_shelf_fio = record.Sheffofprojects.FullName.split(" ")
    if len(splitted_shelf_fio) == 3:
        init_sheff_fio = (
            splitted_shelf_fio[1][0]
            + ". "
            + splitted_shelf_fio[2][0]
            + ". "
            + splitted_shelf_fio[0]
        )
    context = {}
    context["passport_name"] = record.PassportOfProjects.passportName
    context["fio"] = record.Initiatorsofprojects.FullName
    context["initFio"] = init_fio
    context["fio_sheff"] = init_sheff_fio
    context["pos_sheff"] = record.Positions.positionsName
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

    select_roles = (
        select(RolesOfProjects, Specializations, Competensions)
        .join_from(
            RolesOfProjects,
            SpecializationInProjects,
            RolesOfProjects.IDroles == SpecializationInProjects.IDroles,
            isouter=True,
        )
        .join(Specializations)
        .join(CompetensionsInProject)
        .join(Competensions)
        .filter(RolesOfProjects.IDpassport == idpassport)
    )
    roles = db_session.execute(
        text(
            r"""SELECT
	rolesofprojects.rolesRole,
	rolesofprojects.rolesAmount,
	rolesofprojects.rolesFunction,
	GROUP_CONCAT( distinct CONCAT_WS(' ', specializations.specShifr, specializations.specNapravlenie, specializations.specNapravlennost) order by 1 asc SEPARATOR '\n'),
    rolesofprojects.rolesCost,
    GROUP_CONCAT(distinct CONCAT_WS(' - ', competensions.competensionsShifr, competensions.competensionsFull) order by 1 asc SEPARATOR '\n'),
	rolesofprojects.rolesRequirements
FROM
	rolesofprojects
LEFT OUTER JOIN specializationsinprojects ON
	rolesofprojects.IDroles = specializationsinprojects.IDroles
JOIN specializations ON
	specializations.IDspec = specializationsinprojects.IDspec
JOIN competensionsinproject ON
	rolesofprojects.IDroles = competensionsinproject.IDroles
JOIN competensions ON
	competensions.IDcompetensions = competensionsinproject.IDcompetensions
WHERE
	rolesofprojects.IDpassport = :idpassport
group by 1,2,3,5,7"""
        ),
        {"idpassport": idpassport},
    ).all()
    if len(roles) > 0:
        context["roles"] = roles
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

    db_session = get_session()
    passport = (
        db_session.query(PassportOfProjects)
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

    db_session = get_session()
    passport = (
        db_session.query(PassportOfProjects)
        .filter(PassportOfProjects.IDpassport == idpassport)
        .first()
    )
    passport.passportSigned = file_path
    db_session.commit()

    upload_file.save(file_path)

    project = db_session.query(Projects).filter(Projects.IDpassport == passport.IDpassport).first()

    db_session.commit()
    return render_template(
        "documents_template.html",
        idpass=passport.IDpassport,
        signed=passport.passportSigned,
        stadia=project.IDstadiaofpr,
    )


# удалить подписанный договор
@pages.route("/deletePassportSigned", methods=["POST"])
def delete_passport():
    idpassport = request.form.get("idPassport")
    if not idpassport:
        return

    db_session = get_session()
    passport = (
        db_session.query(PassportOfProjects)
        .filter(PassportOfProjects.IDpassport == idpassport)
        .first()
    )
    passport.passportSigned = ""
    db_session.commit()

    project = db_session.query(Projects).filter(Projects.IDpassport == passport.IDpassport).first()

    db_session.commit()
    return render_template(
        "documents_template.html",
        idpass=passport.IDpassport,
        signed=passport.passportSigned,
        stadia=project.IDstadiaofpr,
    )


@pages.route("/iniciators/mailadmin", methods=["GET", "POST"])
def iniciators_org_mailadmin():
    return sheff_org_mailadmin()


@pages.route("/sheffproj/mailadmin", methods=["GET", "POST"])
def sheffproj_mailadmin():
    return sheff_org_mailadmin()


@pages.route("/student/mailadmin", methods=["GET", "POST"])
def student_mailadmin():
    return sheff_org_mailadmin()


@pages.route("/sheffproj/projects", methods=["GET", "POST"])
def sheffproj_projects():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
        idsheffpr = session["user"][0]
        select_projects = (
            select(
                Projects,
                PassportOfProjects,
                StadiaOfProjects,
                Initiatorsofprojects,
                Organizations,
                Sheffofprojects,
                Positions,
            )
            .join_from(
                Projects, PassportOfProjects, Projects.IDpassport == PassportOfProjects.IDpassport
            )
            .join(Sheffofprojects, isouter=True)
            .join(Positions, isouter=True)
            .join(Initiatorsofprojects)
            .join(StadiaOfProjects)
            .join(Organizations)
            .filter(PassportOfProjects.IDsheffpr == idsheffpr)
            .order_by(PassportOfProjects.passportName)
        )
        projects_assign = db_session.execute(
            select(Projects, PassportOfProjects)
            .join_from(
                Projects, PassportOfProjects, Projects.IDpassport == PassportOfProjects.IDpassport
            )
            .filter(PassportOfProjects.IDsheffpr == None)
            .order_by(PassportOfProjects.passportName)
        ).all()
        count_projects = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        projects = db_session.execute(pagination(select_projects)).all()
        projects_edit = db_session.execute(select_projects).all()
        stadia = db_session.query(StadiaOfProjects).filter(StadiaOfProjects.IDstadiaofpr > 2).all()
        stadia_filter = db_session.execute(select(StadiaOfProjects)).all()
        db_session.commit()
        return render_template(
            "sheffproj_projects.html",
            projects=projects,
            projects_assign=projects_assign,
            stadia=stadia,
            projects_edit=projects_edit,
            stadia_filter=stadia_filter,
            count=count_projects,
            page=0,
            function="applyProjectFilters"
        )
    if request.method == "POST":
        select = get_select()
        db_session = get_session()
        idsheffpr = session["user"][0]
        project_filter = request.form.get("projectFilter")
        org_filter = request.form.get("orgFilter")
        fio_init_filter = request.form.get("fioInitFilter")
        stadia_filter = request.form.get("stadiaFilter")
        page = (request.form.get("page") and int(request.form.get("page"))) or 0
        where_stadia_filter = (
            StadiaOfProjects.IDstadiaofpr == stadia_filter if stadia_filter else text("1=1")
        )
        where_project_filter = (
            PassportOfProjects.passportName.ilike("%" + project_filter + "%")
            if project_filter
            else text("1=1")
        )
        where_org_filter = (
            Organizations.orgName.ilike("%" + org_filter + "%") if org_filter else text("1=1")
        )

        where_fio_init_filter = (
            Initiatorsofprojects.FullName.ilike("%" + fio_init_filter + "%")
            if fio_init_filter
            else text("1=1")
        )
        select_projects = (
            select(
                Projects,
                PassportOfProjects,
                StadiaOfProjects,
                Initiatorsofprojects,
                Organizations,
                Sheffofprojects,
                Positions,
            )
            .join_from(
                Projects, PassportOfProjects, Projects.IDpassport == PassportOfProjects.IDpassport
            )
            .join(Sheffofprojects, isouter=True)
            .join(Positions, isouter=True)
            .join(Initiatorsofprojects)
            .join(StadiaOfProjects)
            .join(Organizations)
            # .filter(StadiaOfProjects.IDstadiaofpr == 3)
            .filter(where_stadia_filter)
            .filter(PassportOfProjects.IDsheffpr == idsheffpr)
            .filter(where_project_filter)
            .filter(where_fio_init_filter)
            .filter(where_org_filter)
            .order_by(PassportOfProjects.passportName)
        )

        count_projects = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        projects = db_session.execute(pagination(select_projects, page)).all()
        db_session.commit()
        return render_template("resultAccordionProjects.html", projects=projects, count=count_projects, page=page, function="applyProjectFilters")


@pages.route("/sheffproj/modifyProject", methods=["POST"])
def sheffproj_modify_project():
    db_session = get_session()
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
    project = db_session.query(Projects).filter(Projects.IDprojects == idprojects).first()
    npr = (
        db_session.query(PassportOfProjects)
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
    db_session.commit()
    return redirect("/admin/projects")


@pages.route("/sheffproj/assignment", methods=["GET", "POST"])
def sheffproj_assignment_project():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
        select_projects = (
            select(
                Projects,
                PassportOfProjects,
                StadiaOfProjects,
                Initiatorsofprojects,
                Organizations,
                Sheffofprojects,
                Positions,
            )
            .join_from(
                Projects, PassportOfProjects, Projects.IDpassport == PassportOfProjects.IDpassport
            )
            .join(Sheffofprojects, isouter=True)
            .join(Positions, isouter=True)
            .join(Initiatorsofprojects)
            .join(StadiaOfProjects)
            .join(Organizations)
            .filter(StadiaOfProjects.IDstadiaofpr == 2)
            .filter(PassportOfProjects.IDsheffpr == None)
            .order_by(PassportOfProjects.passportName)
        )
        count_projects = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        projects = db_session.execute(pagination(select_projects)).all()
        db_session.commit()
        return render_template(
            "sheffproj_assignment.html", projects=projects, count=count_projects, page=0, function='dropAssignProjectFilter'
        )
    if request.method == "POST":
        select = get_select()
        db_session = get_session()
        project_filter = request.form.get("projectFilter")
        org_filter = request.form.get("orgFilter")
        fio_init_filter = request.form.get("fioInitFilter")
        page = (request.form.get("page") and int(request.form.get("page"))) or 0
        where_project_filter = (
            PassportOfProjects.passportName.ilike("%" + project_filter + "%")
            if project_filter
            else text("1=1")
        )
        where_org_filter = (
            Organizations.orgName.ilike("%" + org_filter + "%") if org_filter else text("1=1")
        )

        where_fio_init_filter = (
            Initiatorsofprojects.FullName.ilike("%" + fio_init_filter + "%")
            if fio_init_filter
            else text("1=1")
        )
        select_projects = (
            select(
                Projects,
                PassportOfProjects,
                StadiaOfProjects,
                Initiatorsofprojects,
                Organizations,
                Sheffofprojects,
                Positions,
            )
            .join_from(
                Projects, PassportOfProjects, Projects.IDpassport == PassportOfProjects.IDpassport
            )
            .join(Sheffofprojects, isouter=True)
            .join(Positions, isouter=True)
            .join(Initiatorsofprojects)
            .join(StadiaOfProjects)
            .join(Organizations)
            .filter(StadiaOfProjects.IDstadiaofpr == 2)
            .filter(PassportOfProjects.IDsheffpr == None)
            .filter(where_project_filter)
            .filter(where_fio_init_filter)
            .filter(where_org_filter)
            .order_by(PassportOfProjects.passportName)
        )

        count_projects = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        projects = db_session.execute(pagination(select_projects)).all()
        db_session.commit()
        return render_template("resultAccordionProjects.html", projects=projects, count=count_projects, page=page, function='dropAssignProjectFilter')


@pages.route("/sheffproj/assignSheffProj", methods=["POST"])
def assign_sheff_proj_project():
    if request.method == "POST":
        db_session = get_session()
        idproject = request.form["project"]

        project = db_session.query(Projects).filter(Projects.IDprojects == idproject).first()
        npr = (
            db_session.query(PassportOfProjects)
            .filter(PassportOfProjects.IDpassport == project.IDpassport)
            .first()
        )
        npr.IDsheffpr = session["user"][0]
        project.IDstadiaofpr = 3
        db_session.commit()
        return redirect("/sheffproj/assignment")


@pages.route("/admin/stadia", methods=["GET"])
def admin_stadia():
    if request.method == "GET":
        db_session = get_session()
        select = get_select()
        select_projects = (
            select(Projects, PassportOfProjects, StadiaOfProjects)
            .join(PassportOfProjects)
            .join(StadiaOfProjects)
            .filter(StadiaOfProjects.IDstadiaofpr == 1)
            .order_by(PassportOfProjects.passportName)
        )
        projects = db_session.execute(select_projects).all()
        db_session.commit()
        return render_template("stadia.html", projects=projects)


@pages.route("/admin/changeStadia", methods=["POST"])
def admin_change_stadia():
    if request.method == "POST":
        db_session = get_session()
        idproject = request.form["project"]

        project = db_session.query(Projects).filter(Projects.IDprojects == idproject).first()
        project.IDstadiaofpr = 2
        db_session.commit()
        return redirect("/admin/stadia")


@pages.route("/sheffproj/changeStatusProject", methods=["POST"])
def chage_status_project():
    if request.method == "POST":
        db_session = get_session()
        idproject = request.form["project"]
        stadia = request.form["stadia"]
        project = db_session.query(Projects).filter(Projects.IDprojects == idproject).first()
        project.IDstadiaofpr = stadia
        db_session.commit()
        return redirect("/sheffproj/projects")


@pages.route("/sheffproj/members", methods=["GET", "POST"])
def sheffproj_members():
    if request.method == "GET":
        db_session = get_session()
        select = get_select()
        idsheffpr = session["user"][0]
        select_projects = (
            select(
                PassportOfProjects.IDpassport, PassportOfProjects.passportName, Projects.IDprojects
            )
            .distinct()
            .join(Projects)
            .join(StudentsInProjects)
            .filter(PassportOfProjects.IDsheffpr == idsheffpr)
        )
        select_roles = (
            select(RolesOfProjects)
            .join(PassportOfProjects)
            .filter(PassportOfProjects.IDsheffpr == idsheffpr)
        )
        roles = db_session.execute(select_roles).all()
        count_projects = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        projects = db_session.execute(pagination(select_projects)).all()
        groups = db_session.execute(select(Groups)).all()
        status = db_session.execute(select(StadiaOfWorks)).all()
        students = db_session.execute(
            text(
                r"""SELECT
        r.IDroles,
	CONCAT_WS(' ', students.studentsFirstname, students.studentsName, students.studentsFathername) AS anon_1,
	GROUP_CONCAT(DISTINCT CONCAT_WS(' - ', c2.competensionsShifr, c2.competensionsFull) order by 1 separator '<br>'),
	GROUP_CONCAT(distinct CONCAT(s2.specShifr, ' ', s2.specNapravlenie, ' - ', s2.specNapravlennost) order by 1 separator '<br>'),
	`groups`.groupsName,
    ss.IDstudentspr,
    ss.studentsinprFull,
    sow.stadiaofworksName
FROM
	students
JOIN studentsinprojects ss ON
	students.IDstudents = ss.IDstudents
join stadiaofworks sow on sow.idstadiaofworks = ss.idstadiaofworks
JOIN `groups` ON
	`groups`.IDgroups = students.IDgroups
JOIN projects ON
	projects.IDprojects = ss.IDprojects
JOIN passportofprojects ON
	passportofprojects.IDpassport = projects.IDpassport
join rolesofprojects r on
    r.idroles = ss.idroles
left join competensionsinproject c on
	c.IDroles = r.IDroles
left join competensions c2 on
	c2.IDcompetensions = c.IDcompetensions
left join specializationsinprojects s on
	s.IDroles  = r.IDroles
left join specializations s2 on
	s2.IDspec = s.IDspec
WHERE
	passportofprojects.IDsheffpr = :idsheffpr
group BY
	1, 2, 5, 6, 7, 8"""
            ),
            {"idsheffpr": idsheffpr},
        ).all()
        db_session.commit()
        return render_template(
            "sheffproj_members.html",
            students=students,
            projects=projects,
            roles=roles,
            groups=groups,
            status=status,
            count=count_projects,
            page=0,
            function='applyMembersFilters'
        )
    if request.method == "POST":
        db_session = get_session()
        select = get_select()
        fio_filter = request.form["projectFioFilter"]
        role_filter = request.form["projectRoleFilter"]
        napr_filter = request.form["projectNaprFilter"]
        group_filter = request.form["groupFilter"]
        status_filter = request.form["statusFilter"]
        page = (request.form.get("page") and int(request.form.get("page"))) or 0

        idsheffpr = session["user"][0]
        params = {"idsheffpr": idsheffpr}
        where_fio_filter = (
            text(
                "lower(concat_ws(' ', students.studentsFirstname, students.studentsName, students.studentsFathername)) LIKE lower(:fio_filter)"
            )
            if fio_filter
            else text("1=1")
        )
        where_role_filter = (
            RolesOfProjects.rolesRole.ilike("%" + role_filter + "%") if role_filter else text("1=1")
        )
        where_napr_filter = (
            text(
                "lower(concat_ws(' ', specializations.specShifr, specializations.specNapravlenie, specializations.specNapravlennost)) LIKE lower(:role_filter)"
            )
            if napr_filter
            else text("1=1")
        )
        where_group_filter = text("`groups`.idgroups = :idgroup") if group_filter else text("1=1")
        where_status_filter = (
            text("ss.idstadiaofworks = :idstatus") if status_filter else text("1=1")
        )

        if fio_filter:
            params["fio_filter"] = "%" + fio_filter + "%"
        if napr_filter:
            params["napr_filter"] = "%" + napr_filter + "%"
        if group_filter:
            params["idgroup"] = group_filter
        if status_filter:
            params["idstatus"] = status_filter

        select_projects = (
            select(
                PassportOfProjects.IDpassport, PassportOfProjects.passportName, Projects.IDprojects
            )
            .distinct()
            .join(Projects)
            .join(StudentsInProjects)
            .filter(PassportOfProjects.IDsheffpr == idsheffpr)
        )
        select_roles = (
            select(RolesOfProjects)
            .join(PassportOfProjects)
            .filter(PassportOfProjects.IDsheffpr == idsheffpr)
            .filter(where_role_filter)
        )
        roles = db_session.execute(select_roles).all()
        count_projects = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        projects = db_session.execute(pagination(select_projects)).all()
        students = db_session.execute(
            text(
                rf"""SELECT
        r.IDroles,
	CONCAT_WS(' ', students.studentsFirstname, students.studentsName, students.studentsFathername) AS anon_1,
	GROUP_CONCAT(DISTINCT CONCAT_WS(' - ', c2.competensionsShifr, c2.competensionsFull) order by 1 separator '<br>'),
	GROUP_CONCAT(distinct CONCAT(s2.specShifr, ' ', s2.specNapravlenie, ' - ', s2.specNapravlennost) order by 1 separator '<br>'),
	`groups`.groupsName,
    ss.IDstudentspr,
    ss.studentsinprFull,
    sow.stadiaofworksName
FROM
	students
JOIN studentsinprojects ss ON
	students.IDstudents = ss.IDstudents
join stadiaofworks sow on sow.idstadiaofworks = ss.idstadiaofworks
JOIN `groups` ON
	`groups`.IDgroups = students.IDgroups
JOIN projects ON
	projects.IDprojects = ss.IDprojects
JOIN passportofprojects ON
	passportofprojects.IDpassport = projects.IDpassport
join rolesofprojects r on
    r.idroles = ss.idroles
left join competensionsinproject c on
	c.IDroles = r.IDroles
left join competensions c2 on
	c2.IDcompetensions = c.IDcompetensions
left join specializationsinprojects s on
	s.IDroles  = r.IDroles
left join specializations s2 on
	s2.IDspec = s.IDspec
WHERE
	passportofprojects.IDsheffpr = :idsheffpr
    and {where_fio_filter}
    and {where_napr_filter}
    and {where_group_filter}
    and {where_status_filter}
group BY 1, 2, 5, 6, 7, 8"""
            ),
            params,
        ).all()
        db_session.commit()
        return render_template(
            "resultAccordionMembers.html",
            students=students,
            projects=projects,
            roles=roles,
            count=count_projects,
            page=page,
            function='applyMembersFilters'
        )


@pages.route("/admin/mailSheffOrg", methods=["GET"])
def admin_mail_shefforg():
    if request.method == "GET":
        db_session = get_session()
        select = get_select()
        select_projects = select(
            Initiatorsofprojects.IDorg, PassportOfProjects.passportName
        ).join_from(
            PassportOfProjects,
            Initiatorsofprojects,
            Initiatorsofprojects.IDinitpr == PassportOfProjects.IDinitpr,
        )
        projects = db_session.execute(select_projects).all()
        filter_shefforg = Organizations.IDorg == projects[0][0] if projects else text("1=1")
        select_shefforg = (
            select(
                Shefforganizations.shefforgEmail,
                Shefforganizations.shefforgPositions,
                Shefforganizations.FullName,
                Organizations.orgName,
            )
            .join(Organizations)
            .filter(filter_shefforg)
            .order_by(Shefforganizations.FullName)
        )
        shefforg = db_session.execute(select_shefforg).all()
        db_session.commit()
        return render_template("mail_shefforg.html", users=shefforg, projects=projects)


@pages.route("/iniciators/mailSheffOrg", methods=["GET"])
def iniciators_mail_shefforg():
    if request.method == "GET":
        db_session = get_session()
        select = get_select()
        idorg = session["user"][0]
        select_shefforg = (
            select(
                Shefforganizations.shefforgEmail,
                Shefforganizations.shefforgPositions,
                Shefforganizations.FullName,
                Organizations.orgName,
            )
            .join(Organizations)
            .filter(Organizations.IDorg == idorg)
            .order_by(Shefforganizations.FullName)
        )
        shefforg = db_session.execute(select_shefforg).all()
        db_session.commit()
        return render_template("mail_shefforg.html", users=shefforg)


@pages.route("/getSheffOrgMail", methods=["GET"])
def get_shefforg_mail():
    idorg = request.args.get("idOrg")
    db_session = get_session()
    select = get_select()
    select_shefforg = (
        select(
            Shefforganizations.shefforgEmail,
            Shefforganizations.shefforgPositions,
            Shefforganizations.FullName,
            Organizations.orgName,
        )
        .join(Organizations)
        .filter(Organizations.IDorg == idorg)
        .order_by(Shefforganizations.FullName)
    )
    shefforg = db_session.execute(select_shefforg).all()

    return jsonify([list(val) for val in shefforg]), 200


@pages.route("/admin/mail_inic", methods=["GET"])
def admin_mail_inic():
    if request.method == "GET":
        db_session = get_session()
        select = get_select()
        select_projects = select(PassportOfProjects.IDinitpr, PassportOfProjects.passportName)
        projects = db_session.execute(select_projects).all()
        filter_inic = Initiatorsofprojects.IDinitpr == projects[0][0] if projects else text("1=1")
        select_iniciators = (
            select(
                Initiatorsofprojects.initprEmail,
                Initiatorsofprojects.initprPositions,
                Initiatorsofprojects.FullName,
                Organizations.orgName,
            )
            .join(Organizations)
            .filter(filter_inic)
            .order_by(Initiatorsofprojects.FullName)
        )
        iniciators = db_session.execute(select_iniciators).all()
        db_session.commit()
        return render_template("mail_inic.html", users=iniciators, projects=projects)


@pages.route("/getIniciatorMail", methods=["GET"])
def get_iniciator_mail():
    idinic = request.args.get("idInic")
    db_session = get_session()
    select = get_select()
    select_iniciators = (
        select(
            Initiatorsofprojects.initprEmail,
            Initiatorsofprojects.initprPositions,
            Initiatorsofprojects.FullName,
            Organizations.orgName,
        )
        .join(Organizations)
        .filter(Initiatorsofprojects.IDinitpr == idinic)
        .order_by(Initiatorsofprojects.FullName)
    )
    iniciators = db_session.execute(select_iniciators).all()

    return jsonify([list(val) for val in iniciators]), 200


@pages.route("/getCompetitionsSpec", methods=["GET"])
def get_competitions_spec():
    if request.method == "GET":
        db_session = get_session()
        select = get_select()
        idspec = request.args.get("id")
        select_spec = select(
            Competensions.IDcompetensions,
            Competensions.competensionsShifr,
            Competensions.competensionsFull,
        ).filter(Competensions.IDspec == idspec)
        spec = db_session.execute(select_spec).all()
        return jsonify([list(el) for el in spec]), 200


@pages.route("/shefforg/projects", methods=["GET", "POST"])
def shefforg_project():
    if request.method == "GET":
        idorg = session["user"][0]
        select = get_select()
        db_session = get_session()
        select_stadia = select(StadiaOfProjects).order_by(StadiaOfProjects.IDstadiaofpr)
        select_projects = (
            select(
                Projects,
                PassportOfProjects,
                StadiaOfProjects,
                Initiatorsofprojects,
                Organizations,
                Sheffofprojects,
                Positions,
            )
            .join_from(
                Projects, PassportOfProjects, Projects.IDpassport == PassportOfProjects.IDpassport
            )
            .join(Sheffofprojects, isouter=True)
            .join(Positions, isouter=True)
            .join(Initiatorsofprojects)
            .join(StadiaOfProjects)
            .join(Organizations)
            .filter(Initiatorsofprojects.IDorg == idorg)
            .order_by(PassportOfProjects.passportName)
        )
        stadia = db_session.execute(select_stadia).all()
        count_projects = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        projects = db_session.execute(pagination(select_projects)).all()
        db_session.commit()
        return render_template("sheff_org_projects.html", projects=projects, stadia=stadia, count=count_projects, page=0, function="applyProjectFilters")
    if request.method == "POST":
        idorg = session["user"][0]
        select = get_select()
        db_session = get_session()
        project_filter = request.form["projectFilter"]
        stadia_filter = request.form["stadiaFilter"]
        inic_filter = request.form["inicFilter"]
        sheff_proj_filter = request.form["sheffProjFilter"]
        page = (request.form.get("page") and int(request.form.get("page"))) or 0
        where_project_filter = (
            PassportOfProjects.passportName.ilike("%" + project_filter + "%")
            if project_filter
            else text("1=1")
        )
        where_stadia_filter = (
            StadiaOfProjects.IDstadiaofpr == stadia_filter if stadia_filter else text("1=1")
        )
        where_inic_filter = Initiatorsofprojects.FullName.ilike("%" + inic_filter + "%") if inic_filter else text("1=1")
        where_sheff_proj_filter = Sheffofprojects.FullName.ilike("%" + sheff_proj_filter + "%") if sheff_proj_filter else text("1=1")
        select_projects = (
            select(
                Projects,
                PassportOfProjects,
                StadiaOfProjects,
                Initiatorsofprojects,
                Organizations,
                Sheffofprojects,
                Positions,
            )
            .join_from(
                Projects, PassportOfProjects, Projects.IDpassport == PassportOfProjects.IDpassport
            )
            .join(Sheffofprojects, isouter=True)
            .join(Positions, isouter=True)
            .join(Initiatorsofprojects)
            .join(StadiaOfProjects)
            .join(Organizations)
            .filter(Initiatorsofprojects.IDorg == idorg)
            .filter(where_inic_filter)
            .filter(where_sheff_proj_filter)
            .filter(where_project_filter)
            .filter(where_stadia_filter)
            .order_by(PassportOfProjects.passportName)
        )
        count_projects = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        projects = db_session.execute(pagination(select_projects, page)).all()
        db_session.commit()
        return render_template("resultAccordionProjects.html", projects=projects, count=count_projects, page=page, function="applyProjectFilters")


@pages.route("/sheffproj/roles", methods=["GET", "POST"])
def sheffproj_roles():
    if request.method == "GET":
        db_session = get_session()
        select = get_select()
        idsheffpr = session["user"][0]
        select_projects = (
            select(
                PassportOfProjects.IDpassport, PassportOfProjects.passportName, Projects.IDprojects
            )
            .join(Projects)
            .filter(PassportOfProjects.IDsheffpr == idsheffpr)
        )
        roles = db_session.execute(
            text(
                """select	p.IDpassport,
		p2.IDprojects,
		p.passportName,
		r.IDroles,
		r.rolesRole,
		r.rolesFunction,
		r.rolesAmount,
		r.rolesCost,
		r.rolesRequirements,
		group_concat(distinct concat_ws(' ', s2.specShifr, s2.specNapravlenie, s2.specNapravlennost) order by 1 separator '<br>'),
 		group_concat(distinct concat_ws(' - ', c2.competensionsShifr, c2.competensionsFull) order by 1 separator '<br>')
from 	passportofprojects p
		inner join projects p2 on ( p2.IDpassport = p.idpassport )
		inner join rolesofprojects r on ( r.IDpassport = p.IDpassport  )
		left join specializationsinprojects s on ( s.IDroles = r.IDroles )
		left join specializations s2 on ( s2.IDspec = s.IDspec )
		left join competensionsinproject c on ( c.IDroles = r.IDroles )
		left join competensions c2 on ( c2.IDcompetensions = c.IDcompetensions )
where 	p.IDsheffpr = :idsheffpr
group by
		1, 2, 3,4,5,6,7,8,9"""
            ),
            {"idsheffpr": idsheffpr},
        ).all()
        projects_edit = db_session.execute(select_projects).all()
        project_filter = Projects.IDprojects == projects_edit[0][2] if projects_edit else text("1=1")
        select_roles = (
            select(
                RolesOfProjects.IDroles, RolesOfProjects.rolesRole, RolesOfProjects.rolesFunction
            )
            .join(PassportOfProjects)
            .join(Projects)
            .filter(project_filter)
        )
        projects = db_session.execute(pagination(select_projects)).all()
        count = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        roles_selected = db_session.execute(select_roles).all()
        check_spec = db_session.execute(select(Specializations)).all()
        db_session.commit()
        return render_template(
            "sheffproj_roles.html",
            projects_edit=projects_edit,
            projects=projects,
            roles=roles,
            check_spec=check_spec,
            roles_selected=roles_selected,
            count=count,
            page=0,
            function="applyRolesFilters"
        )
    if request.method == "POST":
        db_session = get_session()
        select = get_select()
        idsheffpr = session["user"][0]
        opop_filter = request.form.get("opopFilter")
        role_filter = request.form.get("projectRoleFilter")
        project_filter = request.form.get("projectFilter")
        page = (request.form.get("page") and int(request.form.get("page"))) or 0
        idsheffpr = session["user"][0]
        params = {"idsheffpr": idsheffpr}
        where_project_filter = (
            text("lower(p.passportName) LIKE lower(:project_filter)")
            if project_filter
            else text("1=1")
        )
        where_project_filter_proj = (
            PassportOfProjects.passportName.ilike('%' + project_filter + '%')
            if project_filter
            else text("1=1")
        )
        where_opop_filter = (
            text(
                "lower(concat_ws(' ', s2.specShifr, s2.specNapravlenie, s2.specNapravlennost)) LIKE lower(:opop_filter)"
            )
            if opop_filter
            else text("1=1")
        )
        project_role_filter = (
            text("lower(r.rolesRole) LIKE lower(:role_filter)") if role_filter else text("1=1")
        )
        if opop_filter:
            params["opop_filter"] = "%" + opop_filter + "%"
        if project_filter:
            params["project_filter"] = "%" + project_filter + "%"
        if role_filter:
            params["role_filter"] = "%" + role_filter + "%"
        select_projects = (
            select(
                PassportOfProjects.IDpassport, PassportOfProjects.passportName, Projects.IDprojects
            )
            .join(Projects)
            .filter(PassportOfProjects.IDsheffpr == idsheffpr)
            .filter(where_project_filter_proj)
        )
        roles = db_session.execute(
            text(
                f"""select	p.IDpassport,
		p2.IDprojects,
		p.passportName,
		r.IDroles,
		r.rolesRole,
		r.rolesFunction,
		r.rolesAmount,
		r.rolesCost,
		r.rolesRequirements,
		group_concat(distinct concat_ws(' ', s2.specShifr, s2.specNapravlenie, s2.specNapravlennost) order by 1 separator '<br>'),
 		group_concat(distinct concat_ws(' - ', c2.competensionsShifr, c2.competensionsFull) order by 1 separator '<br>')
from 	passportofprojects p
		inner join projects p2 on ( p2.IDpassport = p.idpassport )
		inner join rolesofprojects r on ( r.IDpassport = p.IDpassport  )
		left join specializationsinprojects s on ( s.IDroles = r.IDroles )
		left join specializations s2 on ( s2.IDspec = s.IDspec )
		left join competensionsinproject c on ( c.IDroles = r.IDroles )
		left join competensions c2 on ( c2.IDcompetensions = c.IDcompetensions )
where 	p.IDsheffpr = 2
        and {project_role_filter}
        and {where_opop_filter}
        and {where_project_filter}
group by
		1, 2, 3,4,5,6,7,8,9"""
            ),
            params,
        ).all()
        projects = db_session.execute(pagination(select_projects, page)).all()
        count = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        db_session.commit()
        return render_template(
            "resultAccordionRoles.html",
            projects=projects,
            roles=roles,
            page=page,
            count=count,
            function="applyRolesFilters"
        )


@pages.route("/sheffproj/addRole", methods=["POST"])
def sheffproj_add_role():
    db_session = get_session()
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
    db_session.add(add_role)
    db_session.flush()
    for idspec in idspecs:
        add_spec = SpecializationInProjects(IDroles=add_role.IDroles, IDspec=idspec)
        db_session.add(add_spec)
        db_session.flush()

    for idcomp in idcomps:
        add_comp = CompetensionsInProject(IDroles=add_role.IDroles, IDcompetensions=idcomp)
        db_session.add(add_comp)
        db_session.flush()

    db_session.commit()
    return redirect("/sheffproj/roles")


@pages.route("/sheffproj/modifyRole", methods=["POST"])
def sheffproj_modify_role():
    db_session = get_session()
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

    rop = db_session.execute(
        select(RolesOfProjects).filter(RolesOfProjects.IDroles == idrole)
    ).first()[0]

    if len(idspecs) != 0:
        db_session.query(SpecializationInProjects).filter(
            SpecializationInProjects.IDroles == idrole
        ).delete()

    for idspec in idspecs:
        add_spec = SpecializationInProjects(IDroles=idrole, IDspec=idspec)
        db_session.add(add_spec)
        db_session.flush()

    if len(idcomps) != 0:
        db_session.query(CompetensionsInProject).filter(
            CompetensionsInProject.IDroles == idrole
        ).delete()

    for idcomp in idcomps:
        add_comp = CompetensionsInProject(IDroles=idrole, IDcompetensions=idcomp)
        db_session.add(add_comp)
        db_session.flush()

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

    db_session.commit()
    return redirect("/sheffproj/roles")


@pages.route("/sheffproj/deleteRole", methods=["POST"])
def sheffproj_delete_role():
    db_session = get_session()
    idrole = request.form["idrole"]

    db_session.query(CompetensionsInProject).filter(
        CompetensionsInProject.IDroles == idrole
    ).delete()
    db_session.query(SpecializationInProjects).filter(
        SpecializationInProjects.IDroles == idrole
    ).delete()
    db_session.query(RolesOfProjects).filter(RolesOfProjects.IDroles == idrole).delete()
    db_session.commit()
    return redirect("/sheffproj/roles")


@pages.route("/student/participation_ticket", methods=["GET", "POST"])
def student_participation_ticket():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
        idgroup = session["user"][0]
        idstudent = session["user"][1]
        select_current_projects = db_session.execute(
            select(Applications.IDprojects).distinct().filter(Applications.IDstudents == idstudent)
        ).all()
        cur_proj = [value[0] for value in select_current_projects]

        select_projects = (
            select(
                Projects,
                PassportOfProjects,
                StadiaOfProjects,
                Initiatorsofprojects,
                Organizations,
                Sheffofprojects,
                Positions,
            )
            .distinct()
            .join_from(Projects, RolesOfProjects, Projects.IDpassport == RolesOfProjects.IDpassport)
            .join(
                SpecializationInProjects,
                RolesOfProjects.IDroles == SpecializationInProjects.IDroles,
            )
            .join(Groups, SpecializationInProjects.IDspec == Groups.IDspec)
            .join(PassportOfProjects, onclause=PassportOfProjects.IDpassport == Projects.IDpassport)
            .join(Sheffofprojects, isouter=True)
            .join(Positions, isouter=True)
            .join(Initiatorsofprojects)
            .join(Organizations)
            .join(StadiaOfProjects)
            .filter(Groups.IDgroups == idgroup)
            .filter(Projects.IDstadiaofpr == 3)
            .filter(Projects.IDprojects.notin_(cur_proj))
            .order_by(PassportOfProjects.passportName)
        )
        projects = db_session.execute(pagination(select_projects)).all()
        projects_count = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        first_project = projects[0] if projects else None
        roles = []
        if first_project:
            select_roles = (
                select(
                    RolesOfProjects.IDroles,
                    RolesOfProjects.rolesRole,
                    RolesOfProjects.rolesFunction,
                )
                .join(Applications, isouter=True)
                .filter(RolesOfProjects.IDpassport == first_project.PassportOfProjects.IDpassport)
                .filter(
                    (Applications.IDprojects.notin_(cur_proj)) | (Applications.IDprojects == None)
                )
                .filter((Applications.IDstudents != idstudent) | (Applications.IDstudents == None))
            )
            roles = db_session.execute(select_roles).all()
        db_session.commit()
        return render_template("student_partic_tickets.html", projects=projects, roles=roles, count=projects_count, page=0, function='applyProjectFilters')
    if request.method == "POST":
        select = get_select()
        db_session = get_session()
        idstudent = session["user"][1]
        idgroup = session["user"][0]
        project_filter = request.form["projectFilter"]
        org_filter = request.form["orgFilter"]
        inic_filter = request.form["inicFilter"]
        sheffproj_filter = request.form["sheffProjFilter"]
        page = (request.form.get("page") and int(request.form.get("page"))) or 0

        where_project_filter = (
            PassportOfProjects.passportName.ilike("%" + project_filter + "%")
            if project_filter
            else text("1=1")
        )
        where_org_filter = (
            Organizations.orgName.ilike("%" + org_filter + "%") if org_filter else text("1=1")
        )
        where_inic_filter = (
            Initiatorsofprojects.FullName.ilike("%" + inic_filter + "%")
            if inic_filter
            else text("1=1")
        )
        where_sheffproj_filter = (
            Sheffofprojects.FullName.ilike("%" + sheffproj_filter + "%")
            if sheffproj_filter
            else text("1=1")
        )
        select_current_projects = db_session.execute(
            select(Applications.IDprojects).distinct().filter(Applications.IDstudents == idstudent)
        ).all()
        cur_proj = [value[0] for value in select_current_projects]

        select_projects = (
            select(
                Projects,
                PassportOfProjects,
                StadiaOfProjects,
                Initiatorsofprojects,
                Organizations,
                Sheffofprojects,
                Positions,
            )
            .distinct()
            .join_from(Projects, RolesOfProjects, Projects.IDpassport == RolesOfProjects.IDpassport)
            .join(
                SpecializationInProjects,
                RolesOfProjects.IDroles == SpecializationInProjects.IDroles,
            )
            .join(Groups, SpecializationInProjects.IDspec == Groups.IDspec)
            .join(PassportOfProjects, onclause=PassportOfProjects.IDpassport == Projects.IDpassport)
            .join(Sheffofprojects, isouter=True)
            .join(Positions, isouter=True)
            .join(Initiatorsofprojects)
            .join(Organizations)
            .join(StadiaOfProjects)
            .join(
                Applications, onclause=RolesOfProjects.IDroles == Applications.IDroles, isouter=True
            )
            .filter(Groups.IDgroups == idgroup)
            .filter(Projects.IDstadiaofpr == 3)
            .filter(Projects.IDprojects.notin_(cur_proj))
            .where(where_project_filter)
            .where(where_org_filter)
            .where(where_inic_filter)
            .where(where_sheffproj_filter)
            .order_by(PassportOfProjects.passportName)
        )
        projects = db_session.execute(pagination(select_projects, page)).all()
        projects_count = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        db_session.commit()
        return render_template("resultAccordionProjects.html", projects=projects, count=projects_count, page=page, function='applyProjectFilters')


@pages.route("/getRolesProjects", methods=["GET"])
def get_roles_projects():
    args = request.args
    idproject = args.get("idProject")
    select = get_select()
    db_session = get_session()
    select_roles = (
        select(RolesOfProjects.IDroles, RolesOfProjects.rolesRole, RolesOfProjects.rolesFunction)
        .join(PassportOfProjects)
        .join(Projects)
        .filter(Projects.IDprojects == idproject)
    )
    roles = db_session.execute(select_roles).all()
    return jsonify([dict(row._mapping) for row in roles]), 200


@pages.route("/student/getRoles", methods=["GET"])
def student_get_roles():
    args = request.args
    idpassport = args.get("id")
    idstudent = session["user"][1]
    select = get_select()
    db_session = get_session()
    select_current_projects = db_session.execute(
        select(Applications.IDprojects).distinct().filter(Applications.IDstudents == idstudent)
    ).all()
    cur_proj = [value[0] for value in select_current_projects]
    select_roles = (
        select(RolesOfProjects.IDroles, RolesOfProjects.rolesRole, RolesOfProjects.rolesFunction)
        .join(Applications, isouter=True)
        .filter(RolesOfProjects.IDpassport == idpassport)
        .filter((Applications.IDprojects.notin_(cur_proj)) | (Applications.IDprojects == None))
        .filter((Applications.IDstudents != idstudent) | (Applications.IDstudents == None))
    )
    roles = db_session.execute(select_roles).all()
    return jsonify([dict(row._mapping) for row in roles]), 200


@pages.route("/student/addTicket", methods=["POST"])
def student_add_ticket():
    db_session = get_session()
    idproject = request.form["project"]
    idrole = request.form["role"]
    courseYear = session["user"][2]
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
        applicationApproved=0,
    )
    db_session.add(add_application)
    db_session.commit()

    return redirect("/student/participation_ticket")


@pages.route("/student/tickets", methods=["GET", "POST"])
def student_tickets():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
        idstudent = session["user"][1]
        select_applications = (
            select(Applications, PassportOfProjects, RolesOfProjects, Confirmation)
            .join_from(
                Applications, RolesOfProjects, RolesOfProjects.IDroles == Applications.IDroles
            )
            .join(Projects)
            .join(PassportOfProjects)
            .join(Confirmation, isouter=True)
            .filter(Applications.IDstudents == idstudent)
            .order_by(PassportOfProjects.passportName)
        )
        applications = db_session.execute(select_applications).all()
        db_session.commit()
        return render_template("student_tickets.html", applications=applications)
    if request.method == "POST":
        select = get_select()
        db_session = get_session()
        idstudent = session["user"][1]
        role_filter = request.form.get("roleFilter")
        project_name_filter = request.form.get("projectNameFilter")
        status_filter = request.form.get("statusFilter")

        where_project_filter = (
            PassportOfProjects.passportName.ilike("%" + project_name_filter + "%")
            if project_name_filter
            else text("1=1")
        )
        where_stage_filter = (
            Applications.applicationApproved == status_filter if status_filter else text("1=1")
        )
        where_role_filter = (
            RolesOfProjects.rolesRole.ilike("%" + role_filter + "%") if role_filter else text("1=1")
        )

        select_applications = (
            select(Applications, PassportOfProjects, RolesOfProjects, Confirmation)
            .join_from(
                Applications, RolesOfProjects, RolesOfProjects.IDroles == Applications.IDroles
            )
            .join(Projects)
            .join(PassportOfProjects)
            .join(Confirmation, isouter=True)
            .filter(Applications.IDstudents == idstudent)
            .filter(where_project_filter)
            .filter(where_stage_filter)
            .filter(where_role_filter)
            .order_by(PassportOfProjects.passportName)
        )
        applications = db_session.execute(select_applications).all()
        db_session.commit()
        return render_template("resultTableStudentTickets.html", applications=applications)


@pages.route("/student/modifyApplication", methods=["POST"])
def student_modify_application():
    if request.method == "POST":
        db_session = get_session()
        idapplication = request.form["application"]
        purpose = request.form["reason"]

        project = (
            db_session.query(Applications)
            .filter(Applications.IDapplications == idapplication)
            .first()
        )

        if str(purpose):
            project.applicationsPurpose = purpose
        db_session.commit()
        return redirect("/student/tickets")


@pages.route("/getApplication", methods=["GET"])
def send_application():
    args = request.args
    idapplication = args.get("idApplication")

    db_session = get_session()
    select = get_select()

    select = (
        select(Specializations, Students, Groups, PassportOfProjects, RolesOfProjects, Applications)
        .join_from(Applications, Projects, Projects.IDprojects == Applications.IDprojects)
        .join(RolesOfProjects)
        .join(SpecializationInProjects)
        .join(Specializations)
        .join(Students)
        .join(Groups)
        .filter(Applications.IDapplications == idapplication)
    )
    record = db_session.execute(select).first()
    if not record:
        return

    context = {}
    context["projectName"] = record.PassportOfProjects.passportName
    context["fio"] = record.Students.FullName
    context["opop"] = record.Specializations.FullSpec
    context["course"] = record.Applications.applicationsCourse
    context["group"] = record.Groups.groupsName
    context["role"] = record.RolesOfProjects.rolesRole
    context["reason"] = record.Applications.applicationsPurpose

    filename = (
        "Заявка на участие в проекте "
        + str(record.PassportOfProjects.passportName).replace('"', "")
        + " от "
        + context["fio"]
        + "_"
        + date.today().strftime("%d_%B_%Y")
        + ".doc"
    )
    file_path = path.join("documents", filename)
    doc = DocxTemplate("./documents/approve_template.docx")

    doc.render(context)

    doc.save(file_path)

    return send_file(file_path, mimetype="multipart/form-data", as_attachment=True)


@pages.route("/sheffproj/tickets", methods=["GET", "POST"])
def sheff_proj_tickets():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
        idsheff_proj = session["user"][0]
        select_applications = (
            select(
                Students, Groups, Specializations, RolesOfProjects, PassportOfProjects, Applications
            )
            .distinct()
            .join_from(
                Applications,
                Students,
                Students.IDstudents == Applications.IDstudents,
                isouter=True,
            )
            .join(RolesOfProjects)
            .join(Groups)
            .join(Projects)
            .join(PassportOfProjects)
            .join(Specializations)
            .filter(PassportOfProjects.IDsheffpr == idsheff_proj)
            .filter(Applications.applicationApproved == 0)
            .order_by(PassportOfProjects.passportName)
        )
        select_projects = (
            select(Projects, PassportOfProjects)
            .distinct()
            .join_from(
                Projects,
                PassportOfProjects,
                PassportOfProjects.IDpassport == Projects.IDpassport,
                isouter=True,
            )
            .join(Applications)
            .filter(PassportOfProjects.IDsheffpr == idsheff_proj)
            .filter(Applications.applicationApproved == 0)
        )
        groups = db_session.execute(select(Groups))
        projects = db_session.execute(pagination(select_projects)).all()
        count = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        applications = db_session.execute(select_applications).all()
        levels = db_session.execute((select(Levels))).all()
        db_session.commit()
        return render_template(
            "sheff_proj_tickets.html",
            projects=projects,
            tickets=applications,
            levels=levels,
            groups=groups,
            count=count,
            page=0,
            function="applyStudTicketsFilters"
        )
    if request.method == "POST":
        select = get_select()
        db_session = get_session()
        fio_filter = request.form["projectFioFilter"]
        project_filter = request.form["projectNameFilter"]
        group_filter = request.form["groupFilter"]
        page = (request.form.get("page") and int(request.form.get("page"))) or 0
        where_fio_filter = (
            Students.FullName.ilike("%" + fio_filter + "%") if fio_filter else text("1=1")
        )
        where_group_filter = Groups.IDgroups == group_filter if group_filter else text("1=1")
        where_project_filter = (
            PassportOfProjects.passportName.ilike("%" + project_filter + "%")
            if project_filter
            else text("1=1")
        )
        idsheff_proj = session["user"][0]
        select_applications = (
            select(
                Students, Groups, Specializations, RolesOfProjects, PassportOfProjects, Applications
            )
            .distinct()
            .join_from(
                Applications,
                Students,
                Students.IDstudents == Applications.IDstudents,
                isouter=True,
            )
            .join(RolesOfProjects)
            .join(Groups)
            .join(Projects)
            .join(PassportOfProjects)
            .join(Specializations)
            .filter(where_fio_filter)
            .filter(where_project_filter)
            .filter(where_group_filter)
            .filter(PassportOfProjects.IDsheffpr == idsheff_proj)
            .filter(Applications.applicationApproved == 0)
            .order_by(PassportOfProjects.passportName)
        )
        select_projects = (
            select(Projects, PassportOfProjects)
            .join_from(
                Projects,
                PassportOfProjects,
                PassportOfProjects.IDpassport == Projects.IDpassport,
                isouter=True,
            )
            .join(Applications)
            .filter(PassportOfProjects.IDsheffpr == idsheff_proj)
            .filter(Applications.applicationApproved == 0)
            .filter(where_project_filter)
        )
        projects = db_session.execute(pagination(select_projects, page)).all()
        count = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        applications = db_session.execute(select_applications).all()
        db_session.commit()
        return render_template(
            "resultAccordionStudentTickets.html", projects=projects, tickets=applications, count=count,
            page=page,
            function="applyStudTicketsFilters"
        )


@pages.route("/sheffproj/modifyApplication", methods=["POST"])
def sheff_proj_modify_applications():
    db_session = get_session()
    idapplication = request.form["application"]
    reason = request.form["reason"]
    record = (
        db_session.query(Applications).filter(Applications.IDapplications == idapplication).first()
    )
    if str(reason) != "":
        record.applicationsPurpose = reason
    db_session.commit()
    return redirect("/sheffproj/tickets")


@pages.route("/sheffproj/approveWork", methods=["POST"])
def sheff_proj_approve_work():
    db_session = get_session()
    idapplication = request.form["application"]
    lvl_comp = request.form["lvl_comp"]
    period = request.form["period"]
    results = request.form["results"]
    record = (
        db_session.query(Applications)
        .join(StudentsInProjects, onclause=StudentsInProjects.IDstudents == Applications.IDstudents)
        .filter(Applications.IDprojects == StudentsInProjects.IDprojects)
        .filter(Applications.IDroles == StudentsInProjects.IDroles)
        .filter(StudentsInProjects.IDstudentspr == idapplication)
        .first()
    )
    confirm = Confirmation(
        IDapplications=record.IDapplications,
        confirmationResults=results,
        confirmationPeriod=period,
        IDlevels=lvl_comp,
        confirmationPattern="",
        confirmationFull="",
    )
    db_session.add(confirm)
    db_session.commit()
    return redirect("/sheffproj/approved_tickets")


@pages.route("/sheffproj/approveTicket", methods=["POST"])
def sheff_proj_approve_ticket():
    db_session = get_session()
    idapplication = request.form["application"]
    record = (
        db_session.query(Applications).filter(Applications.IDapplications == idapplication).first()
    )
    record.applicationApproved = 1
    db_session.flush()

    add_student_proj = StudentsInProjects(
        IDstudents=record.IDstudents,
        IDprojects=record.IDprojects,
        IDroles=record.IDroles,
        IDstadiaofworks=1,
        IDapplications=idapplication,
    )
    db_session.add(add_student_proj)
    db_session.commit()
    return redirect("/sheffproj/tickets")


@pages.route("/sheffproj/declineApplication", methods=["POST"])
def sheff_proj_decline_applications():
    db_session = get_session()
    idapplication = request.form["application"]
    record = (
        db_session.query(Applications).filter(Applications.IDapplications == idapplication).first()
    )
    record.applicationApproved = 2
    db_session.commit()
    return redirect("/sheffproj/tickets")


@pages.route("/sheffproj/approved_tickets", methods=["GET", "POST"])
def sheff_proj_approved_tickets():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
        idsheff_proj = session["user"][0]
        select_projects = (
            select(
                PassportOfProjects.IDpassport, PassportOfProjects.passportName, Projects.IDprojects
            )
            .distinct()
            .join_from(
                Projects, StudentsInProjects, StudentsInProjects.IDprojects == Projects.IDprojects
            )
            .join(PassportOfProjects)
            .filter(PassportOfProjects.IDsheffpr == idsheff_proj)
        )
        count_projects = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        projects = db_session.execute(pagination(select_projects)).all()
        projects_filter = [val[0] for val in projects]
        select_approved = (
            select(
                Students,
                Groups,
                Levels,
                Specializations,
                Confirmation,
                RolesOfProjects,
                PassportOfProjects,
                StudentsInProjects,
                StadiaOfWorks,
            )
            .distinct()
            .join_from(
                StudentsInProjects, Students, Students.IDstudents == StudentsInProjects.IDstudents
            )
            .join(StadiaOfWorks)
            .join(RolesOfProjects)
            .join(
                Confirmation,
                isouter=True,
                onclause=StudentsInProjects.IDconfirmation == Confirmation.IDconfirmation,
            )
            .join(Levels, isouter=True)
            .join(Projects, onclause=StudentsInProjects.IDprojects == Projects.IDprojects)
            .join(PassportOfProjects)
            .join(Groups)
            .join(Specializations)
            .filter(PassportOfProjects.IDsheffpr == idsheff_proj)
            .filter(PassportOfProjects.IDpassport.in_(projects_filter))
            .order_by(PassportOfProjects.passportName)
        )
        approved = db_session.execute(select_approved).all()
        groups = db_session.execute(select(Groups))
        projects = db_session.execute(select_projects).all()
        levels = db_session.execute((select(Levels))).all()
        is_null = len([val for val in approved if val.Confirmation]) == 0
        is_not_confirmed_null = len([val for val in approved if not val.Confirmation]) == 0
        db_session.commit()
        return render_template(
            "sheff_proj_confirmed.html",
            projects=projects,
            approved=approved,
            levels=levels,
            groups=groups,
            is_null=is_null,
            count=count_projects,
            page=0,
            function="applyStudApprovedTicketsFilters",
            is_not_confirmed_null=is_not_confirmed_null
        )
    if request.method == "POST":
        select = get_select()
        db_session = get_session()
        fio_filter = request.form.get("projectFioFilter")
        project_filter = request.form.get("projectNameFilter")
        group_filter = request.form.get("groupFilter")
        page = (request.form.get("page") and int(request.form.get("page"))) or 0
        where_fio_filter = (
            Students.FullName.ilike("%" + fio_filter + "%") if fio_filter else text("1=1")
        )
        where_project_filter = (
            PassportOfProjects.passportName.ilike("%" + project_filter + "%")
            if project_filter
            else text("1=1")
        )
        where_group_filter = Groups.IDgroups == group_filter if group_filter else text("1=1")
        idsheff_proj = session["user"][0]
        select_projects = (
            select(
                PassportOfProjects.IDpassport, PassportOfProjects.passportName, Projects.IDprojects
            )
            .distinct()
            .join_from(
                Projects, StudentsInProjects, StudentsInProjects.IDprojects == Projects.IDprojects
            )
            .join(PassportOfProjects)
            .join(Students)
            .join(Groups)
            .filter(PassportOfProjects.IDsheffpr == idsheff_proj)
            .filter(where_group_filter)
            .filter(where_fio_filter)
            .filter(where_project_filter)
        )
        select_approved = (
            select(
                Students,
                Groups,
                Levels,
                Specializations,
                Confirmation,
                RolesOfProjects,
                PassportOfProjects,
                StudentsInProjects,
                StadiaOfWorks,
            )
            .distinct()
            .join_from(
                StudentsInProjects, Students, Students.IDstudents == StudentsInProjects.IDstudents
            )
            .join(StadiaOfWorks)
            .join(RolesOfProjects)
            .join(
                Confirmation,
                isouter=True,
                onclause=StudentsInProjects.IDconfirmation == Confirmation.IDconfirmation,
            )
            .join(Levels, isouter=True)
            .join(Projects, onclause=StudentsInProjects.IDprojects == Projects.IDprojects)
            .join(PassportOfProjects)
            .join(Groups)
            .join(Specializations)
            .filter(PassportOfProjects.IDsheffpr == idsheff_proj)
            .filter(where_fio_filter)
            .filter(where_project_filter)
            .filter(where_group_filter)
            .order_by(PassportOfProjects.passportName)
        )
        count_projects = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        projects = db_session.execute(pagination(select_projects, page)).all()
        approved = db_session.execute(select_approved).all()
        db_session.commit()
        return render_template(
            "resultAccordionStudentApprovedTickets.html",
            projects=projects,
            approved=approved,
            count=count_projects,
            page=page,
            function="applyStudApprovedTicketsFilters"
        )


@pages.route("/sheffproj/modifyConfirmation", methods=["POST"])
def sheff_proj_modify_confirmation():
    db_session = get_session()
    idconfirmation = request.form["application"]
    results = request.form.get("results")
    period = request.form.get("period")
    lvl_comp = request.form.get("lvl_comp")
    record = (
        db_session.query(Confirmation).filter(Confirmation.IDconfirmation == idconfirmation).first()
    )

    if str(results) != "":
        record.confirmationResults = results
    if str(period) != "":
        record.confirmationPeriod = period
    if str(lvl_comp) != "":
        record.IDlevels = lvl_comp

    db_session.commit()
    return redirect("/sheffproj/approved_tickets")


@pages.route("/sheffproj/declineConfirmation", methods=["POST"])
def sheff_proj_decline_confirmation():
    db_session = get_session()
    idconfirmation = request.form["confirmation"]
    db_session.query(StudentsInProjects).filter(
        StudentsInProjects.IDconfirmation == idconfirmation
    ).delete()
    confirm_record = (
        db_session.query(Confirmation).filter(Confirmation.IDconfirmation == idconfirmation).first()
    )
    db_session.query(Confirmation).filter(Confirmation.IDconfirmation == idconfirmation).delete()
    application_record = (
        db_session.query(Applications)
        .filter(Applications.IDapplications == confirm_record.IDapplications)
        .first()
    )
    application_record.applicationApproved = 2
    db_session.commit()
    return redirect("/sheffproj/approved_tickets")


@pages.route("/getConfirmation", methods=["GET"])
def send_confirmation():
    args = request.args
    idconfirmation = args.get("idConfirmation")

    db_session = get_session()
    confirmed_ticket = db_session.execute(
        text(
            r"""SELECT
	CONCAT_WS(' ', s.studentsFirstname, s.studentsName, s.studentsFathername) as fio,
	concat_ws(' ', s2.specShifr, s2.specNapravlenie, s2.specNapravlennost) as spec,
	year(CURDATE()) - g.groupsYear + 1,
	g.groupsName,
	p2.passportName,
	r.rolesRole,
	c.confirmationPeriod,
	r.rolesAmount,
	GROUP_CONCAT(distinct CONCAT_WS(' - ', c3.competensionsShifr, c3.competensionsFull) order by 1 asc SEPARATOR '\n'),
	c.confirmationResults,
	l.levelsName,
	CONCAT(SUBSTRING(s3.sheffprName,1, 1), '. ', SUBSTRING(s3.sheffprFathername, 1, 1), '. ', s3.sheffprFirstname),
	p3.positionsName
FROM
	confirmation c
	inner join applications a on ( a.IDapplications = c.IDapplications  )
	inner join rolesofprojects r on ( r.IDroles = a.IDroles  )
	inner join students s on ( s.IDstudents = a.IDstudents  )
	inner join `groups` g on ( g.IDgroups  = s.IDgroups  )
	inner join specializations s2 on ( s2.IDspec = g.IDspec  )
	inner join projects p on ( p.IDprojects = a.IDprojects )
	inner join competensionsinproject c2 on ( c2.IDroles = r.IDroles )
	inner join competensions c3 on ( c3.IDcompetensions = c2.IDcompetensions  )
	inner join passportofprojects p2 on ( p2.IDpassport = p.IDpassport )
	inner join levels l on ( l.IDlevels = c.IDlevels  )
	inner join sheffofprojects s3 on ( s3.IDsheffpr = p2.IDsheffpr )
	inner join positions p3 on ( p3.IDpositions = s3.IDpositions )
WHERE
	c.IDconfirmation = :idconf
group by 1,2,3,4,5,6,7,8,10,11, 12, 13"""
        ),
        {"idconf": idconfirmation},
    ).first()

    context = {}
    context["fio"] = confirmed_ticket[0]
    context["opop"] = confirmed_ticket[1]
    context["course"] = confirmed_ticket[2]
    context["group"] = confirmed_ticket[3]
    context["passportName"] = confirmed_ticket[4]
    context["role"] = confirmed_ticket[5]
    context["period"] = confirmed_ticket[6]
    context["amount"] = confirmed_ticket[7]
    context["comp"] = confirmed_ticket[8]
    context["result"] = confirmed_ticket[9]
    context["level"] = confirmed_ticket[10]
    context["fio_pr"] = confirmed_ticket[11]
    context["pos"] = confirmed_ticket[12]
    filename = (
        "Подтверждение участия в проекте "
        + str(context["passportName"]).replace('"', "")
        + " от "
        + context["fio"]
        + "_"
        + date.today().strftime("%d_%B_%Y")
        + ".doc"
    )
    file_path = path.join("documents", filename)
    doc = DocxTemplate("./documents/confirmed_template.docx")

    doc.render(context)

    doc.save(file_path)

    return send_file(file_path, mimetype="multipart/form-data", as_attachment=True)


@pages.route("/student/works", methods=["GET", "POST"])
def student_works():
    if request.method == "GET":
        idstudent = session["user"][1]
        db_session = get_session()
        select = get_select()
        select_projects = (
            select(Projects, PassportOfProjects)
            .join(StudentsInProjects)
            .join(PassportOfProjects)
            .filter(StudentsInProjects.IDstudents == idstudent)
        )
        select_works = (
            select(
                StudentsInProjects,
                Students,
                StadiaOfWorks,
                RolesOfProjects,
                Projects,
                PassportOfProjects,
                Applications,
            )
            .join_from(
                StudentsInProjects, Projects, StudentsInProjects.IDprojects == Projects.IDprojects
            )
            .join(Confirmation, isouter=True)
            .join(
                Applications,
                onclause=Applications.IDapplications == StudentsInProjects.IDapplications,
            )
            .join(PassportOfProjects, PassportOfProjects.IDpassport == Projects.IDpassport)
            .join(Students, onclause=Students.IDstudents == StudentsInProjects.IDstudents)
            .join(StadiaOfWorks)
            .join(RolesOfProjects, RolesOfProjects.IDroles == StudentsInProjects.IDroles)
            .filter(StudentsInProjects.IDstudents == idstudent)
        )

        projects = db_session.execute(pagination(select_projects)).all()
        count = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()

        works = db_session.execute(select_works).all()
        stage = db_session.execute(select(StadiaOfWorks)).all()

        db_session.commit()
        return render_template("student_works.html", projects=projects, works=works, stage=stage, count=count, page=0, function='applyStudentWorksFilter')
    if request.method == "POST":
        idstudent = session["user"][1]
        project_filter = request.form.get("projectFilter")
        stage_filter = request.form.get("stageFilter")
        role_filter = request.form.get("roleFilter")
        inic_filter = request.form.get("inicFilter")
        sheffproj_filter = request.form.get("sheffProjFilter")
        page = (request.form.get("page") and int(request.form.get("page"))) or 0
        db_session = get_session()
        select = get_select()
        where_project_filter = (
            PassportOfProjects.passportName.ilike("%" + project_filter + "%")
            if project_filter
            else text("1=1")
        )
        where_stage_filter = (
            StudentsInProjects.IDstadiaofworks == stage_filter if stage_filter else text("1=1")
        )
        where_role_filter = (
            RolesOfProjects.rolesRole.ilike("%" + role_filter + "%") if role_filter else text("1=1")
        )
        where_inic_filter = (
            Initiatorsofprojects.FullName.ilike("%" + inic_filter + "%")
            if inic_filter
            else text("1=1")
        )
        where_sheffproj_filter = (
            Sheffofprojects.FullName.ilike("%" + sheffproj_filter + "%")
            if sheffproj_filter
            else text("1=1")
        )

        select_projects = (
            select(Projects, PassportOfProjects)
            .join(StudentsInProjects)
            .join(PassportOfProjects)
            .filter(StudentsInProjects.IDstudents == idstudent)
            .filter(where_project_filter)
            .filter(where_stage_filter)
        )
        select_works = (
            select(
                StudentsInProjects,
                Students,
                StadiaOfWorks,
                RolesOfProjects,
                Projects,
                PassportOfProjects,
            )
            .join_from(
                StudentsInProjects, Projects, StudentsInProjects.IDprojects == Projects.IDprojects
            )
            .join(Confirmation, isouter=True)
            .join(
                Applications,
                onclause=Applications.IDapplications == StudentsInProjects.IDapplications,
            )
            .join(PassportOfProjects, PassportOfProjects.IDpassport == Projects.IDpassport)
            .join(Students, onclause=Students.IDstudents == StudentsInProjects.IDstudents)
            .join(StadiaOfWorks)
            .join(RolesOfProjects, RolesOfProjects.IDroles == StudentsInProjects.IDroles)
            .filter(StudentsInProjects.IDstudents == idstudent)
            .filter(where_project_filter)
            .filter(where_stage_filter)
            .filter(where_role_filter)
            .filter(where_inic_filter)
            .filter(where_sheffproj_filter)
        )
        projects = db_session.execute(pagination(select_projects, page)).all()
        count = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()

        works = db_session.execute(select_works).all()
        db_session.commit()
        return render_template("resultAccordionWorks.html", projects=projects, works=works, count=count, page=page, function='applyStudentWorksFilter')


@pages.route("/student/mailAnotherStudents", methods=["GET", "POST"])
def student_mail_students():
    if request.method == "GET":
        db_session = get_session()
        select = get_select()
        idstudent = session["user"][1]

        select_projects = (
            select(Projects.IDprojects, PassportOfProjects.passportName)
            .distinct()
            .join_from(
                PassportOfProjects, Projects, PassportOfProjects.IDpassport == Projects.IDpassport
            )
            .join(StudentsInProjects)
            .filter(StudentsInProjects.IDstudents == idstudent)
        )

        projects = db_session.execute(select_projects).all()
        idproj = projects[0][0] if projects else text("1=0")
        students = db_session.execute(
            text(
                """SELECT distinct
                CONCAT_WS(' ',s3.studentsFirstname, s3.studentsName, s3.studentsFathername),
                s3.studentsEmail,
                concat_ws(' - ', g.groupsname, concat(p3.rolesrole, ' - ', p3.rolesfunction))
        FROM	studentsinprojects s
                join projects p on ( p.IDprojects  = s.IDprojects )
                join passportofprojects p2 on ( p2.IDpassport = p.IDpassport )
                join studentsinprojects s2 on (s2.IDprojects = p.IDprojects)
                join rolesofprojects p3 on ( p3.idroles = s2.idroles )
                join students s3 on ( s3.IDstudents = s.IDstudents  )
                join `groups` g on ( g.idgroups = s3.idgroups )
        WHERE 	p.idprojects = :idproj
                and s.IDstudents = :idstudents
		        and s.IDstudents != s2.IDstudents"""
            ),
            {"idproj": idproj, "idstudents": idstudent},
        ).all()

        db_session.commit()
        return render_template("students_mail_student.html", users=students, projects=projects)


@pages.route("/student/mailIniciator", methods=["GET", "POST"])
def student_mail_iniciator():
    if request.method == "GET":
        db_session = get_session()
        select = get_select()
        idstudent = session["user"][1]
        select_projects = (
            select(PassportOfProjects.IDinitpr, PassportOfProjects.passportName)
            .join(Projects)
            .join(StudentsInProjects)
            .filter(StudentsInProjects.IDstudents == idstudent)
        )
        projects = db_session.execute(select_projects).all()
        filter_inic = Initiatorsofprojects.IDinitpr == projects[0][0] if projects else text("1=0")
        select_iniciators = (
            select(
                Initiatorsofprojects.initprEmail,
                Initiatorsofprojects.initprPositions,
                Initiatorsofprojects.FullName,
                Organizations.orgName,
            )
            .join(Organizations)
            .filter(filter_inic)
            .order_by(Initiatorsofprojects.FullName)
        )
        iniciators = db_session.execute(select_iniciators).all()
        db_session.commit()
        return render_template("students_mail_iniciator.html", users=iniciators, projects=projects)


@pages.route("/shefforg/mailIniciator", methods=["GET", "POST"])
def shefforg_mail_iniciator():
    if request.method == "GET":
        db_session = get_session()
        select = get_select()
        idorg = session["user"][0]
        select_iniciators = (
            select(
                Initiatorsofprojects.initprEmail,
                Initiatorsofprojects.initprPositions,
                Initiatorsofprojects.FullName,
                Organizations.orgName,
            )
            .join(Organizations)
            .filter(Initiatorsofprojects.IDorg == idorg)
            .order_by(Initiatorsofprojects.FullName)
        )
        iniciators = db_session.execute(select_iniciators).all()
        db_session.commit()
        return render_template("students_mail_iniciator.html", users=iniciators)


@pages.route("/student/mailSheffPr", methods=["GET", "POST"])
def student_mail_sheff_proj():
    if request.method == "GET":
        db_session = get_session()
        idstudent = session["user"][1]
        select = get_select()
        select_projects = (
            select(Projects.IDprojects, PassportOfProjects.passportName)
            .distinct()
            .join_from(
                PassportOfProjects, Projects, PassportOfProjects.IDpassport == Projects.IDpassport
            )
            .join(StudentsInProjects)
            .filter(StudentsInProjects.IDstudents == idstudent)
        )

        projects = db_session.execute(select_projects).all()
        idproj = projects[0][0] if projects else text("1=0")

        students = db_session.execute(
            text(
                """SELECT distinct
        CONCAT_WS(' ', s2.sheffprFirstname, s2.sheffprName, s2.sheffprFathername),
        s2.sheffprEmail
    FROM
        projects p
    join passportofprojects p2 on
        ( p2.IDpassport = p.IDpassport )
    join sheffofprojects s2  on
        ( s2.IDsheffpr = p2.IDsheffpr )
    WHERE	p.idprojects = :idproj"""
            ),
            {"idproj": idproj},
        ).all()

        db_session.commit()
        return render_template("students_mail_sheffpr.html", users=students, projects=projects)


@pages.route("/sheffproj/mailAnotherStudents", methods=["GET", "POST"])
def sheffproj_mail_students():
    if request.method == "GET":
        db_session = get_session()
        select = get_select()
        idsheff_proj = session["user"][0]

        select_projects = (
            select(Projects.IDprojects, PassportOfProjects.passportName)
            .distinct()
            .join_from(
                PassportOfProjects, Projects, PassportOfProjects.IDpassport == Projects.IDpassport
            )
            .filter(PassportOfProjects.IDsheffpr == idsheff_proj)
        )

        projects = db_session.execute(select_projects).all()
        idproj = projects[0][0] if projects else text("1=0")

        students = db_session.execute(
            text(
                """SELECT distinct
        CONCAT_WS(' ',s3.studentsFirstname, s3.studentsName, s3.studentsFathername),
		s3.studentsEmail,
        concat_ws(' - ', g.groupsname, concat(p3.rolesrole, ' - ', p3.rolesfunction))
        FROM	studentsinprojects s
                join projects p on ( p.IDprojects  = s.IDprojects )
                join passportofprojects p2 on ( p2.IDpassport = p.IDpassport )
                join students s3 on ( s3.IDstudents = s.IDstudents )
                join rolesofprojects p3 on (p3.idroles = s.idroles)
                join `groups` g on (s3.idgroups = g.idgroups)
        WHERE 	p2.IDsheffpr = :idsheffproj
                and p.idprojects = :idproj"""
            ),
            {"idsheffproj": idsheff_proj, "idproj": idproj},
        ).all()

        db_session.commit()
        return render_template("students_mail_student.html", users=students, projects=projects)


@pages.route("/sheffproj/mailIniciator", methods=["GET", "POST"])
def sheffproj_mail_iniciator():
    if request.method == "GET":
        db_session = get_session()
        select = get_select()
        idsheff_proj = session["user"][0]

        select_projects = (
            select(PassportOfProjects.IDinitpr, PassportOfProjects.passportName)
            .distinct()
            .join_from(
                PassportOfProjects, Projects, PassportOfProjects.IDpassport == Projects.IDpassport
            )
            .filter(PassportOfProjects.IDsheffpr == idsheff_proj)
        )

        projects = db_session.execute(select_projects).all()
        idinic = projects[0][0] if projects else text("1=0")

        iniciators = db_session.execute(
            text(
                """SELECT distinct
            i.initprEmail,
            i.initprPositions,
            CONCAT_WS(' ', i.initprFirstname, i.initprName, i.initprFathername),
            o.orgname
        FROM
            initiatorsofprojects i
        join organizations o on ( o.idorg = i.idorg )
        WHERE	i.IDinitpr = :idinic"""
            ),
            {"idinic": idinic},
        ).all()
        db_session.commit()
        return render_template("students_mail_iniciator.html", users=iniciators, projects=projects)


@pages.route("/iniciators/mailAnotherStudents", methods=["GET", "POST"])
def iniciator_mail_students():
    if request.method == "GET":
        db_session = get_session()
        select = get_select()
        idiniciator = session["user"][1]

        select_projects = (
            select(Projects.IDprojects, PassportOfProjects.passportName)
            .distinct()
            .join_from(
                PassportOfProjects, Projects, PassportOfProjects.IDpassport == Projects.IDpassport
            )
            .join(Initiatorsofprojects)
            .filter(Initiatorsofprojects.IDinitpr == idiniciator)
        )

        projects = db_session.execute(select_projects).all()
        idproj = projects[0][0] if projects else text("1=0")
        students = db_session.execute(
            text(
                """SELECT distinct CONCAT_WS(' ',s3.studentsFirstname, s3.studentsName, s3.studentsFathername),
		s3.studentsEmail,
        concat_ws(' - ', g.groupsname, concat(p3.rolesrole, ' - ', p3.rolesfunction))
FROM	studentsinprojects s
		join projects p on ( p.IDprojects  = s.IDprojects )
        join passportofprojects p2 on ( p2.IDpassport = p.IDpassport )
		join students s3 on ( s3.IDstudents = s.IDstudents  )
        join rolesofprojects p3 on (p3.idroles = s.idroles)
        join `groups` g on (s3.idgroups = g.idgroups)
WHERE 	p.idprojects = :idproj"""
            ),
            {"idproj": idproj},
        ).all()

        db_session.commit()
        return render_template("students_mail_student.html", users=students, projects=projects)


@pages.route("/iniciators/mailSheffPr", methods=["GET", "POST"])
def iniciator_mail_sheff_proj():
    if request.method == "GET":
        db_session = get_session()
        select = get_select()
        idiniciator = session["user"][1]
        select_projects = (
            select(Projects.IDprojects, PassportOfProjects.passportName)
            .distinct()
            .join_from(
                PassportOfProjects, Projects, PassportOfProjects.IDpassport == Projects.IDpassport
            )
            .join(Initiatorsofprojects)
            .filter(Initiatorsofprojects.IDinitpr == idiniciator)
        )

        projects = db_session.execute(select_projects).all()
        idproj = projects[0][0] if projects else text("1=0")

        students = db_session.execute(
            text(
                """SELECT distinct
	CONCAT_WS(' ', s2.sheffprFirstname, s2.sheffprName, s2.sheffprFathername),
	s2.sheffprEmail
FROM
	studentsinprojects s
join projects p on
	( p.IDprojects = s.IDprojects )
join passportofprojects p2 on
	( p2.IDpassport = p.IDpassport )
join sheffofprojects s2  on
	( s2.IDsheffpr = p2.IDsheffpr )
WHERE 	p.idprojects = :idproj"""
            ),
            {"idproj": idproj},
        ).all()

        db_session.commit()
        return render_template("students_mail_sheffpr.html", users=students, projects=projects)


@pages.route("/shefforg/mailAnotherStudents", methods=["GET", "POST"])
def shefforg_mail_students():
    if request.method == "GET":
        db_session = get_session()
        idorg = session["user"][0]
        select = get_select()
        select_projects = (
            select(Projects.IDprojects, PassportOfProjects.passportName)
            .distinct()
            .join_from(
                PassportOfProjects, Projects, PassportOfProjects.IDpassport == Projects.IDpassport
            )
            .join(Initiatorsofprojects)
            .filter(Initiatorsofprojects.IDorg == idorg)
        )

        projects = db_session.execute(select_projects).all()
        idproj = projects[0][0] if projects else text("1=0")

        students = db_session.execute(
            text(
                """SELECT distinct
                CONCAT_WS(' ',s3.studentsFirstname, s3.studentsName, s3.studentsFathername),
                s3.studentsEmail,
                concat_ws(' - ', g.groupsname, concat(p3.rolesrole, ' - ', p3.rolesfunction))
        FROM	studentsinprojects s
                join projects p on ( p.IDprojects  = s.IDprojects )
                join passportofprojects p2 on ( p2.IDpassport = p.IDpassport )
                join students s3 on ( s3.IDstudents = s.IDstudents  )
                join `groups` g on ( g.idgroups = s3.idgroups )
                join rolesofprojects p3 on (p3.idroles = s.idroles)
        WHERE 	p.idprojects = :idproj"""
            ),
            {"idproj": idproj},
        ).all()

        db_session.commit()
        return render_template("students_mail_student.html", users=students, projects=projects)


@pages.route("/shefforg/mailSheffPr", methods=["GET", "POST"])
def shefforg_mail_sheff_proj():
    if request.method == "GET":
        db_session = get_session()
        select = get_select()
        idorg = session["user"][0]

        select_projects = (
            select(Projects.IDprojects, PassportOfProjects.passportName)
            .distinct()
            .join_from(
                PassportOfProjects, Projects, PassportOfProjects.IDpassport == Projects.IDpassport
            )
            .join(Initiatorsofprojects)
            .filter(Initiatorsofprojects.IDorg == idorg)
        )

        projects = db_session.execute(select_projects).all()
        idproj = projects[0][0] if projects else text("1=0")

        students = db_session.execute(
            text(
                """SELECT distinct
            CONCAT_WS(' ', s2.sheffprFirstname, s2.sheffprName, s2.sheffprFathername),
            s2.sheffprEmail
        FROM
            projects p
        join passportofprojects p2 on
            ( p2.IDpassport = p.IDpassport )
        join sheffofprojects s2  on
            ( s2.IDsheffpr = p2.IDsheffpr )
        WHERE	p.idprojects = :idproj"""
            ),
            {"idproj": idproj},
        ).all()

        db_session.commit()
        return render_template("students_mail_sheffpr.html", users=students, projects=projects)


@pages.route("/uploadWorkStudent", methods=["POST"])
def upload_work_student():
    upload_file = request.files.get("file")
    id_work = request.form.get("work_id")
    if not upload_file or not id_work:
        return

    file_path = path.join("documents", upload_file.filename)

    db_session = get_session()
    record = (
        db_session.query(StudentsInProjects)
        .filter(StudentsInProjects.IDstudentspr == id_work)
        .first()
    )
    record.studentsinprFull = file_path
    db_session.commit()

    upload_file.save(file_path)

    db_session.commit()
    return render_template(
        "works_template.html", idstud=record.IDstudentspr, signed=record.studentsinprFull
    )


@pages.route("/deleteWorkStudent", methods=["POST"])
def delete_work_student():
    id_work = request.form.get("idWork")
    if not id_work:
        return

    db_session = get_session()
    record = (
        db_session.query(StudentsInProjects)
        .filter(StudentsInProjects.IDstudentspr == id_work)
        .first()
    )
    record.studentsinprFull = None
    db_session.commit()
    db_session.commit()
    return render_template(
        "works_template.html", idstud=record.IDstudentspr, signed=record.studentsinprFull
    )


@pages.route("/workResult", methods=["GET"])
def get_work_student():
    args = request.args
    idwork = args.get("idwork")

    db_session = get_session()
    work = (
        db_session.query(StudentsInProjects)
        .filter(StudentsInProjects.IDstudentspr == idwork)
        .first()
    )

    if not work.studentsinprFull:
        return "", 404

    return send_file(work.studentsinprFull, mimetype="multipart/form-data", as_attachment=True)


@pages.route("/student/modifyWork", methods=["POST"])
def student_modify_work():
    idwork = request.form["work"]
    idstadia = request.form["stage"]
    db_session = get_session()
    work = (
        db_session.query(StudentsInProjects)
        .filter(StudentsInProjects.IDstudentspr == idwork)
        .first()
    )
    work.IDstadiaofworks = idstadia
    db_session.commit()

    return redirect("/student/works")


@pages.route("/getConfirmationSigned", methods=["GET"])
def get_confirmation_signed():
    args = request.args
    idConfirmation = args.get("idConfirmation")
    db_session = get_session()
    record = (
        db_session.query(Confirmation).filter(Confirmation.IDconfirmation == idConfirmation).first()
    )
    if not record.confirmationSigned:
        return "", 404
    return send_file(record.confirmationSigned, mimetype="multipart/form-data", as_attachment=True)


@pages.route("/uploadConfirmation", methods=["POST"])
def upload_confirmation_signed():
    upload_file = request.files.get("file")
    id_confirmation = request.form.get("confirmation_id")
    if not upload_file or not id_confirmation:
        return

    file_path = path.join("documents", upload_file.filename)

    db_session = get_session()
    confirmation = (
        db_session.query(Confirmation)
        .filter(Confirmation.IDconfirmation == id_confirmation)
        .first()
    )
    confirmation.confirmationSigned = file_path
    db_session.commit()

    upload_file.save(file_path)

    db_session.commit()
    return render_template(
        "confirmed_template.html",
        idconfirm=confirmation.IDconfirmation,
        signed=confirmation.confirmationSigned,
    )


@pages.route("/deleteConfirmation", methods=["POST"])
def delete_confirmation_signed():
    idconfirmation = request.form.get("idConfirmation")
    if not idconfirmation:
        return

    db_session = get_session()
    confirmation = (
        db_session.query(Confirmation)
        .filter(Confirmation.IDconfirmation == idconfirmation)
        .first()
    )
    confirmation.confirmationSigned = None
    db_session.commit()
    db_session.commit()
    return render_template(
        "confirmed_template.html",
        idconfirm=confirmation.IDconfirmation,
        signed=confirmation.confirmationSigned,
    )


@pages.route("/iniciators/works", methods=["GET", "POST"])
def iniciators_works():
    if request.method == "GET":
        idiniciator = session["user"][1]
        db_session = get_session()
        select = get_select()
        select_projects = (
            select(Projects, PassportOfProjects)
            .distinct()
            .join(StudentsInProjects)
            .join(PassportOfProjects)
            .filter(PassportOfProjects.IDinitpr == idiniciator)
        )
        select_works = (
            select(
                StudentsInProjects,
                Students,
                StadiaOfWorks,
                RolesOfProjects,
                Projects,
                PassportOfProjects,
            )
            .distinct()
            .join_from(
                StudentsInProjects, Projects, StudentsInProjects.IDprojects == Projects.IDprojects
            )
            .join(Confirmation, isouter=True)
            .join(
                Applications,
                onclause=Applications.IDapplications == StudentsInProjects.IDapplications,
            )
            .join(PassportOfProjects, PassportOfProjects.IDpassport == Projects.IDpassport)
            .join(Students, onclause=Students.IDstudents == StudentsInProjects.IDstudents)
            .join(StadiaOfWorks)
            .join(RolesOfProjects, RolesOfProjects.IDroles == StudentsInProjects.IDroles)
            .filter(PassportOfProjects.IDinitpr == idiniciator)
        )
        projects = db_session.execute(pagination(select_projects)).all()
        count_projects = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        works = db_session.execute(select_works).all()
        status = db_session.execute(select(StadiaOfWorks)).all()
        db_session.commit()
        return render_template(
            "iniciators_works.html", projects=projects, works=works, status=status, count=count_projects,
            page=0,
            function="applyInicWorkFilters",
        )
    if request.method == "POST":
        idiniciator = session["user"][1]
        db_session = get_session()
        select = get_select()
        fio_filter = request.form.get("fioFilter")
        project_filter = request.form.get("projectFilter")
        role_filter = request.form.get("roleFilter")
        status_filter = request.form.get("statusFilter")
        page = (request.form.get("page") and int(request.form.get("page"))) or 0
        where_status_filter = (
            StudentsInProjects.IDstadiaofworks == status_filter if status_filter else text("1=1")
        )
        where_fio_filter = (
            Students.FullName.ilike("%" + fio_filter + "%") if fio_filter else text("1=1")
        )
        where_project_filter = (
            PassportOfProjects.passportName.ilike("%" + project_filter + "%")
            if project_filter
            else text("1=1")
        )
        where_role_filter = (
            RolesOfProjects.rolesRole.ilike("%" + role_filter + "%") if role_filter else text("1=1")
        )
        select_projects = (
            select(Projects, PassportOfProjects)
            .distinct()
            .join(StudentsInProjects)
            .join(PassportOfProjects)
            .join(RolesOfProjects)
            .join(Students)
            .filter(PassportOfProjects.IDinitpr == idiniciator)
            .filter(where_project_filter)
            .filter(where_role_filter)
            .filter(where_fio_filter)
            .filter(where_status_filter)
        )
        select_works = (
            select(
                StudentsInProjects,
                Students,
                StadiaOfWorks,
                RolesOfProjects,
                Projects,
                PassportOfProjects,
            )
            .distinct()
            .join_from(
                StudentsInProjects, Projects, StudentsInProjects.IDprojects == Projects.IDprojects
            )
            .join(Confirmation, isouter=True)
            .join(
                Applications,
                onclause=Applications.IDapplications == StudentsInProjects.IDapplications,
            )
            .join(PassportOfProjects, PassportOfProjects.IDpassport == Projects.IDpassport)
            .join(Students, onclause=Students.IDstudents == StudentsInProjects.IDstudents)
            .join(StadiaOfWorks)
            .join(RolesOfProjects, RolesOfProjects.IDroles == StudentsInProjects.IDroles)
            .filter(PassportOfProjects.IDinitpr == idiniciator)
            .filter(where_project_filter)
            .filter(where_fio_filter)
            .filter(where_role_filter)
            .filter(where_status_filter)
        )
        projects = db_session.execute(pagination(select_projects, page)).all()
        count_projects = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        works = db_session.execute(select_works).all()

        db_session.commit()
        return render_template("resultAccordionWorks.html", projects=projects, works=works, count=count_projects,
            page=page, function="applyInicWorkFilters",)


@pages.route("/shefforg/works", methods=["GET", "POST"])
def sheff_org_works():
    if request.method == "GET":
        idorg = session["user"][0]
        db_session = get_session()
        select = get_select()
        select_projects = (
            select(Projects, PassportOfProjects)
            .distinct()
            .join_from(
                StudentsInProjects, Projects, StudentsInProjects.IDprojects == Projects.IDprojects
            )
            .join(PassportOfProjects)
            .join(RolesOfProjects)
            .join(Students)
            .join(Initiatorsofprojects)
            .filter(Initiatorsofprojects.IDorg == idorg)
        )
        select_works = (
            select(
                StudentsInProjects,
                Students,
                StadiaOfWorks,
                RolesOfProjects,
                Projects,
                PassportOfProjects,
            )
            .distinct()
            .join_from(
                StudentsInProjects, Projects, StudentsInProjects.IDprojects == Projects.IDprojects
            )
            .join(Confirmation, isouter=True)
            .join(
                Applications,
                onclause=Applications.IDapplications == StudentsInProjects.IDapplications,
            )
            .join(PassportOfProjects, PassportOfProjects.IDpassport == Projects.IDpassport)
            .join(Students, onclause=Students.IDstudents == StudentsInProjects.IDstudents)
            .join(StadiaOfWorks)
            .join(RolesOfProjects, RolesOfProjects.IDroles == StudentsInProjects.IDroles)
            .join(Initiatorsofprojects)
            .filter(Initiatorsofprojects.IDorg == idorg)
        )
        works = db_session.execute(select_works).all()
        stadia = db_session.execute(select(StadiaOfWorks))
        projects = db_session.execute(pagination(select_projects)).all()
        count = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        db_session.commit()
        return render_template(
            "sheff_org_works.html", projects=projects, works=works, stadia=stadia, count=count, page=0, function='applyInicWorkFilters'
        )
    if request.method == "POST":
        idorg = session["user"][0]
        db_session = get_session()
        select = get_select()
        fio_filter = request.form.get("fioFilter")
        project_filter = request.form.get("projectFilter")
        role_filter = request.form.get("roleFilter")
        status_filter = request.form.get("statusFilter")
        page = (request.form.get("page") and int(request.form.get("page"))) or 0
        where_fio_filter = (
            Students.FullName.ilike("%" + fio_filter + "%") if fio_filter else text("1=1")
        )
        where_project_filter = (
            PassportOfProjects.passportName.ilike("%" + project_filter + "%")
            if project_filter
            else text("1=1")
        )
        where_role_filter = (
            RolesOfProjects.rolesRole.ilike("%" + role_filter + "%") if role_filter else text("1=1")
        )
        where_status_filter = (
            StudentsInProjects.IDstadiaofworks == status_filter if status_filter else text("1=1")
        )
        select_projects = (
            select(Projects, PassportOfProjects)
            .distinct()
            .join_from(
                StudentsInProjects, Projects, StudentsInProjects.IDprojects == Projects.IDprojects
            )
            .join(PassportOfProjects)
            .join(RolesOfProjects)
            .join(Students)
            .join(Initiatorsofprojects)
            .filter(Initiatorsofprojects.IDorg == idorg)
            .filter(where_status_filter)
            .filter(where_role_filter)
            .filter(where_project_filter)
            .filter(where_fio_filter)
        )
        select_works = (
            select(
                StudentsInProjects,
                Students,
                StadiaOfWorks,
                RolesOfProjects,
                Projects,
                PassportOfProjects,
            )
            .distinct()
            .join_from(
                StudentsInProjects, Projects, StudentsInProjects.IDprojects == Projects.IDprojects
            )
            .join(Confirmation, isouter=True)
            .join(
                Applications,
                onclause=Applications.IDapplications == StudentsInProjects.IDapplications,
            )
            .join(PassportOfProjects, PassportOfProjects.IDpassport == Projects.IDpassport)
            .join(Students, onclause=Students.IDstudents == StudentsInProjects.IDstudents)
            .join(StadiaOfWorks)
            .join(RolesOfProjects, RolesOfProjects.IDroles == StudentsInProjects.IDroles)
            .join(Initiatorsofprojects)
            .filter(Initiatorsofprojects.IDorg == idorg)
            .filter(where_status_filter)
            .filter(where_role_filter)
            .filter(where_project_filter)
            .filter(where_fio_filter)
        )
        projects = db_session.execute(pagination(select_projects, page)).all()
        count = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        works = db_session.execute(select_works).all()
        db_session.commit()
        return render_template("resultAccordionWorks.html", projects=projects, works=works, count=count, page=page, function='applyInicWorkFilters')


@pages.route("/getFullProject", methods=["GET"])
def get_project_full():
    args = request.args
    idpassport = args.get("idProject")
    db_session = get_session()
    record = (
        db_session.query(Projects)
        .join(PassportOfProjects)
        .filter(PassportOfProjects.IDpassport == idpassport)
        .first()
    )
    if not record.projectsFull:
        return "", 404
    return send_file(record.projectsFull, mimetype="multipart/form-data", as_attachment=True)


@pages.route("/uploadProjectResult", methods=["POST"])
def upload_project_result():
    upload_file = request.files.get("file")
    idpassport = request.form.get("passport_id")
    if not upload_file or not idpassport:
        return

    file_path = path.join("documents", upload_file.filename)

    db_session = get_session()
    record = (
        db_session.query(Projects)
        .join(PassportOfProjects)
        .filter(PassportOfProjects.IDpassport == idpassport)
        .first()
    )
    record.projectsFull = file_path
    db_session.commit()

    upload_file.save(file_path)

    db_session.commit()
    return render_template(
        "result_template.html",
        idproj=record.IDprojects,
        signed=record.projectsFull,
        stadia=record.IDstadiaofpr,
    )


@pages.route("/deleteProjectResult", methods=["POST"])
def delete_project_result():
    idproject = request.form.get("idProject")

    if not idproject:
        return

    db_session = get_session()
    record = db_session.query(Projects).filter(Projects.IDprojects == idproject).first()
    record.projectsFull = None
    db_session.commit()
    db_session.commit()
    return render_template(
        "result_template.html",
        idproj=record.IDprojects,
        signed=record.projectsFull,
        stadia=record.IDstadiaofpr,
    )


@pages.route("/shefforg/members", methods=["GET", "POST"])
def sheff_org_members():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
        idorg = session["user"][0]
        select_projects = (
            select(
                PassportOfProjects.IDpassport, PassportOfProjects.passportName, Projects.IDprojects
            )
            .distinct()
            .join_from(
                Projects,
                PassportOfProjects,
                Projects.IDpassport == PassportOfProjects.IDpassport,
                isouter=True,
            )
            .join(StudentsInProjects)
            .join(Initiatorsofprojects)
            .filter(Initiatorsofprojects.IDorg == idorg)
            .order_by(PassportOfProjects.passportName)
        )
        select_confirmation = (
            select(
                Students,
                Groups,
                Levels,
                Confirmation,
                Specializations,
                RolesOfProjects,
                PassportOfProjects,
                StudentsInProjects,
                StadiaOfWorks,
            )
            .distinct()
            .join_from(
                Projects, StudentsInProjects, Projects.IDprojects == StudentsInProjects.IDprojects
            )
            .join(StadiaOfWorks)
            .join(RolesOfProjects)
            .join(Students)
            .join(Groups)
            .join(
                Confirmation,
                Confirmation.IDconfirmation == StudentsInProjects.IDconfirmation,
                isouter=True,
            )
            .join(Levels, isouter=True)
            .join(PassportOfProjects, PassportOfProjects.IDpassport == Projects.IDpassport)
            .join(Specializations)
            .join(Initiatorsofprojects)
            .filter(Initiatorsofprojects.IDorg == idorg)
            .order_by(PassportOfProjects.passportName)
        )
        groups = db_session.execute(select(Groups))
        approved = db_session.execute(select_confirmation).all()
        levels = db_session.execute((select(Levels))).all()
        status = db_session.execute(select(StadiaOfWorks)).all()
        projects = db_session.execute(pagination(select_projects)).all()
        projects_count = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        db_session.commit()
        return render_template(
            "sheff_org_members.html",
            projects=projects,
            approved=approved,
            levels=levels,
            groups=groups,
            status=status,
            count=projects_count,
            function='applyMemFilters',
            page=0
        )
    if request.method == "POST":
        select = get_select()
        db_session = get_session()
        fio_filter = request.form.get("projectFioFilter")
        project_filter = request.form.get("projectNameFilter")
        group_filter = request.form.get("groupFilter")
        role_filter = request.form.get("roleFilter")
        status_filter = request.form.get("statusFilter")
        page = (request.form.get("page") and int(request.form.get("page"))) or 0
        where_status_filter = (
            StadiaOfWorks.IDstadiaofworks == status_filter if status_filter else text("1=1")
        )
        where_fio_filter = (
            Students.FullName.ilike("%" + fio_filter + "%") if fio_filter else text("1=1")
        )
        where_project_filter = (
            PassportOfProjects.passportName.ilike("%" + project_filter + "%")
            if project_filter
            else text("1=1")
        )
        where_group_filter = Students.IDgroups == group_filter if group_filter else text("1=1")
        where_role_filter = (
            RolesOfProjects.rolesRole.ilike("%" + role_filter + "%") if role_filter else text("1=1")
        )
        idorg = session["user"][0]
        select_projects = (
            select(
                PassportOfProjects.IDpassport, PassportOfProjects.passportName, Projects.IDprojects
            )
            .distinct()
            .join_from(
                Projects,
                PassportOfProjects,
                Projects.IDpassport == PassportOfProjects.IDpassport,
                isouter=True,
            )
            .join(StudentsInProjects)
            .join(RolesOfProjects)
            .join(Students)
            .join(Initiatorsofprojects)
            .filter(Initiatorsofprojects.IDorg == idorg)
            .filter(where_fio_filter)
            .filter(where_project_filter)
            .filter(where_group_filter)
            .filter(where_role_filter)
            .filter(where_status_filter)
            .order_by(PassportOfProjects.passportName)
        )
        select_confirmation = (
            select(
                Students,
                Groups,
                Levels,
                Confirmation,
                Specializations,
                RolesOfProjects,
                PassportOfProjects,
                StudentsInProjects,
                StadiaOfWorks,
            )
            .distinct()
            .join_from(
                Projects, StudentsInProjects, Projects.IDprojects == StudentsInProjects.IDprojects
            )
            .join(StadiaOfWorks)
            .join(RolesOfProjects)
            .join(Students)
            .join(Groups)
            .join(
                Confirmation,
                Confirmation.IDconfirmation == StudentsInProjects.IDconfirmation,
                isouter=True,
            )
            .join(Levels, isouter=True)
            .join(PassportOfProjects, PassportOfProjects.IDpassport == Projects.IDpassport)
            .join(Specializations)
            .join(Initiatorsofprojects)
            .filter(Initiatorsofprojects.IDorg == idorg)
            .filter(where_fio_filter)
            .filter(where_project_filter)
            .filter(where_group_filter)
            .filter(where_role_filter)
            .order_by(PassportOfProjects.passportName)
        )
        approved = db_session.execute(select_confirmation).all()
        projects = db_session.execute(pagination(select_projects, page)).all()
        projects_count = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        db_session.commit()
        return render_template(
            "resultAccordionStudentApprovedTickets.html",
            projects=projects,
            approved=approved,
            count=projects_count,
            function='applyMemFilters',
            page=page
        )


@pages.route("/iniciators/members", methods=["GET", "POST"])
def iniciators_members():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
        idiniciator = session["user"][1]
        select_projects = (
            select(
                PassportOfProjects.IDpassport, PassportOfProjects.passportName, Projects.IDprojects
            )
            .distinct()
            .join_from(
                Projects, PassportOfProjects, PassportOfProjects.IDpassport == Projects.IDpassport
            )
            .join(StudentsInProjects)
            .filter(PassportOfProjects.IDinitpr == idiniciator)
            .order_by(PassportOfProjects.passportName)
        )
        select_confirmation = (
            select(
                Students,
                Groups,
                Levels,
                Confirmation,
                Specializations,
                RolesOfProjects,
                PassportOfProjects,
                StudentsInProjects,
                StadiaOfWorks,
            )
            .distinct()
            .join_from(
                Projects, StudentsInProjects, Projects.IDprojects == StudentsInProjects.IDprojects
            )
            .join(StadiaOfWorks)
            .join(RolesOfProjects)
            .join(Students)
            .join(Groups)
            .join(
                Confirmation,
                Confirmation.IDconfirmation == StudentsInProjects.IDconfirmation,
                isouter=True,
            )
            .join(Levels, isouter=True)
            .join(PassportOfProjects, PassportOfProjects.IDpassport == Projects.IDpassport)
            .join(Specializations)
            .filter(PassportOfProjects.IDinitpr == idiniciator)
            .order_by(PassportOfProjects.passportName)
        )
        count_projects = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        confirmations = db_session.execute(select_confirmation).all()
        projects = db_session.execute(pagination(select_projects)).all()
        levels = db_session.execute((select(Levels))).all()
        status = db_session.execute(select(StadiaOfWorks)).all()
        groups = db_session.execute(select(Groups)).all()
        db_session.commit()
        return render_template(
            "iniciators_members.html",
            projects=projects,
            approved=confirmations,
            levels=levels,
            status=status,
            groups=groups,
            count=count_projects,
            page=0,
            function="applyMemFilters",
        )
    if request.method == "POST":
        select = get_select()
        db_session = get_session()
        fio_filter = request.form.get("projectFioFilter")
        project_filter = request.form.get("projectNameFilter")
        status_filter = request.form.get("statusFilter")
        group_filter = request.form.get("groupFilter")
        role_filter = request.form.get("roleFilter")
        page = (request.form.get("page") and int(request.form.get("page"))) or 0
        where_group_filter = Students.IDgroups == group_filter if group_filter else text("1=1")
        where_role_filter = (
            RolesOfProjects.rolesRole.ilike("%" + role_filter + "%") if role_filter else text("1=1")
        )
        where_status_filter = (
            StadiaOfWorks.IDstadiaofworks == status_filter if status_filter else text("1=1")
        )
        where_fio_filter = (
            Students.FullName.ilike("%" + fio_filter + "%") if fio_filter else text("1=1")
        )
        where_project_filter = (
            PassportOfProjects.passportName.ilike("%" + project_filter + "%")
            if project_filter
            else text("1=1")
        )

        idiniciator = session["user"][1]
        select_projects = (
            select(
                PassportOfProjects.IDpassport, PassportOfProjects.passportName, Projects.IDprojects
            )
            .distinct()
            .join_from(
                Projects, PassportOfProjects, PassportOfProjects.IDpassport == Projects.IDpassport
            )
            .join(StudentsInProjects)
            .join(RolesOfProjects, RolesOfProjects.IDroles == StudentsInProjects.IDroles)
            .join(Students)
            .filter(PassportOfProjects.IDinitpr == idiniciator)
            .filter(where_role_filter)
            .filter(where_group_filter)
            .filter(where_fio_filter)
            .filter(where_project_filter)
            .order_by(PassportOfProjects.passportName)
        )
        select_confirmation = (
            select(
                Students,
                Groups,
                Levels,
                Confirmation,
                Specializations,
                RolesOfProjects,
                PassportOfProjects,
                StudentsInProjects,
                StadiaOfWorks,
            )
            .distinct()
            .join_from(
                Projects, StudentsInProjects, Projects.IDprojects == StudentsInProjects.IDprojects
            )
            .join(StadiaOfWorks)
            .join(RolesOfProjects)
            .join(Students)
            .join(Groups)
            .join(
                Confirmation,
                Confirmation.IDconfirmation == StudentsInProjects.IDconfirmation,
                isouter=True,
            )
            .join(Levels, isouter=True)
            .join(PassportOfProjects, PassportOfProjects.IDpassport == Projects.IDpassport)
            .join(Specializations)
            .filter(where_group_filter)
            .filter(where_role_filter)
            .filter(where_fio_filter)
            .filter(where_project_filter)
            .filter(where_status_filter)
            .filter(PassportOfProjects.IDinitpr == idiniciator)
            .order_by(PassportOfProjects.passportName)
        )
        confirmations = db_session.execute(select_confirmation).all()
        count_projects = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        projects = db_session.execute(pagination(select_projects, page)).all()
        db_session.commit()
        return render_template(
            "resultAccordionStudentApprovedTickets.html",
            projects=projects,
            approved=confirmations,
            count=count_projects,
            page=0,
            function="applyMemFilters"
        )


@pages.route("/student/members", methods=["GET", "POST"])
def student_members():
    if request.method == "GET":
        select = get_select()
        db_session = get_session()
        idstudent = session["user"][1]
        select_projects = (
            select(
                PassportOfProjects.IDpassport, PassportOfProjects.passportName, Projects.IDprojects
            )
            .distinct()
            .join_from(
                Projects, PassportOfProjects, PassportOfProjects.IDpassport == Projects.IDpassport
            )
            .join(StudentsInProjects)
            .filter(StudentsInProjects.IDstudents == idstudent)
            .order_by(PassportOfProjects.passportName)
        )
        select_confirmation = (
            select(
                Students,
                Groups,
                Levels,
                Confirmation,
                Specializations,
                RolesOfProjects,
                PassportOfProjects,
                StudentsInProjects,
                StadiaOfWorks,
            )
            .distinct()
            .join_from(
                StudentsInProjects,
                Students,
                Students.IDstudents == StudentsInProjects.IDstudents,
                isouter=True,
            )
            .join(StadiaOfWorks)
            .join(RolesOfProjects)
            .join(Confirmation, isouter=True)
            .join(Levels, isouter=True)
            .join(Groups)
            .join(Projects, StudentsInProjects.IDprojects == Projects.IDprojects)
            .join(PassportOfProjects, Projects.IDpassport == PassportOfProjects.IDpassport)
            .join(Specializations)
            .filter(Students.IDstudents != idstudent)
            .order_by(PassportOfProjects.passportName)
        )
        confirmations = db_session.execute(select_confirmation).all()
        levels = db_session.execute((select(Levels))).all()
        groups = db_session.execute(select(Groups)).all()
        status = db_session.execute(select(StadiaOfWorks)).all()
        projects = db_session.execute(pagination(select_projects)).all()
        projects_count = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()

        db_session.commit()
        return render_template(
            "students_members.html",
            projects=projects,
            approved=confirmations,
            levels=levels,
            groups=groups,
            status=status,
            count=projects_count,
            function='applyMemFilters',
            page=0
        )
    if request.method == "POST":
        select = get_select()
        db_session = get_session()
        fio_filter = request.form.get("projectFioFilter")
        project_filter = request.form.get("projectNameFilter")
        group_filter = request.form.get("groupFilter")
        napr_filter = request.form.get("naprFilter")
        status_filter = request.form.get("statusFilter")
        page = (request.form.get("page") and int(request.form.get("page"))) or 0
        where_status_filter = (
            StadiaOfWorks.IDstadiaofworks == status_filter if status_filter else text("1=1")
        )
        where_fio_filter = (
            Students.FullName.ilike("%" + fio_filter + "%") if fio_filter else text("1=1")
        )
        where_project_filter = (
            PassportOfProjects.passportName.ilike("%" + project_filter + "%")
            if project_filter
            else text("1=1")
        )
        where_group_filter = Groups.IDgroups == group_filter if group_filter else text("1=1")
        where_napr_filter = (
            Specializations.FullSpec.ilike("%" + napr_filter + "%") if napr_filter else text("1=1")
        )
        idstudent = session["user"][1]
        select_projects = (
            select(
                PassportOfProjects.IDpassport, PassportOfProjects.passportName, Projects.IDprojects
            )
            .distinct()
            .join_from(
                Projects, PassportOfProjects, PassportOfProjects.IDpassport == Projects.IDpassport
            )
            .join(StudentsInProjects)
            .join(Students)
            .filter(StudentsInProjects.IDstudents == idstudent)
            .filter(where_project_filter)
        )
        select_confirmation = (
            select(
                Students,
                Groups,
                Levels,
                Confirmation,
                Specializations,
                RolesOfProjects,
                PassportOfProjects,
                StudentsInProjects,
                StadiaOfWorks,
            )
            .distinct()
            .join_from(
                StudentsInProjects,
                Students,
                Students.IDstudents == StudentsInProjects.IDstudents,
                isouter=True,
            )
            .join(StadiaOfWorks)
            .join(RolesOfProjects)
            .join(Confirmation, isouter=True)
            .join(Levels, isouter=True)
            .join(Groups)
            .join(Projects, StudentsInProjects.IDprojects == Projects.IDprojects)
            .join(PassportOfProjects, Projects.IDpassport == PassportOfProjects.IDpassport)
            .join(Specializations)
            .filter(Students.IDstudents != idstudent)
            .filter(where_status_filter)
            .filter(where_fio_filter)
            .filter(where_project_filter)
            .filter(where_group_filter)
            .filter(where_napr_filter)
            .order_by(PassportOfProjects.passportName)
        )
        projects = db_session.execute(pagination(select_projects, page)).all()
        confirmations = db_session.execute(select_confirmation).all()
        projects_count = db_session.execute(count_records(select_projects, Projects.IDprojects)).scalar_one()
        db_session.commit()
        return render_template(
            "resultAccordionStudentApprovedTickets.html",
            projects=projects,
            approved=confirmations,
            count=projects_count,
            function='applyMemFilters',
            page=0
        )


@pages.route("/admin/mailAnotherStudents", methods=["GET"])
def admin_mail_students():
    if request.method == "GET":
        db_session = get_session()
        select = get_select()
        select_projects = (
            select(Projects.IDprojects, PassportOfProjects.passportName)
            .distinct()
            .join_from(
                PassportOfProjects, Projects, PassportOfProjects.IDpassport == Projects.IDpassport
            )
        )

        projects = db_session.execute(select_projects).all()
        idproj = projects[0][0] if projects else text("1=0")
        students = db_session.execute(
            text(
                """SELECT distinct
                CONCAT_WS(' ',s3.studentsFirstname, s3.studentsName, s3.studentsFathername),
                s3.studentsEmail,
                concat_ws(' - ', g.groupsname, concat(p3.rolesrole, ' - ', p3.rolesfunction))
        FROM	studentsinprojects s
                join projects p on ( p.IDprojects  = s.IDprojects )
                join passportofprojects p2 on ( p2.IDpassport = p.IDpassport )
                join students s3 on ( s3.IDstudents = s.IDstudents  )
                join `groups` g on ( g.idgroups = s3.idgroups )
                join rolesofprojects p3 on ( p3.idroles = s.idroles )
        WHERE 	p.idprojects = :idproj"""
            ),
            {"idproj": idproj},
        ).all()

        db_session.commit()
        return render_template("students_mail_student.html", users=students, projects=projects)


@pages.route("/admin/mailSheffPr", methods=["GET"])
def admin_mail_sheff_proj():
    if request.method == "GET":
        db_session = get_session()
        select = get_select()
        select_projects = (
            select(Projects.IDprojects, PassportOfProjects.passportName)
            .distinct()
            .join_from(
                PassportOfProjects, Projects, PassportOfProjects.IDpassport == Projects.IDpassport
            )
        )

        projects = db_session.execute(select_projects).all()
        idproj = projects[0][0] if projects else text("1=0")
        students = db_session.execute(
            text(
                """SELECT distinct
        CONCAT_WS(' ', s2.sheffprFirstname, s2.sheffprName, s2.sheffprFathername),
        s2.sheffprEmail
    FROM
        projects p
    join passportofprojects p2 on
        ( p2.IDpassport = p.IDpassport )
    join sheffofprojects s2  on
        ( s2.IDsheffpr = p2.IDsheffpr )
    WHERE	p.idprojects = :idproj"""
            ),
            {"idproj": idproj},
        ).all()

        db_session.commit()
        return render_template("students_mail_sheffpr.html", users=students, projects=projects)


@pages.route("/getStudentsMail", methods=["GET"])
def get_student_mail():
    idproj = request.args.get("idProject")
    db_session = get_session()
    students = db_session.execute(
        text(
            """SELECT distinct
                CONCAT_WS(' ',s3.studentsFirstname, s3.studentsName, s3.studentsFathername),
                s3.studentsEmail,
                concat_ws(' - ', g.groupsname, concat(p3.rolesrole, ' - ', p3.rolesfunction))
        FROM	studentsinprojects s
                join projects p on ( p.IDprojects  = s.IDprojects )
                join passportofprojects p2 on ( p2.IDpassport = p.IDpassport )
                join students s3 on ( s3.IDstudents = s.IDstudents  )
                join `groups` g on ( g.idgroups = s3.idgroups )
                join rolesofprojects p3 on (p3.idroles = s.idroles)
        WHERE 	p.idprojects = :idproj"""
        ),
        {"idproj": idproj},
    ).all()

    return jsonify([list(val) for val in students]), 200


@pages.route("/getSheffProjMail", methods=["GET"])
def get_sheff_proj_mail():
    idproj = request.args.get("idProject")
    db_session = get_session()
    students = db_session.execute(
        text(
            """SELECT distinct
        CONCAT_WS(' ', s2.sheffprFirstname, s2.sheffprName, s2.sheffprFathername),
        s2.sheffprEmail
    FROM
        projects p
    join passportofprojects p2 on
        ( p2.IDpassport = p.IDpassport )
    join sheffofprojects s2  on
        ( s2.IDsheffpr = p2.IDsheffpr )
    WHERE	p.idprojects = :idproj"""
        ),
        {"idproj": idproj},
    ).all()

    return jsonify([list(val) for val in students]), 200


def pagination(query, page=0):
    return query.limit(10).offset(page * 10)


def count_records(query, field):
    return query.with_only_columns(func.count(field))
