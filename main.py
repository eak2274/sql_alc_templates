import os
import sys
import asyncio
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from queries.core import SyncCore, AsyncCore
from queries.orm import SyncORM

# run_sync()
# SyncORM.create_tables_orm()
# insert_raw()
# SyncCore.create_tables_orm()
# SyncCore.insert_orm()
# SyncCore.select_raw()
# SyncCore.select_core()
# SyncCore.update_raw(4, "Jeremy")
# SyncCore.update_core(4, 'Barney')
# SyncCore.select_raw()
# SyncORM.insert_orm()
# SyncORM.select_all_orm()
# SyncORM.insert_orm_test_data()
# SyncORM.select_01_orm()
# asyncio.run(SyncORM.insert_orm_additional_test_data())
# asyncio.run(SyncORM.test_join_subquery_cte())
# SyncORM.inspect()
# SyncORM.select_rels()
SyncORM.select_rels_selectinload()
