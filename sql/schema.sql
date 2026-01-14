CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT UNIQUE
);

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    title TEXT,
    venue TEXT,
    event_date TIMESTAMP,
    total_seats INT
);

CREATE TABLE seats (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id),
    seat_number TEXT,
    status TEXT CHECK (status IN ('AVAILABLE', 'BOOKED'))
);

CREATE TABLE bookings (
    id UUID PRIMARY KEY,
    user_id INT REFERENCES users(id),
    event_id INT REFERENCES events(id),
    seat_id INT REFERENCES seats(id),
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
