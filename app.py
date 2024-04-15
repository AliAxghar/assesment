import json
from flask import Config, Flask, jsonify, render_template, request
from question1.read_data import fetch_raw_data_from_csv
from flask_sqlalchemy import SQLAlchemy
from models import PointTable
from models import db
import csv
import os

app = Flask(
    __name__,
    static_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), "static"),
)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/alphamaster"

db.init_app(app)

sorted_items = []


@app.route("/")
def index():
    return render_template("index.html")


def serialize_data(data):
    return {
        "email": data.email,
        "referral": data.referral,
        "nodes": [serialize_data(node) for node in data.nodes],
    }


def prepare_data(raw_data):
    for data in raw_data:
        if not data.referral:
            sorted_items.append(data)
        else:
            check_nodes(data, sorted_items)


def is_email_unique(email, object_list):
    return not any(obj.email == email for obj in object_list)


def check_nodes(data_to_insert, data_items):
    for item in data_items:
        if item.nodes and item.email != data_to_insert.referral:
            check_nodes(data_to_insert, item.nodes)
        else:
            if item.email == data_to_insert.referral:
                if not item.nodes:
                    item.nodes = []
                    item.nodes.append(data_to_insert)
                else:
                    if is_email_unique(data_to_insert.email, item.nodes):
                        item.nodes.append(data_to_insert)

            else:
                check_nodes(data_to_insert, item.nodes)


@app.route("/submit_form", methods=["POST"])
def submit_form():
    error = False
    msg = ""
    email = request.form.get("email")
    question = request.form.get("question")
    if question == "question1":
        raw_data = fetch_raw_data_from_csv("client.csv")
        prepare_data(raw_data)
        sorted_data = [serialize_data(item) for item in sorted_items]
        data = [
            next(
                (item for item in sorted_data if item["email"] == email),
                {"email": email, "referral": "", "nodes": []},
            )
        ]
        text_template = app.jinja_env.get_template("question1.html")
        html = text_template.render(data=data)
        return jsonify({"error": False, "msg": "success", "question": 1, "data": html})
    elif question == "question2":
        data = PointTable.query.filter_by(email=email).first()
        if not data:
            return jsonify(
                {"error": True, "msg": "User does not exist.", "question": 2}
            )
        else:
            text_template = app.jinja_env.get_template("question2.html")
            html = text_template.render(data=data)
            return jsonify(
                {"error": False, "msg": "success", "question": 2, "data": html}
            )
    return jsonify({"error": error, "msg": msg})


def read_csv(file_path):
    # Read data from CSV file, skipping the first row
    with open(file_path, "r", newline="") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first row
        return list(reader)


if __name__ == "__main__":
    app.run(debug=True)
