import psycopg2
from config import load_config


def get_connection():
    config = load_config()
    return psycopg2.connect(**config)


def create_tables():
    sql = """
    CREATE TABLE IF NOT EXISTS players (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS game_sessions (
        id SERIAL PRIMARY KEY,
        player_id INTEGER REFERENCES players(id),
        score INTEGER NOT NULL,
        level_reached INTEGER NOT NULL,
        played_at TIMESTAMP DEFAULT NOW()
    );
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)


def get_or_create_player(username):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO players (username)
                VALUES (%s)
                ON CONFLICT (username) DO NOTHING
            """, (username,))

            cur.execute("SELECT id FROM players WHERE username = %s", (username,))
            return cur.fetchone()[0]


def save_result(username, score, level):
    player_id = get_or_create_player(username)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO game_sessions (player_id, score, level_reached)
                VALUES (%s, %s, %s)
            """, (player_id, score, level))


def get_top_scores():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.username, g.score, g.level_reached, g.played_at
                FROM game_sessions g
                JOIN players p ON g.player_id = p.id
                ORDER BY g.score DESC
                LIMIT 10
            """)
            return cur.fetchall()


def get_personal_best(username):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT MAX(g.score)
                FROM game_sessions g
                JOIN players p ON g.player_id = p.id
                WHERE p.username = %s
            """, (username,))
            result = cur.fetchone()[0]
            return result if result is not None else 0