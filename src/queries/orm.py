from sqlalchemy import text, insert, inspect, select, func, cast, Integer, and_
from sqlalchemy.orm import aliased, joinedload, selectinload, contains_eager
from database import sync_engine, async_engine, session_factory, async_session_factory, Base
from models import WorkersOrm, workers_table, ResumesOrm, Workload

# def create_tables():
#     sync_engine.echo = False
#     Base.metadata.drop_all(sync_engine)
#     Base.metadata.create_all(sync_engine)
#     sync_engine.echo = True

# Асинхронный вариант
# async def create_tables():
#    async with async_engine.begin() as conn:
#        await conn.run_sync(Base.metadata.drop_all)
#        await conn.run_sync(Base.metadata.create_all)

# def insert_data():
#     with session_factory() as session:
#         worker_jack = WorkersOrm(username="Jack")
#         worker_michael = WorkersOrm(username="Michael")
#         session.add_all([worker_jack, worker_michael])
#         session.commit()

# async def insert_data():
#    async with async_session_factory() as session:
#        worker_jack = WorkersOrm(username="Jack")
#        worker_michael = WorkersOrm(username="Michael")
#        session.add_all([worker_jack, worker_michael])
#        await session.commit()

class SyncORM:
    @staticmethod
    def create_tables():
        """
        Создает таблицы в базе данных, согласно описанию моделей,
        определенных в файле models.py.
        """
        sync_engine.echo = False
        Base.metadata.drop_all(sync_engine)     # Удаляет все таблицы, которые уже есть в базе
        Base.metadata.create_all(sync_engine)   # Создает таблицы, согласно описанию моделей
        sync_engine.echo = True

    @staticmethod
    def insert_workers():
        with session_factory() as session:
            worker_jack = WorkersOrm(username="Jack")
            worker_michael = WorkersOrm(username="Michael")
            session.add_all([worker_jack, worker_michael])
            session.flush()     # Отправляет изменения в БД, которые есть в session, но не завершает запрос как commit(). flush() также присваивает первичный ключ (в данном случае id) нашему работнику.
            session.commit()

    @staticmethod
    def insert_resumes():
        with session_factory() as session:
            resume_1 = ResumesOrm(title="Python Junior Developer", compensation=50000, workload=Workload.fulltime, worker_id=1)
            resume_2 = ResumesOrm(title="Python Разработчик", compensation=120000, workload=Workload.parttime, worker_id=1)
            resume_3 = ResumesOrm(title="Python Data Engineer", compensation=30000, workload=Workload.fulltime, worker_id=2)
            resume_4 = ResumesOrm(title="Data Scientist", compensation=40000, workload=Workload.parttime, worker_id=2)
            session.add_all([resume_1, resume_2, resume_3, resume_4])
            session.commit()
    
    @staticmethod
    def select_workers():
        with session_factory() as session:
            # worker_id = 1
            # worker_jack = session.get(WorkersOrm, worker_id)
            query = select(WorkersOrm)   # SELECT * FROM workers
            result = session.execute(query)
            workers = result.scalars().all()
            print("\n     vvv select-orm запрос vvv       ")
            print(f"Таблица: {workers=}")

    @staticmethod
    def update_worker(worker_id: int = 2, new_username: str = "Misha"):
        """
        Код в формате ORM выглядит лаконичнее и проще, нежели в формате Core.
        Более питонячий подход, требует больше запросов. Сначала получить объект,
        затем обновить его данные.
        """
        with session_factory() as session:
            worker_michael = session.get(WorkersOrm, worker_id)
            worker_michael.username = new_username
            session.refresh(worker_michael)     # Запрос refresh() обращается к БД, освежая актуальные данные об объекте. ВАЖНО! В Core такое реализовать сложнее!
            session.commit()

    @staticmethod
    def select_resumes_avg_compensation(like_language: str = "Python"):
        """
        select workload, avg(compensation)::int as avg_compensation
        from resumes
        where title like '%Python%' and compensation > 40000
        group by workload
        """
        with session_factory() as session:
            query = (
                select(
                    ResumesOrm.workload,
                    cast(func.avg(ResumesOrm.compensation), Integer).label("avg_compensation")
                )
                .select_from(ResumesOrm)
                .filter(and_(
                    ResumesOrm.title.contains(like_language),
                    ResumesOrm.compensation > 40000,
                ))
                .group_by(ResumesOrm.workload)
                .having(cast(func.avg(ResumesOrm.compensation), Integer) > 70000)    # Замечание: Нельзя обратиться напрямую к столбцу "avg_compensation", который мы хотим создать
            )
            print("\n       Select-запрос с группировкой и фильтром к таблице Resumes:")
            print(query.compile(compile_kwargs={"literal_binds": True}))        # забиндить значения, которые мы подставляем
            res = session.execute(query)
            result = res.all()

            print(f"\nРезультат: {result[0].avg_compensation}")

    @staticmethod
    def insert_additional_resumes():
        with session_factory() as session:
            workers = [
                {"username": "Artem"},
                {"username": "Roman"},
                {"username": "Petr"},
            ]
            resumes = [
                {"title": "Python Analyst", "compensation": 90000, "workload": Workload.parttime, "worker_id": 3},
                {"title": "Python Senior Developer", "compensation": 500000, "workload": Workload.fulltime, "worker_id": 3},
                {"title": "Machine Learning Engineer", "compensation": 160000, "workload": Workload.fulltime, "worker_id": 4},
                {"title": "DevOps Engineer", "compensation": 80000, "workload": Workload.fulltime, "worker_id": 4},
                {"title": "UI/UX Designer", "compensation": 110000, "workload": Workload.fulltime, "worker_id": 5},
            ]
            insert_workes = insert(WorkersOrm).values(workers)
            insert_resumes = insert(ResumesOrm).values(resumes)
            session.execute(insert_workes)
            session.execute(insert_resumes)
            session.commit()

    @staticmethod
    def join_cte_subquery_window_func(like_language: str = "Python"):
        with session_factory() as session:
            """
            WITH helper2 AS (
                SELECT *, compensation-avg_workload_compensation AS compensation_diff
                FROM
                (SELECT
                    w.id,
                    w.username,
                    r.compensation,
                    r.workload,
                    avg(r.compensation) OVER (PARTITION BY workload)::int AS avg_workload_compensation
                
                FROM resumes r
                JOIN workers w ON r.worker_id = w.id) helper1
            )

            SELECT * FROM helper2
            """
            r = aliased(ResumesOrm)
            w = aliased(WorkersOrm)
            subq = (
                select(
                    r,
                    w,
                    func.avg(r.compensation).over(partition_by=r.workload).cast(Integer).label("avg_workload_compensation"),
                )
                #.select_from(r)
                .join(r, r.worker_id == w.id).subquery("helper1")
            )

            cte = (
                select(
                    subq.c.worker_id,
                    subq.c.username,
                    subq.c.compensation,
                    subq.c.workload,
                    subq.c.avg_workload_compensation,
                    (subq.c.compensation - subq.c.avg_workload_compensation).label("compensation_diff"),
                )
                .cte("helper2")
            )
            query = (
                select(cte)
                .order_by(cte.c.compensation_diff.desc())
            )

            res = session.execute(query)
            result = res.all()
            print(f"\nРезультат:\n{result}")

            #print(query.compile(compile_kwargs={"literal_binds": True}))

    @staticmethod
    def select_workers_with_lazy_relationship():
        with session_factory() as session:
            query = (
                select(WorkersOrm)
            )
            res = session.execute(query)
            result = res.scalars().all()

            print("\n\n     vvv     select_workers_with_lazy_relationship       vvv     \n\n")
            worker_1_resumes = result[0].resumes
            print("\n", worker_1_resumes)

            worker_2_resumes = result[1].resumes
            print("\n", worker_2_resumes)

    @staticmethod
    def select_workers_with_join_relationship():
        """
        Many-to-one, one-to-one 
        """
        with session_factory() as session:
            query = (
                select(WorkersOrm)
                .options(joinedload(WorkersOrm.resumes))
            )
            res = session.execute(query)
            result = res.unique().scalars().all()

            print("\n\n     vvv     select_workers_with_join_relationship       vvv     \n\n")
            worker_1_resumes = result[0].resumes
            print("\n", worker_1_resumes)

            worker_2_resumes = result[1].resumes
            print("\n", worker_2_resumes)

    @staticmethod
    def select_workers_with_selectin_relationship():
        """
        One-to-many, many-to-many
        """
        with session_factory() as session:
            query = (
                select(WorkersOrm)
                .options(joinedload(WorkersOrm.resumes))
            )
            res = session.execute(query)
            result = res.unique().scalars().all()

            print("\n\n     vvv     select_workers_with_selectin_relationship       vvv     \n\n")
            worker_1_resumes = result[0].resumes
            print("\n", worker_1_resumes)

            worker_2_resumes = result[1].resumes
            print("\n", worker_2_resumes)

    @staticmethod
    def select_workers_with_condition_relationship():
        with session_factory() as session:
            query = (
                select(WorkersOrm)
                .options(selectinload(WorkersOrm.resumes_parttime))
            # если хочется подгрузить несколько relationship'ов, то нужно прописать несколько .options
            )
            
            res = session.execute(query)
            result = res.scalars().all()

            print("\n\n     vvv     select_workers_with_condition_relationship       vvv     \n\n")
            print(result)

    @staticmethod
    def select_workers_with_condition_relationship_contains_eager():
        with session_factory() as session:
            query = (
                select(WorkersOrm)
                .join(WorkersOrm.resumes)
                .options(contains_eager(WorkersOrm.resumes))
                .filter(ResumesOrm.workload == "parttime")

            )
            
            res = session.execute(query)
            result = res.unique().scalars().all()

            print("\n\n     vvv     select_workers_with_condition_relationship_contains_eager       vvv     \n\n")
            print(result)

    @staticmethod
    def select_workers_with_relationship_contains_eager_with_limit():
        with session_factory() as session:
            subq = (
                select(ResumesOrm.id.label("parttime_resume_id"))
                .filter(ResumesOrm.worker_id == WorkersOrm.id)
                .order_by(WorkersOrm.id.desc())
                .limit(2)
                .scalar_subquery()
                .correlate(WorkersOrm)
            )

            query = (
                select(WorkersOrm)
                .join(ResumesOrm, ResumesOrm.id.in_(subq))
                .options(contains_eager(WorkersOrm.resumes))
            )

            res = session.execute(query)
            result = res.unique().scalars().all()

            print("\n\n     vvv     select_workers_with_relationship_contains_eager_with_limit       vvv     \n\n")
            print(result)