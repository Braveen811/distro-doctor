import os
import duckdb

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "analytics.duckdb")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = duckdb.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS test_runs (
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            distro VARCHAR,
            success BOOLEAN,
            error_msg VARCHAR
        )
    """)
    conn.close()

def log_results(results):
    init_db()
    conn = duckdb.connect(DB_PATH)
    for distro, res in results.items():
        success = res.get("success", False)
        error = res.get("error", "")[:500]
        conn.execute(
            "INSERT INTO test_runs (distro, success, error_msg) VALUES (?, ?, ?)",
            [distro, success, error]
        )
    conn.close()

def get_analytics_summary():
    if not os.path.exists(DB_PATH):
        return "No historical analytics data yet."
    
    conn = duckdb.connect(DB_PATH)
    total_runs = conn.execute("SELECT COUNT(*) FROM test_runs").fetchone()[0]
    success_rate = conn.execute("SELECT (SUM(CAST(success AS INTEGER)) * 100.0 / COUNT(*)) FROM test_runs").fetchone()[0]
    most_fragile = conn.execute("SELECT distro, SUM(CAST(NOT success AS INTEGER)) as failures FROM test_runs GROUP BY distro ORDER BY failures DESC LIMIT 1").fetchone()
    conn.close()
    
    return {
        "total_runs": total_runs,
        "success_rate": round(success_rate or 0.0, 2),
        "most_fragile_distro": most_fragile[0] if most_fragile else "None"
    }