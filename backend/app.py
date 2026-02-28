from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.events import events_bp
from routes.booking import booking_bp
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

app.register_blueprint(events_bp)
app.register_blueprint(booking_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
