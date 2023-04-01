from flask import Flask, render_template, url_for, request, redirect, session, jsonify, abort, send_file
from flask.helpers import send_from_directory
from sqlalchemy import *
from sqlalchemy import MetaData, create_engine
from sqlalchemy import exc
from sqlalchemy.orm import create_session, aliased
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import re
import math
import hashlib
import os
import time
import json
import pathlib
import platform
import csv
import time
import shutil


if platform.system() == 'Windows':
    engine = create_engine('mysql+pymysql://root:@localhost:3306/projectsystem')
    FULL_PATH_FOLDER = pathlib.Path(os.getcwd(), 'static', 'files')
conn = engine.connect()
metadata = MetaData(bind=engine)
UPLOAD_FOLDER = pathlib.Path('/static', 'files')

Base = declarative_base()


class sheffofprojects(Base):
    __table__ = Table('sheffofprojects', metadata, autoload=True)


Session = sessionmaker(autocommit=True, autoflush=True, bind=engine)
sessions = Session()
app = Flask(__name__)
app.secret_key = os.urandom(20).hex()


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
