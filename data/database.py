import aiosqlite


class DataBase:

    def __init__(self, name: str, table: str) -> None:
        self.name = f"data/{name}"
        self.table = table
        
    async def create_table(self) -> None:
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = """
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(20),
                age INTEGER(2),
                city VARCHAR(255),
                sex INTEGER(1),
                look_for INTEGER(1),
                about TEXT(500),
                photo VARCHAR(255)
            )
            """
            
            await cursor.executescript(query)
            await db.commit()

    async def insert(self, data) -> None:
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            await cursor.execute(
                """
                INSERT INTO users(
                    name,
                    age,
                    city,
                    sex,
                    look_for,
                    about
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                data
            )
            await db.commit()

            x = await cursor.execute("SELECT * FROM users")
            y = await x.fetchall()
            for i in y:
                print(i)