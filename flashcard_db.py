import sqlite3

DB_NAME = "flashcards.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS flashcards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        deck TEXT,
        subject TEXT,
        question TEXT,
        answer TEXT
    )
    """)

    # Migrate existing DB: add deck column if it's missing
    c.execute("PRAGMA table_info(flashcards)")
    columns = [row[1] for row in c.fetchall()]
    if "deck" not in columns:
        c.execute("ALTER TABLE flashcards ADD COLUMN deck TEXT DEFAULT ''")

    conn.commit()
    conn.close()


def add_card(deck, subject, question, answer):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    INSERT INTO flashcards (deck, subject, question, answer)
    VALUES (?, ?, ?, ?)
    """, (deck, subject, question, answer))

    conn.commit()
    conn.close()


def get_all_cards(deck=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    if deck:
        c.execute("SELECT * FROM flashcards WHERE deck = ?", (deck,))
    else:
        c.execute("SELECT * FROM flashcards")

    rows = c.fetchall()
    conn.close()
    return rows


def get_all_decks():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT DISTINCT deck FROM flashcards WHERE deck != '' ORDER BY deck")
    rows = [row[0] for row in c.fetchall()]

    conn.close()
    return rows
def delete_deck(deck):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM flashcards WHERE deck = ?", (deck,))
    conn.commit()
    conn.close()
