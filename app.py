from flask import Flask, session, request
from dotenv import load_dotenv
from pathlib import Path
from os import getenv, getcwd, path
import os
from flask_mail import Mail, Message

from models.database import init_db
from routes import pages

load_dotenv()
FULL_PATH_FOLDER = Path(getcwd(), "static", "files")
UPLOAD_FOLDER = Path("/static", "files")
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "prsystemivt@gmail.com"
app.config["MAIL_DEFAULT_SENDER"] = "prsystemivt@gmail.com"
app.config["MAIL_PASSWORD"] = "zfmropauluojkfhi"
mail = Mail(app)
app.register_blueprint(pages)
init_db()
app.secret_key = os.urandom(20).hex()


@app.route("/sendmailtoadmin", methods=["POST"])
def sheff_org_send_mail():
    if request.method == "POST":
        upload_file = request.files.get("files")
        subject = request.form.get("subject")
        message = request.form.get("message")
        admin = request.form.get("admin")
        msg = Message(subject, recipients=[admin])
        msg.body = message
        if upload_file:
            file_path = path.join("documents", upload_file.filename)
            upload_file.save(file_path)
            with open(file_path, encoding="utf-8") as file:
                msg.attach(file_path, upload_file.name, file.read())
        msg.body += f"\n\n Данное сообщение было создано в информационной системе сопровождения проектной деятельности кафедры ИВТ пользователем {' '.join(session['fullName'])} - {session['pos']}.  В дальнейшем отправляйте почту на {session['email']}"
        mail.send(msg)
        return "Сообщение отправлено", 200


if __name__ == "__main__":
    app.run(debug=True, port=(getenv("PORT") or 5000))
