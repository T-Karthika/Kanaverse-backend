# routes/tts_route.py
from flask import Blueprint, send_file, abort
from gtts import gTTS
import hashlib, os, threading, time

tts_bp = Blueprint("tts", __name__, url_prefix="/api/tts")

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)


def delete_after_delay(path, delay=15):
    """Delete the cached mp3 after <delay> seconds."""
    def _delete():
        time.sleep(delay)
        if os.path.isfile(path):
            try:
                os.remove(path)
            except OSError:
                pass
    threading.Thread(target=_delete, daemon=True).start()


@tts_bp.route("/<path:text>")
def generate_audio(text: str):
    """
    GET /api/tts/<text>
    Works for single kana (あ) or full phrases (たべものがすきです).
    """
    if not text.strip():
        abort(400, description="Empty TTS request")

    # Use an MD5 hash for a safe, unique filename
    fname = hashlib.md5(text.encode("utf-8")).hexdigest() + ".mp3"
    fpath = os.path.join(TEMP_DIR, fname)

    # Generate only if not cached
    if not os.path.isfile(fpath):
        try:
            gTTS(text=text, lang="ja").save(fpath)
            delete_after_delay(fpath)
        except Exception as e:
            abort(500, description=f"TTS generation failed: {e}")

    return send_file(fpath, mimetype="audio/mpeg")
