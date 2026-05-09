import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'shows.db')


async def init_db():
    async with aiosqlite.connect(DB_PATH, check_same_thread=False) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS follows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tvmaze_id INTEGER NOT NULL,
                show_name TEXT NOT NULL,
                season INTEGER,
                number INTEGER,
                episode_name TEXT,
                air_date TEXT
            )
        ''')
        await db.commit()


async def add_follow(tvmaze_id: int, show_name: str, season: int, number: int, episode_name: str, air_date: str):
    async with aiosqlite.connect(DB_PATH, check_same_thread=False) as db:
        await db.execute(
            '''INSERT INTO follows (tvmaze_id, show_name, season, number, episode_name, air_date)
               VALUES (?, ?, ?, ?, ?, ?)''',
            (tvmaze_id, show_name, season, number, episode_name, air_date)
        )
        await db.commit()


async def get_follows():
    async with aiosqlite.connect(DB_PATH, check_same_thread=False) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT * FROM follows ORDER BY air_date ASC') as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def delete_follow(follow_id: int):
    async with aiosqlite.connect(DB_PATH, check_same_thread=False) as db:
        await db.execute('DELETE FROM follows WHERE id = ?', (follow_id,))
        await db.commit()
