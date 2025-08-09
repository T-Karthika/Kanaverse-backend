from flask import Blueprint, jsonify
import os, json

phrases_bp = Blueprint("phrases", __name__, url_prefix="/api/phrases")

BASE_PATH = "data/phrases"

def load_json(filename):
    path = os.path.join(BASE_PATH, filename)
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {"error": "File not found"}

# 👋 Greetings
@phrases_bp.route("/greetings")
def get_greetings():
    return jsonify(load_json("greetings.json"))

# 🏫 Classroom phrases
@phrases_bp.route("/classroom")
def get_classroom_phrases():
    return jsonify(load_json("classroom.json"))

# 🏠 Daily-use phrases
@phrases_bp.route("/daily_use")
def get_daily_use_phrases():
    return jsonify(load_json("daily_use.json"))
