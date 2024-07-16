from database import engine, async_engine
from sqlalchemy import text, insert, select, update
from models import metadata, workers_table, Base


class SyncCore:

    @staticmethod
    def run_sync():
        with engine.connect() as conn:
            res = conn.execute(text("SELECT 1 as OOPS, VERSION()"))
            print(f"{res.one()=}")

    @staticmethod
    def create_tables():
        metadata.drop_all(engine)
        metadata.create_all(engine)

    @staticmethod
    def create_tables_orm():
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    @staticmethod
    def select_raw():
        with engine.connect() as conn:
            stmt = """
                SELECT * FROM workers;
                """
            res = conn.execute(text(stmt)).scalars("name").all()
            print(f"{res=}")

    @staticmethod
    def select_core():
        with engine.connect() as conn:
            stmt = select(workers_table)
            res = conn.execute(stmt).all()
            print(f"{res=}")

    @staticmethod
    def insert_raw():
        with engine.connect() as conn:
            stmt = """
            insert into workers
            values
                (1, 'Vasya'),
                (2, 'Petya');
            """
            conn.execute(text(stmt))
            conn.commit()

    @staticmethod
    def insert_core():
        with engine.connect() as conn:
            stmt = insert(workers_table).values(
                [
                    (3, 'Anthony'),
                    (4, 'Joee')
                ]
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def update_raw(id: int, new_name: str):
        with engine.connect() as conn:
            stmt = text("""
                    UPDATE workers SET name = :new_name WHERE id = :id;
                    """)
            stmt = stmt.bindparams(id=id, new_name=new_name)
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def update_core(id: int, new_name: str):
        with engine.connect() as conn:
            stmt = (
                update(workers_table)
                .values(name=new_name)
                .filter_by(id=id)
            )
            conn.execute(stmt)
            conn.commit()


class AsyncCore:

    @staticmethod
    async def run_async():
        async with async_engine.connect() as conn:
            res = await conn.execute(text("SELECT 1 as OOPS, VERSION()"))
            print(f"{res.all()[0]=}")
