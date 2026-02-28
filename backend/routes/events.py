from flask import Blueprint, jsonify
from db import get_connection

events_bp = Blueprint('events', __name__)

@events_bp.route("/events", methods=["GET"])
def get_events():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, venue, event_date FROM events")
    rows = cur.fetchall()
    conn.close()

    return jsonify(rows)

@events_bp.route("/events/<int:event_id>/seats", methods=["GET"])
def get_seats(event_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, seat_number, status FROM seats WHERE event_id=%s ORDER BY id", (event_id,))
    rows = cur.fetchall()
    conn.close()

    return jsonify(rows)
