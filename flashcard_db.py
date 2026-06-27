import sqlite3
from datetime import date, timedelta

DB_NAME = "flashcards.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS flashcards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        deck TEXT NOT NULL,
        subject TEXT NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        review_date TEXT DEFAULT '',
        interval INTEGER DEFAULT 1,
        ease REAL DEFAULT 2.5,
        repetitions INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def add_card(deck, subject, question, answer):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO flashcards
        (deck, subject, question, answer)
        VALUES (?, ?, ?, ?)
    """, (deck, subject, question, answer))

    conn.commit()
    conn.close()


def get_all_cards(deck=None):
    conn = get_connection()
    c = conn.cursor()

    if deck:
        c.execute("""
            SELECT
                id,
                deck,
                subject,
                question,
                answer,
                review_date,
                interval,
                ease,
                repetitions
            FROM flashcards
            WHERE deck=?
            ORDER BY id
        """, (deck,))
    else:
        c.execute("""
            SELECT
                id,
                deck,
                subject,
                question,
                answer,
                review_date,
                interval,
                ease,
                repetitions
            FROM flashcards
            ORDER BY id
        """)

    rows = c.fetchall()
    conn.close()
    return rows


def get_all_decks():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT DISTINCT deck
        FROM flashcards
        ORDER BY deck
    """)

    decks = [row["deck"] for row in c.fetchall()]

    conn.close()
    return decks


def delete_deck(deck):
    conn = get_connection()
    c = conn.cursor()

    c.execute("DELETE FROM flashcards WHERE deck=?", (deck,))

    conn.commit()
    conn.close()


def get_due_cards(deck):
    conn = get_connection()
    c = conn.cursor()

    today = date.today().isoformat()

    c.execute("""
        SELECT
            id,
            deck,
            subject,
            question,
            answer,
            review_date,
            interval,
            ease,
            repetitions
        FROM flashcards
        WHERE deck=?
        AND (review_date='' OR review_date<=?)
        ORDER BY id
    """, (deck, today))

    rows = c.fetchall()
    conn.close()
    return rows


def review_card(card_id, success):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT interval,ease,repetitions
        FROM flashcards
        WHERE id=?
    """, (card_id,))

    row = c.fetchone()

    interval = row["interval"]
    ease = row["ease"]
    reps = row["repetitions"]

    if success:
        reps += 1

        if reps == 1:
            interval = 1
        elif reps == 2:
            interval = 3
        else:
            interval = max(1, round(interval * ease))

        ease += 0.1

    else:
        reps = 0
        interval = 1
        ease = max(1.3, ease - 0.2)

    next_review = (date.today() + timedelta(days=interval)).isoformat()

    c.execute("""
        UPDATE flashcards
        SET
            interval=?,
            ease=?,
            repetitions=?,
            review_date=?
        WHERE id=?
    """, (
        interval,
        ease,
        reps,
        next_review,
        card_id
    ))

    conn.commit()
    conn.close()


def get_forecast_data():
    conn = get_connection()
    c = conn.cursor()

    today = date.today()

    forecast = {
        (today + timedelta(days=i)).isoformat(): 0
        for i in range(7)
    }

    c.execute("SELECT review_date FROM flashcards")

    for row in c.fetchall():
        review = row["review_date"]

        if not review:
            forecast[today.isoformat()] += 1
        elif review < today.isoformat():
            forecast[today.isoformat()] += 1
        elif review in forecast:
            forecast[review] += 1

    conn.close()

    return list(forecast.items())


def get_mastery_data():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT repetitions FROM flashcards")

    stats = {
        "New (0 reps)": 0,
        "Learning (1-3 reps)": 0,
        "Mastered (4+ reps)": 0,
    }

    for row in c.fetchall():
        reps = row["repetitions"]

        if reps == 0:
            stats["New (0 reps)"] += 1
        elif reps < 4:
            stats["Learning (1-3 reps)"] += 1
        else:
            stats["Mastered (4+ reps)"] += 1

    conn.close()

    return stats
