from flask import Flask
from flask_cors import CORS
from routes.events import events_bp
from routes.booking import booking_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(events_bp)
app.register_blueprint(booking_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
