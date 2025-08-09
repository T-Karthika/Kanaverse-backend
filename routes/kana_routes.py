# routes/kana_routes.py
from flask import Blueprint, jsonify, abort
import os, json

# /api/kana is a nice, self‑documenting prefix
kana_bp = Blueprint("kana", __name__, url_prefix="/api/kana")

# Absolute path to …/data/kana
BASE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "kana",
)

# Valid path parts so we can 400 on typos
VALID_SCRIPTS = {"hiragana", "katakana"}
VALID_CATEGORIES = {"basic", "dakuten", "handakuten", "yoon"}


def load_json(script: str, category: str):
    """Return JSON from <script>_<category>.json or 404."""
    filename = f"{script}_{category}.json"
    file_path = os.path.join(BASE_PATH, filename)
    if not os.path.isfile(file_path):
        abort(404, description=f"{filename} not found")
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


@kana_bp.route("/<script>/<category>", methods=["GET"])
def get_kana(script: str, category: str):
    """
    GET /api/kana/<script>/<category>
       script   -> hiragana | katakana
       category -> basic | dakuten | handakuten | yoon
    """
    script = script.lower()
    category = category.lower()

    if script not in VALID_SCRIPTS or category not in VALID_CATEGORIES:
        abort(400, description="Invalid script or category")

    return jsonify(load_json(script, category))
