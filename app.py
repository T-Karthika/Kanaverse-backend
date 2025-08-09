from flask import Flask
from flask_cors import CORS
import os

# Create the Flask app
app = Flask(__name__)
CORS(app)

# Create temp directory for TTS
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

# ─── Register blueprints ───
from routes.kana_routes import kana_bp
from routes.kanji_routes import kanji_bp
from routes.verbs_routes import verbs_bp
from routes.phrases_routes import phrases_bp
from routes.practice_routes import practice_bp
from routes.tts_route import tts_bp
from routes.quiz_routes import quiz_bp
from routes.minigames import mini_games


# ⚠️ Do NOT give url_prefix here if it's already in the Blueprint constructor
app.register_blueprint(kana_bp)
app.register_blueprint(kanji_bp)
app.register_blueprint(verbs_bp)
app.register_blueprint(phrases_bp)
app.register_blueprint(practice_bp)
app.register_blueprint(tts_bp)
app.register_blueprint(quiz_bp)
app.register_blueprint(mini_games)

# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=5000)
