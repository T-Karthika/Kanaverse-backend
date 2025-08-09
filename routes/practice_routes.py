from flask import Blueprint, jsonify
import os, json

practice_bp = Blueprint("practice", __name__, url_prefix="/api/practice")

BASE_PATH = "data/practice"


def load_json(filename: str):
    """Return parsed JSON or an error dict if the file is missing."""
    path = os.path.join(BASE_PATH, filename)
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": f"{filename} not found"}


# ────────────────────────────────────────────────
# 📚  Level‑based practice routes
# ────────────────────────────────────────────────
@practice_bp.route("/level1")
def get_level1():
    return jsonify(load_json("level1.json"))


@practice_bp.route("/level2")
def get_level2():
    return jsonify(load_json("level2.json"))


@practice_bp.route("/level3")
def get_level3():
    return jsonify(load_json("level3.json"))


# ────────────────────────────────────────────────
# 📝  JLPT quiz routes
# ────────────────────────────────────────────────
@practice_bp.route("/n4quiz")
def get_n4_quiz():
    return jsonify(load_json("n4_quiz.json"))


@practice_bp.route("/n5quiz")
def get_n5_quiz():
    return jsonify(load_json("n5_quiz.json"))
