# routes/minigames.py
from flask import Blueprint, jsonify, request, abort
import os, json, random

mini_games = Blueprint("mini_games", __name__, url_prefix="/api/mini-games")

# Path to kana JSON files: backend/data/kana/*.json
KANA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "kana"
)

# Allowed kana sets
VALID_KANA_SETS = {
    "hiragana_basic",
    "hiragana_dakuten",
    "hiragana_handakuten",
    "hiragana_yoon",
    "katakana_basic",
    "katakana_dakuten",
    "katakana_handakuten",
    "katakana_yoon"
}


def load_kana_data(kana_set: str):
    """Load kana data from file or return 404."""
    if kana_set not in VALID_KANA_SETS:
        abort(400, description=f"Invalid kana set: {kana_set}")

    file_path = os.path.join(KANA_PATH, f"{kana_set}.json")
    if not os.path.isfile(file_path):
        abort(404, description=f"{kana_set}.json not found")

    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


@mini_games.route("/kana-tile", methods=["GET"])
def kana_tile_game():
    """
    GET /api/mini-games/kana-tile?set=hiragana_basic
    If no set is provided, choose a random one from VALID_KANA_SETS.
    """
    kana_set = request.args.get("set")

    # If no set provided, pick a random one
    if not kana_set:
        kana_set = random.choice(list(VALID_KANA_SETS))

    kana_data = load_kana_data(kana_set)

    if not kana_data:
        abort(400, description="Empty kana set")

    correct = random.choice(kana_data)
    correct_kana = correct["kana"]
    romaji = correct["romaji"]

    # Build 4 unique answer options
    options = [correct_kana]
    while len(options) < 4:
        choice = random.choice(kana_data)["kana"]
        if choice not in options:
            options.append(choice)

    random.shuffle(options)

    return jsonify({
        "set": kana_set,  # return which set was used for debugging
        "correct": correct_kana,
        "romaji": romaji,
        "options": options
    })
