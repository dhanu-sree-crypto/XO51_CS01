import sqlite3

DB_NAME = "authguard.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS authorization_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_intent TEXT,
            tool TEXT,
            operation TEXT,
            source TEXT,
            risk TEXT,
            decision TEXT
        )
    """)

    conn.commit()
    conn.close()


def log_request(user_intent, tool, operation, source, risk, decision):
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        INSERT INTO authorization_logs
        (user_intent, tool, operation, source, risk, decision)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_intent,
        tool,
        operation,
        source,
        risk,
        decision
    ))

    conn.commit()
    conn.close()