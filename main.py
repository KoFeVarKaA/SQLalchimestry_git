from src.queries.orm import SyncORM
from src.queries.core import SyncCore

# SyncORM.create_tables()
# SyncORM.insert_workers()
# SyncORM.insert_resumes()
# SyncORM.select_workers_with_condition_relationship()
# SyncORM.select_workers_with_condition_relationship_contains_eager()
SyncCore.select_workers(2)