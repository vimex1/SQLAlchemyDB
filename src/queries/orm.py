from sqlalchemy import text, insert, inspect, select, func, cast, Integer, and_
from database import sync_engine, async_engine, session_factory, async_session_factory, Base
from models import WorkersOrm, workers_table, ResumesOrm, Workload

# def create_tables():
#     sync_engine.echo = False
#     Base.metadata.drop_all(sync_engine)
#     Base.metadata.create_all(sync_engine)
#     sync_engine.echo = True

# Асинхронный вариант, не показанный в видео
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