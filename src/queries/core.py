from sqlalchemy import text, insert, select, update
from database import sync_engine, async_engine
from models import metadata_obj, workers_table

# def get_123_sync():
#     with sync_engine.connect() as conn:
#         print(f"{res.first()=}")
#         res = conn.execute(text("SELECT 1,2,3 union select 4,5,6"))

#async def get_123_async():
#    async with async_engine.connect() as conn:
#        res = await conn.execute(text("SELECT 1,2,3 union select 4,5,6"))
#        print(f"{res.first()=}")

# def create_tables():
#     sync_engine.echo = False
#     metadata_obj.drop_all(sync_engine)
#     metadata_obj.create_all(sync_engine)
#     sync_engine.echo = True

#async def create_tables():
#    async with async_engine.begin() as conn:
#        await conn.run_sync(metadata_obj.drop_all)
#        await conn.run_sync(metadata_obj.create_all)





class SyncCore:
    @staticmethod
    def insert_data():
        with sync_engine.connect() as conn:
            # stmt = """INSERT INTO workers (username) VALUES 
            #     ('Jack'),
            #     ('Michael');"""
            stmt = insert(workers_table).values(
                [
                    {"username": "Jack"},
                    {"username": "Michael"},
                ]
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def insert_workers():
        with sync_engine.connect() as conn:
            stmt = insert(workers_table).values(
                [
                    {"username": "Jack"},
                    {"username": "Michael"},
                ]
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_workers():
        with sync_engine.connect() as conn:
            query = select(workers_table)   # SELECT * FROM workers
            result = conn.execute(query)
            workers = result.all()
            print("\n     vvv select запрос vvv       ")
            print(f"Таблица: {workers=}")

    @staticmethod
    def update_worker(worker_id: int = 2, new_username: str = "Misha"):
        """
        Код в формате Core более громоздок, но работает быстрее, т.к. требует меньше запросов к БД.
        Но этот подход может показаться более сложным, т.к. являет собой SQL-запросы, но с некоторым уровнем абстракции
        за счёт sqlalchemy.
        """
        with sync_engine.connect() as conn:

            # stmt = text("UPDATE workers SET username=:username WHERE id=:id")
            # stmt = stmt.bindparams("username=new_username, id=worker_id")

            stmt = (
                update(workers_table)
                .values(username=new_username)
                # .where(workers_table.c.id==worker_id)
                .filter_by(id=worker_id)
            )

            conn.execute(stmt)
            conn.commit()