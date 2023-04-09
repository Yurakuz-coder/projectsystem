from datetime import datetime, date
from os import path
import hashlib
import locale
from docxtpl import DocxTemplate
from flask import Blueprint, render_template, request, redirect, session, send_file
from sqlalchemy import text
from models.models import Sheffofprojects, Organizations, Shefforganizations, Contracts
from models.database import get_session, get_select

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
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
        return render_template("organization.html", shefforg=shefforg, organizations=organizations, orgsheff=orgsheff)
    if request.method == "POST":
        fio_filters = request.form["fioFilters"]
        org_filters = request.form["orgFilters"]
        yuradress_filters = request.form["yuradressFilters"]
        where_fio_filters = (
            Shefforganizations.FullName.ilike("%" + fio_filters + "%") if fio_filters else text("1=1")
        )
        where_org_filters = (
            Organizations.orgName.ilike("%" + org_filters + "%") if org_filters else text("1=1")
        )
        where_yuradress_filters = (
            Organizations.orgYuraddress.ilike("%" + yuradress_filters + "%") if yuradress_filters else text("1=1")
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
        return render_template("resultTableOrg.html", shefforg=shefforg, organizations=organizations, orgsheff=orgsheff)


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
        db_sessions.query(Organizations).filter(
            Organizations.IDorg == idorg
        ).delete()
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
        npr = (db_sessions.query(Organizations).filter(Organizations.IDorg == idorg).first())
        if str(idsheforg) != "":
            npr.IDshefforg = int(idsheforg)
        if str(name) != "":
            npr.orgName = str(name)
        if str(yur) != "":
            npr.orgYuraddress= str(yur)
        if str(adres) != "":
            npr.orgPostaddress = str(adres)
        if str(em) != "":
            npr.orgEmail = str(em)
        if str(phone) != "":
            npr.orgPhone = str(phone)
        db_sessions.commit()
        return redirect("/admin/organization")


@pages.route("/admin/contracts", methods=["GET", "POST"])  # Договоры об организации проектного обучения
def route_contracts():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        select_org = select(Organizations).order_by(Organizations.orgName)
        select_contracts = select(Contracts).order_by(Contracts.IDcontracts)
        contracts = db_sessions.execute(select_contracts).all()
        organizations = db_sessions.execute(select_org).all()

        return render_template("contracts.html", contracts=contracts, organizations=organizations)
    if request.method == "POST":
        date_filters = request.form["dateContractFilter"]
        org_filters = request.form["orgFilters"]
        number_filters = request.form["numberContractFilter"]
        where_org_filters = (
            Organizations.orgName.ilike("%" + org_filters + "%") if org_filters else text("1=1")
        )
        where_date_filters = (
            Contracts.contractsStart.ilike(date_filters) if date_filters else text("1=1")
        )
        where_number_filters = (
            Contracts.contractsNumber.ilike("%" + number_filters + "%") if number_filters else text("1=1")
        )
        select = get_select()
        db_sessions = get_session()
        select_contracts = (
            select(
                Contracts
                )
                .join(Organizations)
                .where(where_number_filters)
                .where(where_date_filters)
                .where(where_org_filters)
                .order_by(Contracts.IDcontracts)
        )
        contracts = db_sessions.execute(select_contracts).all()
        return render_template("resultTableContracts.html", contracts=contracts)

@pages.route("/admin/addContract", methods=["POST"])  # добавление организации
def add_contract():
    if request.method == "POST":
        db_sessions = get_session()
        id_org = int(request.form["addorg"])
        contract_number = int(request.form["contractNumber"])
        contract_start_date = datetime.strptime(request.form["contractStart"], '%Y-%m-%d').date()
        contract_end_date = datetime.strptime(request.form["contractEnd"], '%Y-%m-%d').date()
        add = Contracts(
            IDorg=id_org,
            contractsNumber=contract_number,
            contractsStart=contract_start_date,
            contractsFinish=contract_end_date,
            contractsPattern='test',
            contractsFull='full'
        )
        db_sessions.add(add)
        db_sessions.commit()
        return redirect("/admin/contracts")


@pages.route("/admin/delContract", methods=["POST"])  # удаление организации
def del_contract():
    if request.method == "POST":
        db_sessions = get_session()
        id_contract = int(request.form["delContract"])
        db_sessions.query(Contracts).filter(
            Contracts.IDcontracts == id_contract
        ).delete()
        db_sessions.commit()
        return redirect("/admin/contracts")


@pages.route("/admin/modifyContract", methods=["POST"])  # редактирование организации
def modify_contract():
    if request.method == "POST":
        db_sessions = get_session()
        id_contract = int(request.form["modifyContract"])
        id_org = int(request.form["addorg"])
        contract_number = int(request.form["contractNumber"])
        contract_start_date = str(request.form["contractStart"])
        contract_end_date = str(request.form["contractEnd"])
        npr = (db_sessions.query(Contracts).filter(Contracts.IDcontracts == id_contract).first())
        if str(id_org) != "":
            npr.IDorg = int(id_org)
        if str(contract_number) != "":
            npr.contractsNumber = int(contract_number)
        if str(contract_start_date) != "":
            npr.contractsStart= str(contract_start_date)
        if str(contract_end_date) != "":
            npr.contractsFinish = str(contract_end_date)
        db_sessions.commit()
        return redirect("/admin/contracts")

@pages.route('/getDocument', methods=['GET'])
def send_document():
    args = request.args
    id_contract = args.get('idContract')
    db_sessions = get_session()
    contract = db_sessions.query(Contracts).filter(Contracts.IDcontracts == id_contract).first()
    context = {}
    if not contract:
        return
    context['contract_number'] = contract.contractsNumber
    context['org_name'] = contract.organizations.orgName
    context['contract_end_date'] = contract.contractsFinish.strftime("%d %B %Y")
    context['org_ur_address'] = contract.organizations.orgYuraddress
    context['org_postal_address'] = contract.organizations.orgPostaddress
    context['contract_start_date'] = contract.contractsStart.strftime("«%d» %B %Y г.")
    filename = 'Договор ' + str(contract.contractsNumber) + '_' + date.today().strftime("%d_%B_%Y") + '.doc'
    file_path = path.join('documents', filename)
    doc = DocxTemplate('./documents/contract_template.docx')

    doc.render(context)

    doc.save(file_path)

    return send_file(file_path, mimetype='multipart/form-data', as_attachment=True)



