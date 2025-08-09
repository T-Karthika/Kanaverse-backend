# routes/quiz_routes.py
from flask import Blueprint, jsonify
import json, os, random, logging

quiz_bp = Blueprint("quiz", __name__, url_prefix="/api/quiz")

BASE_PATH = "data"            # adjust if your JSON lives elsewhere
MAX_PER_SET = 15              # how many questions per single‑topic quiz
DISTRACTOR_COUNT = 3          # number of wrong options


# ────────────────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────────────────
def load_json(path: str):
    """Return parsed JSON list or [] if file is missing/invalid."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except FileNotFoundError:
        logging.warning("JSON not found: %s", path)
        return []
    except json.JSONDecodeError as e:
        logging.error("Bad JSON (%s): %s", path, e)
        return []


def sample_distractors(pool: list, answer):
    """Return up to DISTRACTOR_COUNT choices that differ from answer."""
    pool = [x for x in pool if x != answer]
    k = min(DISTRACTOR_COUNT, len(pool))
    return random.sample(pool, k) if k else []


def generate_question_set(items: list, qtype: str) -> list:
    """Build a list of MCQ dicts from source items."""
    questions = []
    if not items:
        return questions

    for itm in random.sample(items, min(MAX_PER_SET, len(items))):
        if qtype == "kana":
            question = f"What is the romaji for '{itm['kana']}'?"
            answer   = itm["romaji"]
            pool     = [x["romaji"] for x in items]
        elif qtype == "kanji":
            question = f"What is the meaning of Kanji '{itm['kanji']}'?"
            answer   = itm["meaning"]
            pool     = [x["meaning"] for x in items]
        elif qtype == "verbs":
            question = f"What does '{itm['kana']}' mean?"
            # some verb lists store meaning under "meaning" (Eng)
            answer   = itm.get("meaning") or itm.get("english")
            pool     = [x.get("meaning") or x.get("english") for x in items]
        elif qtype == "phrases":
            jp_txt   = itm.get("japanese") or itm.get("kana") or itm.get("jp")
            en_txt   = itm.get("english")  or itm.get("meaning")
            question = f"What is the English meaning of '{jp_txt}'?"
            answer   = en_txt
            pool     = [
                x.get("english") or x.get("meaning")
                for x in items
                if x.get("english") or x.get("meaning")
            ]
        else:
            continue

        distractors = sample_distractors(pool, answer)
        options = distractors + [answer]
        random.shuffle(options)

        questions.append(
            {
                "question": question,
                "options": options,
                "answer": answer,
            }
        )

    return questions


# ────────────────────────────────────────────────────────────
# Single‑topic quizzes
# URLs:  /api/quiz/kana_basic   etc.
# ────────────────────────────────────────────────────────────
@quiz_bp.route("/kana_basic")
def quiz_kana():
    data = load_json(os.path.join(BASE_PATH, "kana", "hiragana_basic.json"))
    return jsonify(generate_question_set(data, "kana"))


@quiz_bp.route("/kanji_n5")
def quiz_kanji_n5():
    data = load_json(os.path.join(BASE_PATH, "kanji", "jlpt", "n5", "basics.json"))
    return jsonify(generate_question_set(data, "kanji"))


@quiz_bp.route("/verbs_n5")
def quiz_verbs_n5():
    data = load_json(os.path.join(BASE_PATH, "verbs", "jlpt_n5.json"))
    return jsonify(generate_question_set(data, "verbs"))


@quiz_bp.route("/phrases")
def quiz_phrases():
    data = load_json(os.path.join(BASE_PATH, "phrases", "greetings.json"))
    return jsonify(generate_question_set(data, "phrases"))


# ────────────────────────────────────────────────────────────
# Mixed quiz (up to 15 questions total)
# URL: /api/quiz/mixed
# ────────────────────────────────────────────────────────────
@quiz_bp.route("/mixed")
def quiz_mixed():
    sources = {
        "kana":    os.path.join(BASE_PATH, "kana",  "hiragana_basic.json"),
        "kanji":   os.path.join(BASE_PATH, "kanji", "jlpt", "n5", "basics.json"),
        "verbs":   os.path.join(BASE_PATH, "verbs", "jlpt_n5.json"),
        "phrases": os.path.join(BASE_PATH, "phrases", "greetings.json"),
    }

    combined = []
    for qtype, path in sources.items():
        items = load_json(path)
        subset = generate_question_set(items, qtype)
        if subset:
            # take up to 3 from each topic
            combined.extend(random.sample(subset, min(3, len(subset))))

    random.shuffle(combined)
    return jsonify(combined[:MAX_PER_SET])
