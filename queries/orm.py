from sqlalchemy import select, and_, func, Integer
from sqlalchemy.orm import aliased, joinedload, selectinload
from models import Base, Worker, Resume, Workload
from database import engine, session_factory, async_session_factory
from pprint import pprint


class SyncORM:

    @staticmethod
    def create_tables_orm():
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    @staticmethod
    def select_orm(id: int):
        with session_factory() as session:
            res = session.get(Worker, id)
            # print(f"{res=}")
            pprint(res)
            # print(res)

    @staticmethod
    def select_all_orm():
        with session_factory() as session:
            # res = session.query(Worker).all()
            # for worker in res:
            #     print(worker)

            stmt = select(Worker)
            result = session.execute(stmt)
            print(result.scalars().all())

    @staticmethod
    async def select_all_orm_async():
        async with async_session_factory() as session:
            # res = session.query(Worker).all()
            # for worker in res:
            #     print(worker)

            stmt = select(Worker)
            result = await session.execute(stmt)
            print(result.scalars().all())

    @staticmethod
    def select_01_orm():
        with session_factory() as session:
            # res = session.query(Worker).all()
            # for worker in res:
            #     print(worker)

            stmt = (
                select(
                    Resume.workload,
                    # func.avg(Resume.compensation).label("avg_compensation")
                    func.round(func.avg(Resume.compensation), 2).label("avg_compensation")
                )
                .select_from(Resume)
                .where(
                    and_(
                        Resume.compensation > 40000,
                        #Resume.title.contains("Python")
                        func.lower(Resume.title).contains("python")
                    )
                )
                .group_by(Resume.workload)
            )
            print(stmt.compile(compile_kwargs={"literal_binds": True}))
            # result = session.execute(stmt)
            # print(result.all())

    # session.expire(obj) или session.expire_all() - сбросить все изменения в конкр объекте или в сессии

    @staticmethod
    def insert_orm():
        with session_factory() as session:
            worker_alice = Worker(name='Ryan')
            worker_dick = Worker(name="Eric")
            session.add_all([worker_alice, worker_dick])
            session.flush()
            session.commit()

    @staticmethod
    def insert_orm_test_data():
        with session_factory() as session:
            worker_ryan = Worker(name='Ryan')
            worker_alice = Worker(name="Alice")
            session.add_all([worker_ryan, worker_alice])
            session.flush()
            resume_junior = Resume(
                title="Python junior developer",
                compensation=50000,
                workload=Workload.fulltime,
                worker_id=worker_ryan.id
            )
            resume_dev = Resume(
                title="Python developer",
                compensation=150000,
                workload=Workload.fulltime,
                worker_id=worker_ryan.id
            )
            resume_data_engineer = Resume(
                title="Python data engineer",
                compensation=250000,
                workload=Workload.parttime,
                worker_id=worker_alice.id
            )
            resume_data_scientist = Resume(
                title="Data scientist",
                compensation=300000,
                workload=Workload.fulltime,
                worker_id=worker_alice.id
            )
            session.add_all([resume_junior, resume_dev, resume_data_engineer, resume_data_scientist])
            session.commit()

    @staticmethod
    async def insert_orm_additional_test_data():
        async with async_session_factory() as async_session:
            worker_artem = Worker(name='Artem')
            worker_roman = Worker(name='Roman')
            worker_petr = Worker(name='Petr')
            async_session.add_all([worker_artem, worker_roman, worker_petr])
            await async_session.flush()
            resume_1 = Resume(
                title="Python programmer",
                compensation=60000,
                workload=Workload.fulltime,
                worker_id=worker_artem.id
            )
            resume_2 = Resume(
                title="Machine learning engineer",
                compensation=70000,
                workload=Workload.parttime,
                worker_id=worker_artem.id
            )
            resume_3 = Resume(
                title="Python data scientist",
                compensation=80000,
                workload=Workload.parttime,
                worker_id=worker_roman.id
            )
            resume_4 = Resume(
                title="Python analyst",
                compensation=90000,
                workload=Workload.fulltime,
                worker_id=worker_roman.id
            )
            resume_5 = Resume(
                title="Python junior developer",
                compensation=100000,
                workload=Workload.fulltime,
                worker_id=worker_petr.id
            )
            async_session.add_all([resume_1, resume_2, resume_3, resume_4, resume_5])
            await async_session.commit()

    @staticmethod
    async def test_join_subquery_cte():
        async with async_session_factory() as async_session:
            w = aliased(Worker)
            r = aliased(Resume)
            subquery = (
                select(
                    w.id,
                    w.name,
                    r.id,
                    r.title,
                    r.compensation,
                    r.workload,
                    func.avg(r.compensation).over(partition_by=r.workload).cast(Integer).label('avg_compensation')
                ).select_from(w)
                .join(r, w.id == r.worker_id)
            ).subquery('q')
            cte = (
                select(
                    subquery.c.id,
                    subquery.c.name,
                    subquery.c.id,
                    subquery.c.title,
                    subquery.c.compensation,
                    subquery.c.workload,
                    subquery.c.avg_compensation,
                    (subquery.c.compensation - subquery.c.avg_compensation).label('diff_compensation')
                ).cte('t')
            )
            query = (
                select(cte).order_by(cte.c.diff_compensation.desc())
            )
            res = await async_session.execute(query)
            print(res.all())

    @staticmethod
    def inspect():
        # print(Worker.get_mapper().__dict__)
        cols = Worker.get_mapper().columns
        for col in cols:
            print(col)
            print(col.key)

    # joinedload -> suits for many-to-one and one-to-one relationship
    # selectinload -> suits for one-to-many and many-to-many relationship

    # в асинхронном варианте lazy loading не работает (вызывает ошибку), только eager loading
    # можно использовать resumes = await worker.awaitable_attrs.resumes
    @staticmethod
    def select_rels_lazy_load():
        with session_factory() as session:
            stmt = select(Worker)
            res = session.execute(stmt).scalars().all()
            print(res)

            print(res[0].resumes)

            print()

    @staticmethod
    def select_rels_joined_load():
        with session_factory() as session:
            stmt = select(Worker).options(joinedload(Worker.resumes))
            res = session.execute(stmt).unique().scalars().all()
            print(res)

            print(res[0].resumes)

            print()

    @staticmethod
    def select_rels_selectinload():
        with session_factory() as session:
            stmt = select(Worker).options(selectinload(Worker.resumes))
            res = session.execute(stmt).unique().scalars().all()
            print(res)

            print(res[0].resumes)

            print()