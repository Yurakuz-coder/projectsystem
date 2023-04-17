from datetime import datetime, date
from os import path, remove
import hashlib
import locale
from docxtpl import DocxTemplate
from flask import Blueprint, render_template, request, redirect, session, send_file
from sqlalchemy import text
from models.models import Sheffofprojects, Organizations, Shefforganizations, Contracts, Specializations, Formstuding, Groups, Students, Studentsingroups
from models.database import get_session, get_select
from pymorphy2 import MorphAnalyzer
import csv

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
        select_contracts = select(Contracts).order_by(Contracts.contractsNumber, Contracts.contractsStart)
        select_contracts_order = select(Contracts).join(Organizations).order_by(Organizations.orgName, Contracts.contractsNumber, Contracts.contractsStart)
        contracts = db_sessions.execute(select_contracts).all()
        organizations = db_sessions.execute(select_org).all()
        contracts_order = db_sessions.execute(select_contracts_order).all()

        return render_template("contracts.html", contracts=contracts, organizations=organizations, contracts_order=contracts_order)
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
    select = text('''SELECT p.contractsNumber, o.orgName, p.contractsFinish, o.orgYuraddress, o.orgPostaddress, p.contractsStart, s.shefforgDoc, s.shefforgFirstname as firstName, s.shefforgName as name, s.shefforgFathername as surname, s.shefforgPositions
        FROM projectsudycontracts p
            inner join organizations o on ( o.IDorg = p.IDorg )
            inner join shefforganizations s on ( s.IDshefforg = o.IDshefforg)
        WHERE
            p.IDcontracts = :id_contract
        ''')

    contract = db_sessions.execute(select, {'id_contract': id_contract}).first()

    if not contract:
        return

    context = {}
    context["contract_number"] = contract[0]
    context["org_name"] = contract[1]
    context["contract_end_date"] = get_date(contract[2].strftime("%d.%m.%Y"))
    context["org_ur_address"] = contract[3]
    context["org_postal_address"] = contract[4]
    context["contract_start_date"] = get_date(contract[5].strftime("%d.%m.%Y")) + ' г.'
    document = [value for value in morph.parse(contract[6]) if value.tag.number == 'sing' and value.tag.POS == 'NOUN' ][0].inflect({'gent'}).word
    first_name = [value for value in morph.parse(contract[7]) if value.tag.number == 'sing' and value.tag.POS == 'NOUN' ][0].inflect({'gent'}).word
    name = [value for value in morph.parse(contract[8]) if value.tag.number == 'sing' and value.tag.POS == 'NOUN' ][0].inflect({'gent'}).word
    sur_name = [value for value in morph.parse(contract[9]) if value.tag.number == 'sing' and value.tag.POS == 'NOUN' ][0].inflect({'gent'}).word
    position = [value for value in morph.parse(contract[10]) if value.tag.number == 'sing' and value.tag.POS == 'NOUN' ][0].inflect({'gent'}).word
    context["document"] = document
    context["fio"] = contract[7] + ' ' + contract[8][0] + '. ' + contract[9][0] + '.'
    context["position"] = contract[10].capitalize()
    context["position_and_fio"] = position + ' ' + first_name.capitalize() + ' ' + name.capitalize() + ' ' + sur_name.capitalize()
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
    month_list = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня',
           'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']
    date_list = date.split('.')
    return ('«' + date_list[0] + '» ' +
        month_list[int(date_list[1]) - 1] + ' ' +
        date_list[2])


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


@pages.route( "/admin/specializations", methods=["GET", "POST"])  # Специализации
def specializations():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        select_spec = select(Specializations).order_by(Specializations.specShifr, Specializations.specNapravlenie, Specializations.specNapravlennost)
        specializations = db_sessions.execute(select_spec).all()
        return render_template("specializations.html", specializations=specializations)
    if request.method == "POST":
        shifr_filters = request.form.get("shifrFilters")
        napr_filters = request.form.get("naprFilters")
        where_shifr_filters = (
            Specializations.specShifr.ilike("%" + shifr_filters + "%") if shifr_filters else text("1=1")
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
            .order_by(Specializations.specShifr, Specializations.specNapravlenie, Specializations.specNapravlennost)
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


@pages.route( "/admin/groups", methods=["GET", "POST"])  #Группы
def groups():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        select_tablegr = select(Groups, Formstuding.form_stName, Specializations.FullSpec).join(Formstuding).join(Specializations).order_by(Specializations.FullSpec, Groups.groupsName, Groups.groupsYear, Formstuding.form_stName)
        select_formst = select(Formstuding).order_by(Formstuding.form_stName)
        select_groups = select(Groups).order_by(Groups.groupsName)
        select_spec = select(Specializations).order_by(Specializations.specShifr, Specializations.specNapravlenie, Specializations.specNapravlennost)
        formst = db_sessions.execute(select_formst).all()
        specializations = db_sessions.execute(select_spec).all()
        groups = db_sessions.execute(select_groups).all()
        groups_table = db_sessions.execute(select_tablegr).all()
        return render_template("groups.html", formst=formst, specializations=specializations, groups=groups, groups_table=groups_table)

    if request.method == "POST":
        form_education = request.form.get("formEducation")
        direct_study = request.form.get("directStudy")
        year_study = request.form.get("yearStudy")
        where_form_education = (
            Formstuding.form_stName.ilike("%" + form_education + "%") if form_education else text("1=1")
        )
        where_direct_study = (
            Specializations.specNapravlenie.ilike("%" + direct_study + "%")
            if direct_study
            else text("1=1")
        )
        where_year_study = (
            Groups.groupsYear.ilike("%" + year_study + "%")
            if year_study
            else text("1=1")
        )
        select = get_select()
        db_sessions = get_session()
        select_group = (
            select(Groups, Formstuding.form_stName, Specializations.FullSpec).join(Formstuding).join(Specializations).where(where_form_education).where(where_direct_study).where(where_year_study).order_by(Specializations.FullSpec, Groups.groupsName, Groups.groupsYear, Formstuding.form_stName)
        )
        groups_table = db_sessions.execute(select_group).all()
        return render_template("resultTableGroups.html", groups_table=groups_table)


@pages.route( "/admin/addGroup", methods=["POST"])  #Добавить группы
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


@pages.route( "/admin/delGroup", methods=["POST"])  #Удалить группы
def delgroups():
    db_sessions = get_session()
    id_gr = int(request.form["delGroup"])
    db_sessions.query(Groups).filter(Groups.IDgroups == id_gr).delete()
    db_sessions.commit()
    return redirect("/admin/groups")


@pages.route( "/admin/modifyGroup", methods=["POST"])  #Редактировать группы
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


#Загрузка csv в специализации
@pages.route('/admin/csvSpec', methods=['POST'])
def insert_csv_spec():
    try:
        upload_file = request.files.get("file")
        file_path = path.join("documents", upload_file.filename)
        upload_file.save(file_path)
        with open(file_path, encoding='utf-8') as file:
            db_sessions = get_session()
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                add = Specializations(
                    specShifr=row['Шифр'],
                    specNapravlenie=row['Направление'],
                    specNapravlennost=row['Направленность'],
                )
                db_sessions.add(add)
                db_sessions.commit()
        return '', 200
    finally:
        remove(file_path)

#Загрузка csv в группы
@pages.route('/admin/csvGroup', methods=['POST'])
def insert_csv_group():
    try:
        upload_file = request.files.get("file")
        file_path = path.join("documents", upload_file.filename)
        upload_file.save(file_path)
        with open(file_path, encoding='utf-8') as file:
            db_sessions = get_session()
            select = get_select()
            reader = csv.DictReader(file, delimiter=";")
            for row in reader:
                napr = row['Направление'].split("-")
                idform_st = db_sessions.execute(select(Formstuding.IDform_st).where(Formstuding.form_stName == row['Форма обучения'])).first()
                idspec = db_sessions.execute(select(Specializations.IDspec).where(Specializations.specShifr == napr[0]).where(Specializations.specNapravlenie == napr[1]).where(Specializations.specNapravlennost == napr[2])).first()
                add = Groups(
                    groupsName=row['Название группы'],
                    groupsYear=row['Год набора'],
                    IDform_st=idform_st[0],
                    IDspec=idspec[0],
                )
                db_sessions.add(add)
                db_sessions.commit()
        return '', 200
    finally:
        remove(file_path)


@pages.route( "/admin/students", methods=["GET", "POST"])  #Студенты
def students():
    if request.method == "GET":
        select = get_select()
        db_sessions = get_session()
        select_redstud = select(Students.IDstudents, Students.FullName, Students.studentsStudbook).order_by(Students.FullName)
        select_studnotgroup = (select(Students.IDstudents, Students.FullName, Students.studentsStudbook, Studentsingroups)
                               .join_from(
            Students,
            Studentsingroups,
            Studentsingroups.IDstudents == Students.IDstudents,
            isouter=True,
        )
                               .filter(Studentsingroups.IDgroups.is_(None))
                               .order_by(Students.FullName)
                               )
        studnotgroup = db_sessions.execute(select_studnotgroup).all()
        redstud = db_sessions.execute(select_redstud).all()
        return render_template("students.html", studnotgroup=studnotgroup, redstud=redstud)


@pages.route( "/admin/addStudents", methods=["POST"])  #Добавить студента
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
        passw = hashlib.md5(password.encode())
        passw = passw.hexdigest()
        add = Students(
            studentsFirstname=fname,
            studentsName=name,
            studentsFathername=lname,
            studentsStudbook=book,
            studentsPhone=tel,
            studentsEmail=em,
            Login=login,
            Pass=passw,
        )
        db_sessions.add(add)
        db_sessions.commit()
        return redirect("/admin/students")


@pages.route( "/admin/delStudent", methods=["POST"])  #Удалить студента
def delstudents():
    db_sessions = get_session()
    id_st = int(request.form["delStudent"])
    db_sessions.query(Students).filter(Students.IDstudents == id_st).delete()
    db_sessions.commit()
    return redirect("/admin/students")


@pages.route( "/admin/modifyStudent", methods=["POST"])  #Редактировать студента
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
    if str(password) != "":
        password = hashlib.md5(password.encode())
        password = password.hexdigest()
        npr.Pass = str(password)
    db_sessions.commit()
    return redirect("/admin/students")
