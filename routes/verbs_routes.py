from flask import Blueprint, jsonify
import os, json

verbs_bp = Blueprint("verbs", __name__, url_prefix="/api/verbs")

BASE_PATH = "data/verbs"

def load_json(filename):
    path = os.path.join(BASE_PATH, filename)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {"error": "File not found"}

# 📘 Basic Verbs
@verbs_bp.route("/basic")
def get_basic_verbs():
    return jsonify(load_json("basics.json"))

# 📗 JLPT N5 Verbs
@verbs_bp.route("/jlpt_n5")
def get_jlpt_n5_verbs():
    return jsonify(load_json("jlpt_n5.json"))

# 📙 JLPT N4 Verbs
@verbs_bp.route("/jlpt_n4")
def get_jlpt_n4_verbs():
    return jsonify(load_json("jlpt_n4.json"))

# 🛠️ Verb Conjugation Practice
@verbs_bp.route("/conjugations")
def get_conjugation_practice():
    return jsonify(load_json("conjugations.json"))
