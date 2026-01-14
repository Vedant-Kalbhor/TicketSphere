from flask import Flask
from routes.events import events_bp
from routes.booking import booking_bp

app = Flask(__name__)

app.register_blueprint(events_bp)
app.register_blueprint(booking_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
