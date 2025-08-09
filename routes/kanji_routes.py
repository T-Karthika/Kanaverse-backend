from flask import Blueprint, jsonify
import json, os

kanji_bp = Blueprint("kanji", __name__, url_prefix="/api/kanji")
BASE_PATH = "data/kanji/jlpt"

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def list_categories(level):
    level_path = os.path.join(BASE_PATH, level)
    if not os.path.exists(level_path):
        return []
    return [
        f.replace(".json", "")
        for f in os.listdir(level_path)
        if f.endswith(".json")
    ]

# ✅ Get list of categories
@kanji_bp.route("/n5")
def list_n5_categories():
    return jsonify(list_categories("n5"))

@kanji_bp.route("/n4")
def list_n4_categories():
    return jsonify(list_categories("n4"))

# ✅ Get kanji data by category
@kanji_bp.route("/n5/<category>")
def jlpt_n5(category):
    file_path = os.path.join(BASE_PATH, "n5", f"{category}.json")
    if os.path.exists(file_path):
        return jsonify(load_json(file_path))
    return jsonify({"error": "Category not found in N5"}), 404

@kanji_bp.route("/n4/<category>")
def jlpt_n4(category):
    file_path = os.path.join(BASE_PATH, "n4", f"{category}.json")
    if os.path.exists(file_path):
        return jsonify(load_json(file_path))
    return jsonify({"error": "Category not found in N4"}), 404
