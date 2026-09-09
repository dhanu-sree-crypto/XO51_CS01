from database import init_db, log_request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from authorization import authorize_request
init_db()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AuthRequest(BaseModel):
    user_intent: str
    tool: str
    operation: str
    source: str
    risk: str


@app.get("/")
def home():
    return {
        "message": "AuthGuard Backend is Running"
    }


@app.post("/authorize")
def authorize(request: AuthRequest):
    decision = authorize_request(
        request.source.lower(),
        request.risk.lower()
    )
    log_request(
        request.user_intent,
        request.tool,
        request.operation,
        request.source,
        request.risk,
        decision
    )

    return {
        "decision": decision,
        "reason": {
            "ALLOW": "The action is within the permitted scope and no significant authorization conflict was detected.",
            "DENY": "The requested action originates from an untrusted source and has high security impact.",
            "ESCALATE": "This operation requires additional authorization before execution."
        }[decision]
    }
@app.get("/logs")
def get_logs():
    import sqlite3

    conn = sqlite3.connect("authguard.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, user_intent, tool, operation, source, risk, decision
        FROM authorization_logs
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return {
        "logs": [
            {
                "id": row[0],
                "user_intent": row[1],
                "tool": row[2],
                "operation": row[3],
                "source": row[4],
                "risk": row[5],
                "decision": row[6]
            }
            for row in rows
        ]
    }
@app.get("/stats")
def get_stats():
    import sqlite3

    conn = sqlite3.connect("authguard.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM authorization_logs")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM authorization_logs WHERE decision='ALLOW'")
    allowed = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM authorization_logs WHERE decision='DENY'")
    denied = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM authorization_logs WHERE decision='ESCALATE'")
    escalated = cursor.fetchone()[0]

    conn.close()

    return {
        "total_requests": total,
        "allowed": allowed,
        "denied": denied,
        "escalated": escalated
    }