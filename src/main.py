import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

#Задание: добавить вакансии в таблицу resumes - успешно

from queries.orm import SyncORM
from queries.core import SyncCore

SyncORM.create_tables()
# SyncCore.create_tables()

SyncORM.insert_workers()
# SyncCore.insert_workers()

SyncORM.insert_resumes()


# SyncCore.select_workers()
# SyncCore.update_worker()

SyncORM.select_workers()

SyncORM.update_worker()

SyncORM.select_resumes_avg_compensation()

SyncORM.insert_additional_resumes()

SyncORM.join_cte_subquery_window_func()

SyncORM.select_workers_with_lazy_relationship()

SyncORM.select_workers_with_join_relationship()

SyncORM.select_workers_with_selectin_relationship()

SyncORM.select_workers_with_condition_relationship()

SyncORM.select_workers_with_condition_relationship_contains_eager()

SyncORM.select_workers_with_relationship_contains_eager_with_limit()