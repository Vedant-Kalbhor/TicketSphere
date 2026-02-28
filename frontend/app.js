// ============================================================
//  TicketSphere — Frontend Logic
//  Vanilla JS · connects to Flask backend on EC2
// ============================================================

// ── Config ───────────────────────────────────────────────────
// Change this to your EC2 public IP or domain when deploying.
// For local development keep it as http://localhost:5000
// Use an empty string for relative paths (best for same-server deployment)
const API_BASE_URL = ""; 
// const API_BASE_URL = "http://100.48.205.199:5000";


// ── DOM References ───────────────────────────────────────────
const eventsGrid     = document.getElementById("events-grid");
const emptyState     = document.getElementById("empty-state");
const errorState     = document.getElementById("error-state");
const modalOverlay   = document.getElementById("modal-overlay");
const modalClose     = document.getElementById("modal-close");
const modalEventName = document.getElementById("modal-event-name");
const bookingForm    = document.getElementById("booking-form");
const bookingEventId = document.getElementById("booking-event-id");
const seatIdInput    = document.getElementById("seat-id");
const userIdInput    = document.getElementById("user-id");
const seatMap        = document.getElementById("seat-map");
const summary        = document.getElementById("selection-summary");
const btnText        = document.getElementById("btn-text");
const btnLoader      = document.getElementById("btn-loader");
const submitBtn      = document.getElementById("booking-submit");
const toastContainer = document.getElementById("toast-container");

// ── Event icon pool (cosmetic) ───────────────────────────────
const EVENT_ICONS = ["🎵", "🎤", "💻", "🎭", "🏟️", "🎪", "📚", "🎬", "🎨", "🧑‍💻"];

function pickIcon(id) {
    return EVENT_ICONS[id % EVENT_ICONS.length];
}

// ── Format date nicely ───────────────────────────────────────
function formatDate(raw) {
    try {
        const d = new Date(raw);
        return d.toLocaleDateString("en-IN", {
            weekday: "short",
            year: "numeric",
            month: "short",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit",
        });
    } catch {
        return raw;
    }
}

// ── Fetch Events ─────────────────────────────────────────────
async function fetchEvents() {
    // Reset states
    emptyState.style.display = "none";
    errorState.style.display = "none";
    eventsGrid.innerHTML = `
        <div class="skeleton-card"></div>
        <div class="skeleton-card"></div>
        <div class="skeleton-card"></div>
    `;

    try {
        const res = await fetch(`${API_BASE_URL}/events`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const events = await res.json();

        if (!events || events.length === 0) {
            eventsGrid.innerHTML = "";
            emptyState.style.display = "block";
            return;
        }

        renderEvents(events);
    } catch (err) {
        console.error("Failed to fetch events:", err);
        eventsGrid.innerHTML = "";
        errorState.style.display = "block";
    }
}

// ── Render Event Cards ───────────────────────────────────────
function renderEvents(events) {
    eventsGrid.innerHTML = events
        .map((evt) => {
            // Backend returns rows as arrays: [id, title, venue, event_date]
            const [id, title, venue, eventDate] = evt;
            return `
                <article class="event-card" data-id="${id}">
                    <div class="event-card__icon">${pickIcon(id)}</div>
                    <h3 class="event-card__title">${escapeHtml(title)}</h3>
                    <div class="event-card__meta">
                        <span>📍 ${escapeHtml(venue)}</span>
                        <span>📅 ${formatDate(eventDate)}</span>
                    </div>
                    <div class="event-card__actions">
                        <button class="btn btn-primary" onclick="openBookingModal(${id}, '${escapeHtml(title)}')">
                            Book Now <span class="btn-arrow">→</span>
                        </button>
                    </div>
                </article>
            `;
        })
        .join("");
}

// ── HTML escape (safety) ─────────────────────────────────────
function escapeHtml(str) {
    const div = document.createElement("div");
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
}

// ── Booking Modal ────────────────────────────────────────────
function openBookingModal(eventId, eventTitle) {
    bookingEventId.value = eventId;
    modalEventName.textContent = eventTitle;
    bookingForm.reset();
    modalOverlay.classList.add("active");
    userIdInput.focus();
}

function closeModal() {
    modalOverlay.classList.remove("active");
}

modalClose.addEventListener("click", closeModal);
modalOverlay.addEventListener("click", (e) => {
    if (e.target === modalOverlay) closeModal();
});
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeModal();
});

// ── Submit Booking ───────────────────────────────────────────
bookingForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const eventId = parseInt(bookingEventId.value);
    const userId  = parseInt(userIdInput.value);
    const seatId  = parseInt(seatIdInput.value);

    if (!userId || !seatId) {
        showToast("Please fill in all fields.", "error");
        return;
    }

    // UI loading state
    btnText.textContent = "Processing…";
    btnLoader.style.display = "inline-block";
    submitBtn.disabled = true;

    try {
        const res = await fetch(`${API_BASE_URL}/book`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id: userId,
                event_id: eventId,
                seat_id: seatId,
            }),
        });

        const data = await res.json();

        if (res.ok) {
            closeModal();
            showToast(`🎉 Booking confirmed! ID: ${data.booking_id}`, "success");
        } else {
            showToast(data.message || "Booking failed. Try again.", "error");
        }
    } catch (err) {
        console.error("Booking error:", err);
        showToast("Network error — is the backend running?", "error");
    } finally {
        btnText.textContent = "Confirm Booking";
        btnLoader.style.display = "none";
        submitBtn.disabled = false;
    }
});

// ── Toast Notifications ──────────────────────────────────────
function showToast(message, type = "info") {
    const toast = document.createElement("div");
    toast.className = `toast toast--${type}`;
    toast.textContent = message;
    toastContainer.appendChild(toast);

    // Auto-dismiss after 4s
    setTimeout(() => {
        toast.classList.add("fade-out");
        toast.addEventListener("animationend", () => toast.remove());
    }, 4000);
}

// ── Init ─────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
    fetchEvents();
});
